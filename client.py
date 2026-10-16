"""Terminal client for the multi-client TCP chat application.

Run: python client.py
Use 127.0.0.1 when the server runs on this same computer.
"""

import socket
import threading

PORT = 5000
MAX_LINE_BUFFER = 8192


def receive_messages(client: socket.socket, finished: threading.Event) -> None:
    """Read newline-delimited server messages without blocking user input."""
    buffer = ""
    try:
        while not finished.is_set():
            data = client.recv(4096)
            if not data:
                break
            buffer += data.decode("utf-8")

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                print(f"\n{message}")
                print("> ", end="", flush=True)

            if len(buffer) > MAX_LINE_BUFFER:
                print("\nServer sent an oversized message; disconnecting.")
                break
    except (ConnectionError, OSError, UnicodeError):
        pass
    finally:
        finished.set()
        print("\nConnection to server closed.")


def main() -> None:
    host = input("Server IP (127.0.0.1 for this computer): ").strip()
    if not host:
        host = "127.0.0.1"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    finished = threading.Event()

    try:
        client.connect((host, PORT))
        print(f"Connected to {host}:{PORT}.")

        receiver = threading.Thread(
            target=receive_messages,
            args=(client, finished),
            daemon=True,
        )
        receiver.start()

        username = input("Choose a username: ").strip()[:30]
        client.sendall((username + "\n").encode("utf-8"))
        print("Start chatting. Type /quit to exit.")

        while not finished.is_set():
            try:
                message = input("> ")
            except EOFError:
                message = "/quit"

            if message.strip().lower() == "/quit":
                try:
                    client.sendall(b"/quit\n")
                except OSError:
                    pass
                break

            message = message.strip()
            if message:
                try:
                    client.sendall((message.replace("\n", " ") + "\n").encode("utf-8"))
                except (ConnectionError, OSError) as error:
                    print(f"Could not send message: {error}")
                    break

    except (ConnectionError, OSError) as error:
        print(f"Connection error: {error}")
        print("Check that the server is running and the IP address is correct.")
    finally:
        finished.set()
        try:
            client.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        client.close()


if __name__ == "__main__":
    main()
