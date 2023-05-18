"""Client Side GUI Chat room"""
import socket as soc
import threading
import json
from sys import exit
from connection import exceptions
from connection.Client import Connection
from connection.locals import *
import tkinter
from tkinter import NORMAL, DISABLED, VERTICAL, END, messagebox, StringVar


## Def root window
root = tkinter.Tk()
root.title("GUI Chat Room")
root.geometry("600x600")
root.resizable(False, False)
root.config(bg=BLACK)


#### Def Func ####


def connect(connection: Connection):
    """Connect to a server at a given IP:Port address"""

    my_listbox.delete(0, END)  # Clear any previous chats

    connection.name = name_entry.get()
    connection.target_ip = ip_entry.get()
    connection.target_port = port_entry.get()
    connection.color = message_color.get()

    if connection.name == "":
        error_message = f"Name entry cannot be Empty when trying to connect"
        my_listbox.insert(0, error_message)
        print(error_message)

        return False

    try:
        # Create a client socket
        connection.client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        connection.client_soc.connect(
            (connection.target_ip, int(connection.target_port))
        )

        # Receive an incoming message packet from the server
        message_json = connection.client_soc.recv(connection.bytesize)
        process_message(connection, message_json)

        connection.connected = True

        return True

    except:
        error_message = f"Connection not established...goodbye"
        my_listbox.insert(0, error_message)
        print(error_message)

        return False


def disconnect(connection: Connection):
    """Disconnect the client from the server"""

    connection.connected = False

    # Create a disconnect packet
    message_packet = create_message(
        F_DISCONNECT, connection.name, "I am leaving", connection.color
    )
    message_json = json.dumps(message_packet)

    connection.client_soc.send(message_json.encode(connection.encoder))

    # Disable gui
    gui_end()


def gui_start():
    """Officially start connection by updating GUI"""

    # Normal
    disconnect_button.config(state=NORMAL)
    send_button.config(state=NORMAL)

    # Disabled
    name_entry.config(state=DISABLED)
    ip_entry.config(state=DISABLED)
    port_entry.config(state=DISABLED)
    connect_button.config(state=DISABLED)

    for button in color_buttons:
        button.config(state=DISABLED)


def gui_end():
    """Officially end connection by updating the GUI"""

    # Disables
    disconnect_button.config(state=DISABLED)
    send_button.config(state=DISABLED)

    # Normal
    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)
    connect_button.config(state=NORMAL)

    for button in color_buttons:
        button.config(state=NORMAL)


def create_message(flag, name, text, color):
    """Return a message packet to be sent"""

    message_packet = {
        "flag": flag,
        "name": name,
        "text": text,
        "color": color,
    }

    return message_packet


def process_message(connection: Connection, message_json: str | bytes):
    """Update the client based on the message packet flag"""

    # Unpack the json message
    message_packet = json.loads(message_json)

    flag = message_packet["flag"]
    name = message_packet["name"]
    text = message_packet["text"]
    color = message_packet["color"]

    if flag == F_INFO:
        # The Server is asking for info to verify connection
        message_packet = create_message(
            F_INFO, connection.name, "Joins the server!", connection.color
        )
        message_json = json.dumps(message_packet)
        connection.client_soc.send(message_json.encode(connection.encoder))

        # Enable the GUI
        gui_start()

        # Create thread to continuously receive messages from the server
        receive_thread = threading.Thread(target=receive_message, args=(connection,))
        receive_thread.start()

    elif flag == F_MESSAGE:
        # Server has sent a message to be displayed
        my_listbox.insert(0, f"{name}: {text}")
        my_listbox.itemconfig(0, fg=color)

    elif flag == F_DISCONNECT:
        # The server wants the client to disconnect
        my_listbox.insert(0, f"{name}: {text}")
        my_listbox.itemconfig(0, fg=color)

        disconnect(connection)

    else:
        # Catch any processing errors
        error_message = f"Error processing a message from the server..."
        my_listbox.insert(0, error_message)
        print(error_message)


def send_message(connection: Connection):
    """Send a message to the server"""

    if input_entry.get() == "":
        my_listbox.insert(0, "You can't send nothing")
        return False

    message_packet = create_message(
        F_MESSAGE, connection.name, input_entry.get(), connection.color
    )
    message_json = json.dumps(message_packet)
    connection.client_soc.send(message_json.encode(connection.encoder))

    # Clear the message entry field
    input_entry.delete(0, END)


