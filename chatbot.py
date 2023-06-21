# Frontend for the R3DNET - a generic chat bot roleplaying a cyberpunk fixer (hacker)
# Version 1.0
# (c)2023.6 Krzysztof Krystian Jankowski

import tkinter as tk
from tkinter import font as tkfont
from subprocess import Popen, PIPE
import threading

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry('480x640')
        self.master.minsize(480, 640)
        self.master.title('R3DNET V1.0')
        self.master.config(bg='#f5f5dc')

        custom_font = tkfont.Font(family="Georgia", size=12)

        self.text_area = tk.Text(master, font=custom_font, bd=0)
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)
        self.text_area.config(bg='#f5f5dc', fg='#556b2f')
        self.text_area.config(highlightbackground='#f5f5dc', highlightcolor='#f5f5dc')

        self.entry = tk.Entry(master, font=custom_font, bd=2)
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack(side='bottom', fill='x', padx=10, pady=10)
        self.entry.config(bg='#f5f5dc', fg='#8b4513')
        self.entry.config(highlightbackground='#8b4513', highlightcolor='#8b4513')

        self.process = Popen(["stdbuf", "-o0", "./chatbot.sh"], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
        self.thread = threading.Thread(target=self.read_output, daemon=True)
        self.thread.start()
        self.text_area.tag_config('user_input', foreground='#8b4513')
        self.text_area.tag_config('bot_input', foreground='#8b4513')

    def send_message(self, event=None):
        message = self.entry.get()
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
