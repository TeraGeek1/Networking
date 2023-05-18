"""Server Side Advanced GUI Chat room"""
import socket as soc
import threading
import json
import sys
from connection.Server import Connection
from connection.locals import *
import tkinter
from tkinter import END, DISABLED, NORMAL, VERTICAL, messagebox

# Def Window
root = tkinter.Tk()
root.title("Chat server")
root.geometry("600x600")
root.resizable(False, False)
root.config(bg=BLACK)


# Def func
def start_server(connection: Connection):
    """Start a server with the given port"""

    start_gui()
    connection.connected = True

    # Get the port to run the server on and bind to the connection object
    try:
        connection.port = int(port_entry.get())
    except ValueError:
        error_message = f"The port entry can not be empty"
        history_listbox.insert(0, error_message)
        print(error_message)
        return False

    # Create server socket
    connection.soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    connection.soc.bind((connection.host_ip, connection.port))
    connection.soc.listen()

    # Update GUI
    history_listbox.delete(0, END)
    history_listbox.insert(
        0, f"Server started on {connection.host_ip}:{connection.port}..."
    )

    # Create a thread to continuously listen for connections
    connect_thread = threading.Thread(target=connect_client, args=(connection,))
    connect_thread.start()

    return True


def end_server(connection: Connection):
    """Begin the process of ending the server"""

    connection.connected = False

    # Alert all users that that the server is closing
    message_packet = create_message(
        F_DISCONNECT, "Admin", "Server is closing", LIGHT_GREEN
    )
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json)

    # Update GUI
    end_gui()

    connection.soc.close()


def connect_client(connection: Connection):
    """Connect a incoming client to the server"""

    while True:
        try:
            client_soc, client_addr = connection.soc.accept()

            if client_addr[0] in connection.baned_ips:
                message_packet = create_message(
                    F_DISCONNECT,
                    "Server (private)",
                    "You Have been BANED...goodbye",
                    LIGHT_GREEN,
                )

                message_json = json.dumps(message_packet)
                client_soc.send(message_json.encode(connection.encoder))

                # Close the client socket
                client_soc.close()
                continue

            if connection.connected == False:
                message_packet = create_message(
                    F_DISCONNECT,
                    "Server (private)",
                    "The server is still closed",
                    LIGHT_GREEN,
                )

                message_json = json.dumps(message_packet)
                client_soc.send(message_json.encode(connection.encoder))

                # Close the client socket
                client_soc.close()

                continue

            # Send a message packet to receive client info
            message_packet = create_message(
                F_INFO,
                "Server (private)",
                "Creating local account...",
                LIGHT_GREEN,
            )

            message_json = json.dumps(message_packet)
            client_soc.send(message_json.encode(connection.encoder))

            # Wait for confirmation message to be sent verifying the connection
            message_json = client_soc.recv(connection.bytesize).decode(
                connection.encoder
            )
            process_message(connection, message_json, client_soc, client_addr)

        except:
            error_class = sys.exc_info()[0]
            error_message = sys.exc_info()[1]
            my_message = "Error in client connection thread"
            history_listbox.insert(0, f"{error_class}")
            history_listbox.insert(1, f"{error_message}")
            history_listbox.insert(2, my_message)
            print(error_class)
            print(error_message)
            print(my_message)
            break


def create_message(flag, name, text, color):
    """Return a message packet to be sent"""

    message_packet = {
        "flag": flag,
        "name": name,
        "text": text,
        "color": color,
    }

    return message_packet


def process_message(
    connection: Connection,
    message_json: str,
    client_soc: soc.socket,
    client_addr=(0, 0),
):
    """Update server info based on a message packet flag"""

    message_packet = json.loads(message_json)  # Decode and turn to dict in one step

    flag = message_packet["flag"]
    name = message_packet["name"]
    text = message_packet["text"]
    color = message_packet["color"]

    if flag == F_INFO:
        # Add new client info into appropriate lists
        connection.client_socs.append(client_soc)
        connection.client_ips.append(client_addr[0])

        # Broadcast that a new client has joined
        message_packet = create_message(
            F_MESSAGE, "Server", f"{name} has joined the server", LIGHT_GREEN
        )
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json)

        # Update server UI
        client_listbox.insert(END, f"Name: {name}        IP Addr: {client_addr[0]}")
        client_listbox.itemconfig(END, fg=color)

        # Now that a client has been established, start a thread to receive messages
        receive_thread = threading.Thread(
            target=receive_message,
            args=(
                connection,
                client_soc,
            ),
        )
        receive_thread.start()

    elif flag == F_MESSAGE:
        # A client has sent a message
        broadcast_message(connection, message_json)

        # Update Admin UI
        history_listbox.insert(0, f"{name}: {text}")
        history_listbox.itemconfig(0, fg=color)

    elif flag == F_DISCONNECT:
        # Close/Remove client socket
        index = connection.client_socs.index(client_soc)
        connection.client_socs.remove(client_soc)
        connection.client_ips.pop(index)
        client_listbox.delete(index)
        client_soc.close()

        # Alert all users that this client has left
        message_packet = create_message(
            F_MESSAGE, "Server:", f"{name} --- has left the server...", LIGHT_GREEN
        )
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json)

        # Update Admin UI
        history_listbox.insert(0, f"Server:, --- {name} --- has left the server...")

    else:
        # Catch for errors
        history_listbox.insert(0, "Error processing message")


