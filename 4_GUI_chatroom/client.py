"""Client Side GUI Chat room"""
import tkinter
import threading
import socket as soc
from tkinter import NORMAL, DISABLED, VERTICAL, END


## Def root window
root = tkinter.Tk()
root.title("GUI Chat Room")
root.iconbitmap("4_GUI_chatroom/icon.ico")
root.geometry("600x600")
root.resizable(False, False)


## Def fonts and colors
my_font = ("SimSun", 14)
BLACK = "#010101"
LIGHT_GREEN = "#1fc742"
root.config(bg=BLACK)


## Def socket const vars ##
ENCODER = "utf-8"
BYTESIZE = 1024
client_soc: soc.socket


#### Def Func ####


def connect():
    """Connect to a server at a given IP:Port address"""

    global client_soc

    ## Clear any previous chats
    my_listbox.delete(0, END)

    ## Get the required connection info
    name = name_entry.get()
    ip = ip_entry.get()
    port = port_entry.get()

    ## Only if all required info is available try to connect
    if name and ip and port:
        ## Conditions for connection are met, try for connection
        my_listbox.insert(0, f"{name} --- is waiting to connect to {ip}:{port}...")

        ## Create a client socket IPv4 and TCP
        client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        client_soc.connect((ip, int(port)))

        ## Verify that the connection is valid
        verify_connection(name)

    else:
        ## Conditions to attempt a connection where not met
        my_listbox.insert(0, "Insufficient information given for connection...")


def verify_connection(name: str):
    """Verify that the server connection is valid and pass required info"""

    ## The server will send a '@_NAME' flag if a valid connection was made
    flag = client_soc.recv(BYTESIZE).decode(ENCODER)

    if flag == "@_NAME":
        ## The connection was made, send the client name and wait for verification
        client_soc.send(name.encode(ENCODER))

        message = client_soc.recv(BYTESIZE).decode(ENCODER)

        if message:
            ## Server sent a verification, connection is valid
            my_listbox.insert(0, message)

            ## Change the buttons/entry states
            connect_button.config(state=DISABLED)
            disconnect_button.config(state=NORMAL)
            send_button.config(state=NORMAL)

            name_entry.config(state=DISABLED)
            ip_entry.config(state=DISABLED)
            port_entry.config(state=DISABLED)

            ## Create a thread to receive messages from the server
            receive_thread = threading.Thread(target=receive_message)
            receive_thread.start()

        else:
            ## No verification message was received
            my_listbox.insert(0, "Connection not verified. Goodbye...")
            client_soc.close()

    else:
        ## Did not receive a '@_NAME' flag
        my_listbox.insert(0, "Connection refused, Goodbye...")
        client_soc.close()


def disconnect():
    """Disconnect from the server"""

    ## Close the client socket
    client_soc.close()

    ## Change the buttons/entry states
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)
    send_button.config(state=DISABLED)

    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)


def send_message():
    """Send a message to the server to be broadcast"""

    ## Send the message to the server
    message = input_entry.get()
    client_soc.send(message.encode(ENCODER))

    ## Clear the entry field
    input_entry.delete(0, END)


def receive_message():
    """Receive an incoming message from the server"""

    while True:
        try:
            ## Receive an incoming message
            message = client_soc.recv(BYTESIZE).decode(ENCODER)

            ## Show the message to the client
            my_listbox.insert(0, message)

        except:
            ## "Don't Know what the error is
            error_message = "An error in the receive_thread"
            my_listbox.insert(0, error_message)
            print(error_message)

            disconnect()
            break


#### Def GUI Layout ####
## Create frames
info_frame = tkinter.Frame(root, bg=BLACK)
output_frame = tkinter.Frame(root, bg=BLACK)
input_frame = tkinter.Frame(root, bg=BLACK)

info_frame.pack()
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
    command=connect,
)
disconnect_button = tkinter.Button(
    info_frame,
    text="Disconnect",
    font=my_font,
    bg=LIGHT_GREEN,
    borderwidth=5,
    width=10,
    state=DISABLED,
    command=disconnect,
)


name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)


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
    command=send_message,
)

input_entry.grid(row=0, column=0, padx=5, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)


## Run the root windows mainloop()
root.mainloop()
