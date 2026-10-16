
Multi-Client Chat Application Using Python
A beginner-friendly real-time terminal chat application built with Python TCP sockets and threads. Multiple clients connect to one server and messages are broadcast to all connected users.

Features
TCP client-server communication
Multiple simultaneous clients using one thread per client
Broadcast messages to connected users
Join/leave notifications
Unique usernames within the current server session
/quit command for a graceful client exit
No third-party packages required
Requirements
Python 3.9 or later recommended
Windows, macOS, or Linux
Standard Python libraries only: socket, threading
Project files
chat_application/
├── server.py
├── client.py
└── README.md
Run on Windows
Open a terminal in this folder.

1. Start the server
python server.py
If needed, use py server.py.

2. Start the first client
Open a second terminal in the same folder:

python client.py
Enter 127.0.0.1 as the server IP if both programs are on the same computer. Choose a username.

3. Start another client
Open a third terminal and run python client.py again. Choose a different username. Messages sent by one client should appear for the other connected clients.

4. Stop
Type /quit in a client to leave. Press Ctrl+C in the server terminal to stop the server.

Connect from another computer on the same LAN
Run ipconfig on the server computer and find its IPv4 address.
In the client, enter that LAN IP instead of 127.0.0.1.
Ensure both devices are on a network that permits device-to-device connections.
Allow Python/server port TCP 5000 through the host firewall only on a trusted private network, if required.
127.0.0.1 always refers to the client computer itself; it is not the server's address when the server is on another machine.

How it works
The server creates a TCP listening socket on port 5000.
Each accepted client is handled by a separate thread.
Clients send UTF-8 messages terminated by a newline.
The server broadcasts each message to connected clients.
A lock protects the shared client dictionary.
Networking concepts demonstrated
TCP/IP
Client-server architecture
IP addresses and port numbers
Socket programming
Multithreading
Message broadcasting
Newline-delimited application messages
Limitations and safety
This is an educational demonstration, not a production-ready messenger. It does not encrypt messages or authenticate users. Use only on trusted networks; do not expose it to the public internet as-is. Add TLS, authentication, rate limits, and stronger input validation before real-world deployment.

Possible extensions
Tkinter graphical interface
Private messaging
Online-user list
Timestamps and saved chat history
TLS encryption and user authentication
⋮⋮⋮⋮⋮⋮⋮⋮⋮⋮⋮⋮