def start_gui():
    """Put the GUI in to the connected mode"""

    # Clear the previous chat
    history_listbox.delete(0, END)
    client_listbox.delete(0, END)
    my_connection.reset_server()

    # Normal
    end_button.config(state=NORMAL)
    self_broadcast_button.config(state=NORMAL)
    message_button.config(state=NORMAL)
    kick_button.config(state=NORMAL)
    ban_button.config(state=NORMAL)

    # Disabled
    port_entry.config(state=DISABLED)
    start_button.config(state=DISABLED)


def end_gui():
    """Put The GUI in the disconnected mode"""

    # Disabled
    end_button.config(state=DISABLED)
    self_broadcast_button.config(state=DISABLED)
    message_button.config(state=DISABLED)
    kick_button.config(state=DISABLED)
    ban_button.config(state=DISABLED)

    # Normal
    port_entry.config(state=NORMAL)
    start_button.config(state=NORMAL)


def broadcast_message(connection: Connection, message_json: str):
    """Send a message to all connected clients..."""

    message_json_encoded = message_json.encode(connection.encoder)
    for client_soc in connection.client_socs:
        client_soc.send(message_json_encoded)


def receive_message(connection: Connection, client_soc: soc.socket):
    """Receive an incoming message from a client"""

    while True:
        try:
            # Get a message json from a client
            message_json = client_soc.recv(connection.bytesize).decode(
                connection.encoder
            )
            process_message(connection, message_json, client_soc)

        except:
            break


def on_closing():
    """Handles wat happens when the user presses the RED X button"""

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if my_connection.connected:
            end_server(my_connection)
        root.destroy()
        exit()


def self_broadcast(connection: Connection):
    """Broadcast a special admin message to all clients"""

    text = input_entry.get()

    if text == "":
        history_listbox.insert(0, "You cannot send nothing")
        return False

    # Create a message packet
    message_packet = create_message(F_MESSAGE, "Admin", text, LIGHT_GREEN)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json)
    history_listbox.insert(0, f"--- {text} ---")

    # Clear the entry field
    input_entry.delete(0, END)
    return True


def private_message(connection: Connection):
    """Send a private message to a specific client"""

    text = input_entry.get()

    if text == "":
        history_listbox.insert(0, "You cannot send nothing")
        return False

    # Select the client from the client listbox and access their socket
    index = client_listbox.curselection()[0]
    client_soc = connection.client_socs[index]

    # Create message packet
    message_packet = create_message(F_MESSAGE, "Admin (private)", text, LIGHT_GREEN)
    message_json = json.dumps(message_packet)

    client_soc.send(message_json.encode(connection.encoder))

    # Clear the entry field
    input_entry.delete(0, END)
    return True


def kick_client(connection: Connection):
    """Kick a given client off the server"""

    text = input_entry.get()

    if text == "":
        text = "You have been kicked"

    # Get the selected client socket
    index = client_listbox.curselection()[0]
    client_soc = connection.client_socs[index]

    # Create package
    message_packet = create_message(F_DISCONNECT, "Admin (private)", text, LIGHT_GREEN)
    message_json = json.dumps(message_packet)

    client_soc.send(message_json.encode(connection.encoder))


def ban_client(connection: Connection):
    """Ban a given client based on their IP address"""

    text = input_entry.get()

    if text == "":
        text = "You have been Baned"

    # Get the selected client socket
    index = client_listbox.curselection()[0]
    client_soc = connection.client_socs[index]
    client_ip = connection.client_ips[index]

    # Create package
    message_packet = create_message(F_DISCONNECT, "Admin (private)", text, LIGHT_GREEN)
    message_json = json.dumps(message_packet)

    client_soc.send(message_json.encode(connection.encoder))

    # Add the Ip to the Baned IP's
    connection.baned_ips.append(connection.client_ips[index])  # Turn off to debug


