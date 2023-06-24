# Frontend for the R3DNET - a generic chat bot roleplaying a cyberpunk fixer (hacker)
# Version 2.0
# (c)2023.6 Krzysztof Krystian Jankowski

import os
import glob
import tkinter as tk
from tkinter import font as tkfont
from subprocess import Popen, PIPE
import threading

class SetupWindow:
    def __init__(self, master, app):
        self.master = master
        self.master.geometry('640x400')
        self.master.minsize(480, 360)
        self.master.title('R3DNET V2.0')
        self.master.config(bg='#000000')
        custom_font = tkfont.Font(family="Share Tech Mono", size=12)

        self.app = app
        self.master.withdraw()  # Hide the main window until setup is done


        self.setup_window = tk.Toplevel(self.master)
        self.setup_window.title("Setup")

        self.setup_window.config(bg='#000000')

        self.label_welcome = tk.Label(self.setup_window, text="Welcome to the P1X chatbot named R3DNET\n\nAI companion who seeks to understand and connect with others through meaningful conversation.")
        self.label_welcome.config(bg='#000000', fg='#cccccc', font=custom_font)
        self.label_welcome.pack(padx=32,pady=32)

        self.var_binary = tk.StringVar(self.setup_window)
        self.var_binary.set("./chatbot.sh")  # default value
        self.dropdown = tk.OptionMenu(self.setup_window, self.var_binary, "./chatbot.sh", "./chatbot-steamdeck.sh", "./chatbot-pi4.sh")
        self.dropdown.config(bg='#000000', fg='#cccccc', font=custom_font)
        self.dropdown.pack(padx=32,pady=32)

        self.model_files = glob.glob("./models/*.bin")
        if not self.model_files:
            self.label_no_model = tk.Label(self.setup_window, text="No model files found in /models/. Please download a model.")
            self.label_no_model.config(bg='#000000', fg='#cccccc', font=custom_font)
            self.label_no_model.pack()
        else:
            self.start_button = tk.Button(self.setup_window, text="Start", command=self.start)
            self.start_button.config(bg='#000000', fg='#cccccc', font=custom_font)
            self.start_button.pack()

        self.quit_button = tk.Button(self.setup_window, text="Quit", command=self.quit)
        self.quit_button.config(bg='#000000', fg='#cccccc', font=custom_font)
        self.quit_button.pack()

    def quit(self):
        self.setup_window.destroy()
        self.master.quit()

    def start(self):
        self.setup_window.destroy()
        self.master.deiconify()  # Show the main window
        self.app.start_chatbot(self.var_binary.get())

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry('640x400')
        self.master.minsize(480, 360)
        self.master.title('R3DNET V2.0')
        self.master.config(bg='#000000')

        custom_font = tkfont.Font(family="Share Tech Mono", size=15)

        self.text_area = tk.Text(master, font=custom_font, bd=0, height=14)
        self.text_area.pack(expand=True, fill='both', padx=64, pady=16)
        self.text_area.config(bg='#000000', fg='#cccccc')
        self.text_area.config(highlightbackground='#000000', highlightcolor='#000000')
        self.text_area.tag_config('user_input', foreground='#ffffff')
        self.text_area.tag_config('bot_input', foreground='#cccccc')

        self.entry = tk.Entry(master, font=custom_font, bd=0)
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack(side='bottom', fill='x', padx=64, pady=8)
        self.entry.config(bg='#000000', fg='#ffffff')
        self.entry.config(highlightbackground='#cccccc', highlightcolor='#cccccc')

        self.process = None
        self.thread = None
        SetupWindow(master, self)  # Display setup window

    def start_chatbot(self, binary_name):
        self.process = Popen(["stdbuf", "-o0", "./" + binary_name], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
        self.thread = threading.Thread(target=self.read_output, daemon=True)
        self.thread.start()

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if not message:
            return
        self.text_area.insert('end', message + '\n', 'user_input')
        self.text_area.see('end')
        self.process.stdin.write(bytes(message + '\n', 'utf-8'))
        self.process.stdin.flush()
        self.entry.delete(0, 'end')

    def read_output(self):
        while True:
            try:
                output = self.process.stdout.read(1).decode()
            except UnicodeDecodeError:
                continue
            if output == '' and self.process.poll() is not None:
                break
            if output:
                self.text_area.insert('end', output, 'bot_output')
                self.text_area.see('end')

root = tk.Tk()
app = ChatApp(root)
root.mainloop()
