# Multiplayer Pong

A multiplayer Pong game developed in Python. The project uses Python sockets, threading, and Turtle graphics to demonstrate operating systems concepts like processes, interprocess communication, concurrency, and synchronization.

## Current Version: 0.1 — Networking Prototype

This initial prototype allows two clients to connect to a Python server and control separate paddles.

**Current features:**
- Two clients can connect to one server.
- Each client is assigned a player number.
- Each player controls a paddle using keyboard input.
- Paddle positions are synchronized across both client windows.
- The server uses threads to handle client connections.
- A lock protects shared game state.

**Not yet implemented:**
- Ball movement and collisions
- Scoring and win conditions
- Support for more than two players
- Menus and player customization

## Requirements

- Python 3 with Tkinter/Turtle support
- PyCharm, VS Code, or another Python-compatible environment

No additional Python packages are required for this prototype.

## How to Run the Prototype

### 1. Download the Project

Clone the GitHub repository using GitHub Desktop, or download the repository as a ZIP file and extract it.

Open the project folder in PyCharm or VS Code.

### 2. Start the Server

Open a terminal in the project directory and run:

```bash
python server.py
```

The server should display:

```text
Server listening on port 5555
```

Keep this terminal running.

### 3. Start Player 1

Open a second terminal in the same project directory and run:

```bash
python client.py 127.0.0.1
```

A Turtle window should open displaying the Pong paddles.

### 4. Start Player 2

Open a third terminal and run:

```bash
python client.py 127.0.0.1
```

A second Turtle window should open.

Both clients should now be connected to the server.

## Controls

Player 1 : W / S or Up / Down
Player 2 : W / S or Up / Down

Each client controls only its assigned paddle. Select the appropriate Turtle window before pressing the movement keys.

Press **Escape** to close a client window.

## Expected Results

1. Moving Player 1's paddle should update its position in both windows.
2. Moving Player 2's paddle should update its position in both windows.
3. The server terminal should display messages when players connect or disconnect.

The prototype can be tested entirely on one computer.

## Connecting from Another Computer

The server and clients can also communicate over a local network.

1. Connect both computers to the same network.
2. Run `server.py` on the host computer.
3. Find the host computer's local IPv4 address using `ipconfig` on Windows.
4. On the second computer, run:

```bash
python client.py SERVER_IP
```

Replace `SERVER_IP` with the host computer's actual IPv4 address.

The default TCP port is `5555`.

Windows Firewall may need to be configured to allow incoming connections to the server.

## Project Files

| File | Description |
|---|---|
| `server.py` | Accepts client connections, processes movement requests, and broadcasts paddle positions. |
| `client.py` | Displays the Turtle window, handles keyboard input, and communicates with the server. |
| `config.py` | Contains network and game configuration settings. |
| `.gitignore` | Excludes generated files, local environments, and IDE settings from Git. |

## Additional Notes

This is an early prototype intended to verify that Python sockets and Turtle graphics can support multiplayer communication.

Future versions will expand the game while continuing to demonstrate operating systems concepts.