#### Def GUI layout ####
# Create Frames
connection_frame = tkinter.Frame(root, bg=BLACK)
history_frame = tkinter.Frame(root, bg=BLACK)
client_frame = tkinter.Frame(root, bg=BLACK)
message_frame = tkinter.Frame(root, bg=BLACK)
admin_frame = tkinter.Frame(root, bg=BLACK)

# Place the frames
connection_frame.pack(pady=5)
history_frame.pack()
client_frame.pack(pady=5)
message_frame.pack()
admin_frame.pack()


## Connection Frame layout ##
port_label = tkinter.Label(
    connection_frame, text="Port", font=my_font, fg=LIGHT_GREEN, bg=BLACK
)
port_entry = tkinter.Entry(connection_frame, width=10, borderwidth=3, font=my_font)
start_button = tkinter.Button(
    connection_frame,
    text="Start Server",
    font=my_font,
    borderwidth=5,
    width=15,
    bg=LIGHT_GREEN,
    command=lambda: start_server(my_connection),
)
end_button = tkinter.Button(
    connection_frame,
    text="End Server",
    font=my_font,
    borderwidth=5,
    width=15,
    bg=LIGHT_GREEN,
    state=DISABLED,
    command=lambda: end_server(my_connection),
)

# Place widgets
port_label.grid(row=0, column=0, padx=2, pady=10)
port_entry.grid(row=0, column=1, padx=2, pady=10)
start_button.grid(row=0, column=2, padx=5, pady=10)
end_button.grid(row=0, column=3, padx=5, pady=10)


## History Frame layout ##
history_scrollbar = tkinter.Scrollbar(history_frame, orient=VERTICAL)
history_listbox = tkinter.Listbox(
    history_frame,
    height=10,
    width=55,
    borderwidth=3,
    font=my_font,
    bg=BLACK,
    fg=LIGHT_GREEN,
    yscrollcommand=history_scrollbar.set,  # Link the listbox and scrollbar
)
history_scrollbar.config(
    command=history_listbox.yview  # Link the listbox and scrollbar
)

# Place widgets
history_listbox.grid(row=0, column=0)
history_scrollbar.grid(row=0, column=1, sticky="NS")


## Client Frame layout ##
client_scrollbar = tkinter.Scrollbar(client_frame, orient=VERTICAL)
client_listbox = tkinter.Listbox(
    client_frame,
    height=10,
    width=55,
    borderwidth=3,
    font=my_font,
    bg=BLACK,
    fg=LIGHT_GREEN,
    yscrollcommand=client_scrollbar.set,  # Link the listbox and scrollbar
)
client_scrollbar.config(command=client_listbox.yview)  # Link the listbox and scrollbar

# Place widgets
client_listbox.grid(row=0, column=0)
client_scrollbar.grid(row=0, column=1, sticky="NS")


## Message Frame layout ##
input_entry = tkinter.Entry(message_frame, width=40, borderwidth=3, font=my_font)
self_broadcast_button = tkinter.Button(
    message_frame,
    text="Broadcast",
    width=13,
    borderwidth=5,
    font=my_font,
    bg=LIGHT_GREEN,
    state=DISABLED,
    command=lambda: self_broadcast(my_connection),
)
root.bind("<Return>", lambda event: self_broadcast(my_connection))

# Place widgets
input_entry.grid(row=0, column=0, padx=5, pady=5)
self_broadcast_button.grid(row=0, column=1, padx=5, pady=5)


## Admin Frame layout ##
message_button = tkinter.Button(
    admin_frame,
    text="PM",
    font=my_font,
    borderwidth=5,
    width=15,
    bg=LIGHT_GREEN,
    state=DISABLED,
    command=lambda: private_message(my_connection),
)
kick_button = tkinter.Button(
    admin_frame,
    text="Kick",
    font=my_font,
    borderwidth=5,
    width=15,
    bg=LIGHT_GREEN,
    state=DISABLED,
    command=lambda: kick_client(my_connection),
)
ban_button = tkinter.Button(
    admin_frame,
    text="Ban",
    font=my_font,
    borderwidth=5,
    width=15,
    bg=LIGHT_GREEN,
    state=DISABLED,
    command=lambda: ban_client(my_connection),
)

# Place widgets
message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)

# Create a Connection object andRun the mainloop of the window
my_connection = Connection()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
