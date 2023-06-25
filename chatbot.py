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
        self.master.geometry('800x640')
        self.master.minsize(480, 640)
        self.master.title('LLaMA Assistant')
        self.master.config(bg='#1e2229')
        custom_font = tkfont.Font(family="Share Tech Mono", size=12)

        self.app = app
        self.master.withdraw()  # Hide the main window until setup is done


        self.setup_window = tk.Toplevel(self.master)
        self.setup_window.title("Setup")

        self.setup_window.config(bg='#1e2229')

        self.label_welcome = tk.Label(self.setup_window, text="Welcome to the P1X LLaMA Assistant\n\nChoose the chatbot.")
        self.label_welcome.config(bg='#1e2229', fg='#17a488', font=custom_font)
        self.label_welcome.pack(padx=32,pady=32)

        self.var_binary = tk.StringVar(self.setup_window)
        self.var_binary.set("./chatbot.sh")  # default value
        self.dropdown = tk.OptionMenu(self.setup_window, self.var_binary, "./cyberpunk.sh", "./chatbot.sh", "./chatbot-steamdeck.sh", "./chatbot-pi4.sh")
        self.dropdown.config(bg='#1e2229', fg='#17a488', font=custom_font)
        self.dropdown.pack(padx=32,pady=32)

        self.model_files = glob.glob("./models/*.bin")
        if not self.model_files:
            self.label_no_model = tk.Label(self.setup_window, text="No model files found in /models/. Please download a model.")
            self.label_no_model.config(bg='#1e2229', fg='#aaa488', font=custom_font)
            self.label_no_model.pack(padx=32,pady=8)
        else:
            self.start_button = tk.Button(self.setup_window, text="Start", command=self.start)
            self.start_button.config(bg='#1e2229', fg='#17a488', font=custom_font)
            self.start_button.pack(padx=32,pady=8)

        self.quit_button = tk.Button(self.setup_window, text="Quit", command=self.quit)
        self.quit_button.config(bg='#1e2229', fg='#17a488', font=custom_font)
        self.quit_button.pack(padx=32,pady=8)

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
        self.master.geometry('800x640')
        self.master.minsize(480, 640)
        self.master.title('R3DNET V2.1')
        self.master.config(bg='#1e2229')

        custom_font = tkfont.Font(family="Share Tech Mono", size=12)

        self.text_area = tk.Text(master, font=custom_font, bd=0)
        self.text_area.pack(expand=True, fill='both', padx=128, pady=32)
        self.text_area.config(bg='#1e2229', fg='#17a488')
        self.text_area.config(highlightbackground='#1e2229', highlightcolor='#1e2229', insertbackground='#47a349')
        self.text_area.tag_config('user_input', foreground='#47a349')
        self.text_area.tag_config('bot_input', foreground='#17a488')

        self.send_return_button = tk.Button(master, text="Continue", command=self.send_return)
        self.send_return_button.config(bg='#1e2229', fg='#47a349')
        self.send_return_button.pack(padx=128)

        self.entry = tk.Entry(master, font=custom_font, bd=0, width=100)
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack(side='bottom', fill='x', padx=128, pady=32)
        self.entry.config(bg='#1e2229', fg='#47a349')
        self.entry.config(highlightbackground='#17a488', highlightcolor='#17a488', insertbackground='#47a349')

        self.process = None
        self.thread = None
        SetupWindow(master, self)  # Display setup window

    def start_chatbot(self, binary_name):
        self.process = Popen(["stdbuf", "-o0", "./" + binary_name], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
        self.thread = threading.Thread(target=self.read_output, daemon=True)
        self.thread.start()

    def send_return(self):
        if self.process is not None and self.process.poll() is None:
            self.process.stdin.write(b'\n')
            self.process.stdin.flush()

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
