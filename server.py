"""Multi-client TCP chat server.

Run: python server.py
Default port: 5000
This is an educational example; messages are not encrypted or authenticated.
"""

import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}  # socket -> username
lock = threading.Lock()
stopping = threading.Event()


def send_line(sock: socket.socket, message: str) -> None:
    """Send one newline-delimited UTF-8 message."""
    sock.sendall((message.replace("\r", " ").replace("\n", " ") + "\n").encode("utf-8"))


def broadcast(message: str, exclude=None) -> None:
    """Send a message to all currently connected clients."""
    with lock:
        recipients = list(clients.keys())

    for recipient in recipients:
        if recipient is exclude:
            continue
        try:
            send_line(recipient, message)
        except OSError:
            remove_client(recipient)


def remove_client(client: socket.socket) -> None:
    """Remove and close a client safely; announce departure if named."""
    with lock:
        username = clients.pop(client, None)

    try:
        client.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    try:
        client.close()
    except OSError:
        pass

    if username:
        print(f"{username} disconnected")
        if not stopping.is_set():
            broadcast(f"[SERVER] {username} left the chat.")


def read_line(reader) -> str | None:
    """Read one complete newline-terminated line from a text stream."""
    line = reader.readline()
    if line == "":
        return None
    return line.rstrip("\r\n")


def handle_client(client: socket.socket, address) -> None:
    username = None
    try:
        client.settimeout(300)
        reader = client.makefile("r", encoding="utf-8", newline="\n")
        send_line(client, "Enter your username:")

        requested = read_line(reader)
        if requested is None:
            return
        username = requested.strip()[:30]
        if not username:
            username = f"Guest-{address[1]}"

        # Keep usernames unique for a clear classroom demonstration.
        with lock:
            existing = {name.casefold() for name in clients.values()}
            base_name = username
            suffix = 2
            while username.casefold() in existing:
                username = f"{base_name[:25]}-{suffix}"
                suffix += 1
            clients[client] = username

        print(f"{username} connected from {address}")
        send_line(client, f"[SERVER] Welcome, {username}. Type /quit to leave.")
        broadcast(f"[SERVER] {username} joined the chat.", exclude=client)

        for raw_message in reader:
            message = raw_message.strip()
            if not message:
