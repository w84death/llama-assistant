# Frontend for the P1X LLaMA Assistant
# Version 2.0
# (c)2023.6 Krzysztof Krystian Jankowski

import os
import glob
import tkinter as tk
from tkinter import font as tkfont
from subprocess import Popen, PIPE
import threading
import datetime
from gtts import gTTS
import os
from queue import Queue

class SetupWindow:
    def __init__(self, master, app):
        self.master = master
        self.master.geometry('640x800')
        self.master.minsize(480, 640)
        self.master.title('P1X LLaMA Assistant')
        self.master.config(bg='#1e2229')
        custom_font = tkfont.Font(family="Share Tech Mono", size=12)

        self.app = app
        self.master.withdraw()  # Hide the main window until setup is done

        self.setup_window = tk.Toplevel(self.master)
        self.setup_window.geometry('640x480')
        self.setup_window.minsize(640, 480)
        self.setup_window.title("P1X LLaMA Assistant // Setup")
        self.setup_window.config(bg='#1e2229')

        self.header_image = tk.PhotoImage(file='header.png')
        header_label = tk.Label(self.setup_window, image=self.header_image)
        header_label.pack(pady=8)

        self.label_welcome = tk.Label(self.setup_window, text="Welcome to the P1X LLaMA Assistant\n\nUse [CTRL]+[S] to save the chat log.\n\nChoose the chatbot:")
        self.label_welcome.config(bg='#1e2229', fg='#17a488', font=custom_font)
        self.label_welcome.pack(padx=32,pady=8)

        self.var_binary = tk.StringVar(self.setup_window)
        self.var_binary.set("./cyberpunk.sh")  # default value
        self.dropdown = tk.OptionMenu(self.setup_window, self.var_binary, "./cyberpunk.sh", "./chatbot.sh",  "./email.sh", "./chatbot-pi4.sh", "./chatbot-steamdeck.sh", "./email-steamdeck.sh")
        self.dropdown.config(bg='#1e2229', fg='#17a488', font=custom_font)
        self.dropdown.pack(padx=32,pady=4)

        self.model_files = glob.glob("./models/*.bin")
        if not self.model_files:
            self.label_no_model = tk.Label(self.setup_window, text="No model files found in /models/. Please download a model.")
            self.label_no_model.config(bg='#1e2229', fg='#aaa488', font=custom_font)
            self.label_no_model.pack(padx=32,pady=8)
        else:
            self.start_button = tk.Button(self.setup_window, text="Start", command=self.start, bd=0, activebackground='#47a349', activeforeground='#1e2229')
            self.start_button.config(bg='#1e2229', fg='#17a488', font=custom_font)
            self.start_button.pack(side='right', padx=32,pady=8)

        self.quit_button = tk.Button(self.setup_window, text="Quit", command=self.quit, bd=0, activebackground='#47a349', activeforeground='#1e2229')
        self.quit_button.config(bg='#1e2229', fg='#17a488', font=custom_font)
        self.quit_button.pack(side='left', padx=32,pady=8)

        self.app.queue.put("Welcome to the P1X LLaMA Assistant")

    def quit(self):
        self.setup_window.destroy()
        self.master.quit()

    def start(self):
        self.setup_window.destroy()
        self.master.deiconify()  # Show the main window
        self.app.start_chatbot(self.var_binary.get())

class ChatApp:
    def __init__(self, master):
        self.read_enabled = False
        self.master = master
        self.master.geometry('640x800')
        self.master.minsize(480, 640)
        self.master.title('P1X LLaMA Assistant')
        self.master.config(bg='#1e2229')

        custom_font = tkfont.Font(family="Share Tech Mono", size=12)

        self.text_area = tk.Text(master, font=custom_font, bd=0)
        self.text_area.pack(expand=True, fill='both', padx=128, pady=32)
        self.text_area.config(bg='#1e2229', fg='#17a488')
        self.text_area.config(highlightbackground='#1e2229', highlightcolor='#1e2229', insertbackground='#47a349')
        self.text_area.tag_config('user_input', foreground='#47a349')
        self.text_area.tag_config('bot_input', foreground='#17a488')

        self.send_return_button = tk.Button(master, text="Continue", command=self.send_return, font=custom_font, bd=0, activebackground='#47a349', activeforeground='#1e2229')
        self.send_return_button.config(bg='#1e2229', fg='#47a349')
        self.send_return_button.pack(padx=128)

        self.entry = tk.Entry(master, font=custom_font, bd=0, width=100)
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack(side='bottom', fill='x', padx=128, pady=32)
        self.entry.config(bg='#1e2229', fg='#47a349')
        self.entry.config(highlightbackground='#17a488', highlightcolor='#17a488', insertbackground='#47a349')

        self.entry.focus_set()

        self.master.bind('<Control-s>', self.save_content)

        self.read_button = tk.Button(master, text="Read", command=self.toggle_reading, font=custom_font, bd=0, activebackground='#47a349', activeforeground='#1e2229')
        self.read_button.config(bg='#1e2229', fg='#47a349')
        self.read_button.pack(side='left', padx=32)

        self.queue = Queue()
        self.speak_thread()

        self.process = None
        self.thread = None
        SetupWindow(master, self)  # Display setup window

    def start_chatbot(self, binary_name):
        self.process = Popen(["stdbuf", "-o0", "./" + binary_name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.thread = threading.Thread(target=self.read_output, daemon=True)
        self.thread.start()

    def toggle_reading(self):
        self.read_enabled = not self.read_enabled

    def speak_thread(self):
        def run():
            import tempfile
            while True:
                text = self.queue.get()
                if text:
                    tts = gTTS(text=text, lang='en')
                    temp_filename = tempfile.mktemp(suffix=".mp3")
                    tts.save(temp_filename)
                    os.system(f"mpg123 {temp_filename}")
                    os.remove(temp_filename)
                self.queue.task_done()

        thread = threading.Thread(target=run)
        thread.start()

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
        buffer = ''
        while True:
            try:
                output = self.process.stdout.read(1).decode()
            except UnicodeDecodeError:
                continue
            if output == '' and self.process.poll() is not None:
                break
            if output:
                if self.read_enabled:
                    buffer += output
                    if output == '\n' or output == '.':
                        self.queue.put(buffer)
                        buffer = ''
                self.text_area.insert('end', output, 'bot_output')
                self.text_area.see('end')

    def save_content(self, event=None):
        content = self.text_area.get('1.0', 'end-1c')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f'chatlog_{timestamp}.txt', 'w') as f:
            f.write(content)
        self.text_area.insert('end', '\n> Chat log saved to chatlog_'+timestamp+'.txt\n', 'user_input')


root = tk.Tk()
app = ChatApp(root)
root.mainloop()