def receive_message(connection: Connection):
    """Receive a message from the server"""

    while True:
        # Receive an incoming message
        try:
            # Receive an incoming json bytes object
            message_json = connection.client_soc.recv(connection.bytesize)
            process_message(connection, message_json)

        except:
            # Cannot receive message, close the connection and break
            my_listbox.insert(0, "Connection has been closed...goodbye")

            connection.client_soc.close()
            break


def on_closing():
    """Handles wat happens when the user presses the RED X button"""

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if my_connection.connected:
            disconnect(my_connection)
        root.destroy()
        exit()


#### Def GUI Layout ####
## Create frames
info_frame = tkinter.Frame(root, bg=BLACK)
color_frame = tkinter.Frame(root, bg=BLACK)
output_frame = tkinter.Frame(root, bg=BLACK)
input_frame = tkinter.Frame(root, bg=BLACK)

info_frame.pack()
color_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()


## Info Frame layout ##
name_label = tkinter.Label(
    info_frame, text="Client Name: ", font=my_font, fg=LIGHT_GREEN, bg=BLACK
)
name_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
ip_label = tkinter.Label(
    info_frame, text="IP Address", font=my_font, fg=LIGHT_GREEN, bg=BLACK
)
ip_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
port_label = tkinter.Label(
    info_frame, text="Port Num", font=my_font, fg=LIGHT_GREEN, bg=BLACK
)
port_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font, width=10)
connect_button = tkinter.Button(
    info_frame,
    text="Connect",
    font=my_font,
    bg=LIGHT_GREEN,
    borderwidth=5,
    width=10,
    command=lambda: connect(my_connection),
)
disconnect_button = tkinter.Button(
    info_frame,
    text="Disconnect",
    font=my_font,
    bg=LIGHT_GREEN,
    borderwidth=5,
    width=10,
    state=DISABLED,
    command=lambda: disconnect(my_connection),
)


name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)


## Color Frame layout ##
message_color = StringVar()
message_color.set(WHITE)

white_button = tkinter.Radiobutton(
    color_frame,
    width=5,
    text="White",
    variable=message_color,
    value=WHITE,
    bg=BLACK,
    fg=LIGHT_GREEN,
    font=my_font,
)
red_button = tkinter.Radiobutton(
    color_frame,
    width=5,
    text="Red",
    variable=message_color,
    value=RED,
    bg=BLACK,
    fg=LIGHT_GREEN,
    font=my_font,
)
orange_button = tkinter.Radiobutton(
    color_frame,
    width=5,
    text="Orange",
    variable=message_color,
    value=ORANGE,
    bg=BLACK,
    fg=LIGHT_GREEN,
    font=my_font,
)
yellow_button = tkinter.Radiobutton(
    color_frame,
    width=5,
    text="Yellow",
    variable=message_color,
    value=YELLOW,
    bg=BLACK,
    fg=LIGHT_GREEN,
    font=my_font,
)
blue_button = tkinter.Radiobutton(
    color_frame,
    width=5,
    text="Blue",
    variable=message_color,
    value=BLUE,
    bg=BLACK,
    fg=LIGHT_GREEN,
    font=my_font,
)
purple_button = tkinter.Radiobutton(
    color_frame,
    width=5,
    text="Purple",
    variable=message_color,
    value=PURPLE,
    bg=BLACK,
    fg=LIGHT_GREEN,
    font=my_font,
)
color_buttons = [
    white_button,
    red_button,
    orange_button,
    yellow_button,
    blue_button,
    purple_button,
]

white_button.grid(row=0, column=0, padx=2, pady=2)
red_button.grid(row=0, column=1, padx=2, pady=2)
orange_button.grid(row=0, column=2, padx=2, pady=2)
yellow_button.grid(row=0, column=3, padx=2, pady=2)
blue_button.grid(row=0, column=5, padx=2, pady=2)
purple_button.grid(row=0, column=6, padx=2, pady=2)


## Output Frame layout ##
my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(
    output_frame,
    height=20,
    width=55,
    borderwidth=3,
    bg=BLACK,
    fg=LIGHT_GREEN,
    font=my_font,
    yscrollcommand=my_scrollbar.set,
)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")


## Input Frame layout ##
input_entry = tkinter.Entry(input_frame, width=45, borderwidth=3, font=my_font)
send_button = tkinter.Button(
    input_frame,
    text="Send",
    font=my_font,
    borderwidth=5,
    width=10,
    bg=LIGHT_GREEN,
    state=DISABLED,
    command=lambda: send_message(my_connection),
)
root.bind("<Return>", lambda event: send_message(my_connection))

input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)


## Run the root windows mainloop()
# Create a Connection object andRun the mainloop of the window
my_connection = Connection()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
