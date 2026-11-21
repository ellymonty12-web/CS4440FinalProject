
# client.py

import socket
import threading
import json
import queue
import sys
import turtle

from config import (
    SERVER_PORT,
    WIDTH,
    HEIGHT,
    PADDLE_SPEED
)

# Server address can be supplied from the command line.
SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

# Thread-safe queue for messages received from the server.
messages = queue.Queue()

# Connect to the server.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

# Set up the Turtle window.
screen = turtle.Screen()
screen.title("Multiplayer Pong Prototype")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)

# Create a paddle.
def create_paddle(x, color):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color(color)
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x, 0)
    return paddle


left_paddle = create_paddle(-350, "white")
right_paddle = create_paddle(350, "cyan")

# Display connection information.
status = turtle.Turtle()
status.hideturtle()
status.color("white")
status.penup()
status.goto(0, 250)

player_id = None
running = True


def receive_messages():
    """Receive network messages in a background thread."""
    try:
        with client.makefile("r", encoding="utf-8") as stream:
            for line in stream:
                try:
                    message = json.loads(line)
                    messages.put(message)
                except json.JSONDecodeError:
                    continue
    except (OSError, ValueError):
        pass
    finally:
        messages.put({"type": "disconnected"})


def send_move(direction):
    """Send a movement command to the server."""
    if not running or player_id is None:
        return

    message = {
        "type": "move",
        "direction": direction
    }

    try:
        data = json.dumps(message) + "\n"
        client.sendall(data.encode("utf-8"))
    except OSError:
        messages.put({"type": "disconnected"})


def move_up():
    send_move("up")


def move_down():
    send_move("down")


def update_screen():
    """Process received messages on Turtle's main thread."""
    global player_id, running

    while not messages.empty():
        message = messages.get()

        if message.get("type") == "welcome":
            player_id = message["player"]

            status.clear()
            status.write(
                f"You are Player {player_id}",
                align="center",
                font=("Arial", 16, "normal")
            )

        elif message.get("type") == "state":
            paddles = message["paddles"]

            left_paddle.sety(paddles["1"])
            right_paddle.sety(paddles["2"])

        elif message.get("type") == "error":
            status.clear()
            status.write(
                message.get("message", "Server error"),
                align="center",
                font=("Arial", 16, "normal")
            )
            running = False

        elif message.get("type") == "disconnected":
            status.clear()
            status.write(
                "Disconnected from server",
                align="center",
                font=("Arial", 16, "normal")
            )
            running = False

    screen.update()

    if running:
        screen.ontimer(update_screen, 30)


def close_game():
    """Close the connection and Turtle window."""
    global running
    running = False

    try:
        client.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass

    client.close()
    screen.bye()


# Register keyboard controls.
screen.listen()

screen.onkeypress(move_up, "w")
screen.onkeypress(move_down, "s")

screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")

# Close with Escape.
screen.onkey(close_game, "Escape")

# Start the network receiver.
receiver = threading.Thread(
    target=receive_messages,
    daemon=True
)
receiver.start()

# Start the graphical update loop.
update_screen()

screen.mainloop()
