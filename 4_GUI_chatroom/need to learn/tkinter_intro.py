## Tkinter introduction
import tkinter
from tkinter import BOTH, StringVar, END


## Def window
root = tkinter.Tk()
root.title("let's Chat")
root.iconbitmap("4_GUI_chatroom/need to learn/icon.ico")
root.geometry("400x600")
root.resizable(0, 0)


## Def colors
root_color = "#535657"
input_color = "#4f646f"
output_color = "#dee7e7"
root.config(bg=root_color)


## Def func


def send_message():
    """Send the users message to the output frame"""

    message_label = tkinter.Label(
        output_frame, text=message_entry.get(), fg=text_color.get(), bg=output_color, font=("Helvetica", 12)
    )
    message_label.pack()

    # Clear the entry field for next message
    message_entry.delete(0, END)


###### Def GUI Layout ######
## Def frames
input_frame = tkinter.LabelFrame(root, bg=input_color)
output_frame = tkinter.LabelFrame(root, bg=output_color)
input_frame.pack(pady=10)
output_frame.pack(padx=10, pady=(0, 10), fill=BOTH, expand=True)

## Def widgets
# Input bar
message_entry = tkinter.Entry(input_frame, text="Enter a message: ", width=25, font=("Helvetica", 12))
send_button = tkinter.Button(input_frame, text="Send", command=send_message, bg=output_color)
message_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
send_button.grid(row=0, column=3, rowspan=2, padx=10, pady=10, ipadx=20, ipady=5)

text_color = StringVar()
text_color.set("#0000ff")
red_button = tkinter.Radiobutton(input_frame, text="Red", variable=text_color, value="#ff0000", bg=input_color)
green_button = tkinter.Radiobutton(input_frame, text="Green", variable=text_color, value="#00ff00", bg=input_color)
blue_button = tkinter.Radiobutton(input_frame, text="Blue", variable=text_color, value="#0000ff", bg=input_color)

red_button.grid(row=1, column=0)
green_button.grid(row=1, column=1)
blue_button.grid(row=1, column=2)

# Output stream
output_label = tkinter.Label(
    output_frame, text="--- Stored Messages ---", fg=input_color, bg=output_color, font=("Helvetica bold", 18)
)
output_label.pack(pady=15)


## Run the root window's mainloop()
root.mainloop()
