
# server.py

import socket
import threading
import json

from config import SERVER_HOST, SERVER_PORT, PADDLE_LIMIT

# Shared game state.
paddles = {
    "1": 0,
    "2": 0
}

# Connected clients.
clients = {}

# Protects shared state.
game_lock = threading.Lock()


def send_message(conn, message):
    """Send one JSON message over TCP."""
    data = json.dumps(message) + "\n"
    conn.sendall(data.encode("utf-8"))


def broadcast_state():
    """Send paddle positions to both players."""
    with game_lock:
        state = {
            "type": "state",
            "paddles": paddles.copy()
        }
        connections = list(clients.values())

    for conn in connections:
        try:
            send_message(conn, state)
        except OSError:
            pass


def handle_client(conn, player_id):
    """Receive and process one player's input."""
    try:
        send_message(conn, {
            "type": "welcome",
            "player": player_id
        })

        broadcast_state()

        # TCP is a stream, so read complete JSON lines.
        with conn.makefile("r", encoding="utf-8") as stream:
            for line in stream:
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if message.get("type") != "move":
                    continue

                direction = message.get("direction")

                if direction not in ("up", "down"):
                    continue

                with game_lock:
                    change = 20 if direction == "up" else -20
                    new_y = paddles[player_id] + change

                    paddles[player_id] = max(
                        -PADDLE_LIMIT,
                        min(PADDLE_LIMIT, new_y)
                    )

                broadcast_state()

    except (OSError, ValueError):
        pass

    finally:
        with game_lock:
            clients.pop(player_id, None)

        conn.close()
        print(f"Player {player_id} disconnected.")
        broadcast_state()


def main():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(2)

    print(f"Server listening on port {SERVER_PORT}")

    try:
        while True:
            conn, address = server.accept()

            with game_lock:
                available = [
                    p for p in ("1", "2")
                    if p not in clients
                ]

                if available:
                    player_id = available[0]
                    clients[player_id] = conn
                    paddles[player_id] = 0
                else:
                    player_id = None

            if player_id is None:
                send_message(conn, {
                    "type": "error",
                    "message": "Match is full"
                })
                conn.close()
                continue

            print(f"Player {player_id} connected: {address}")

            thread = threading.Thread(
                target=handle_client,
                args=(conn, player_id),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nServer shutting down.")

    finally:
        server.close()


if __name__ == "__main__":
    main()
