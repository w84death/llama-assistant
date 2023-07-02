# Frontend for the P1X LLaMA Assistant
# Version 2.0
# (c)2023.6 Krzysztof Krystian Jankowski

import os
import io
import glob
import tkinter as tk
from tkinter import font as tkfont
from subprocess import Popen, PIPE
import subprocess
import threading
import datetime
from queue import Queue
import json
import base64
import requests
import argparse
from PIL import Image, ImageTk
import re

parser = argparse.ArgumentParser(description='P1X LLaMA  Assistant')
parser.add_argument('--ip', type=str, default='127.0.0.1', help='The IP of the Automatic1111 API endpoint')
args = parser.parse_args()

class SetupWindow:
    def __init__(self, master, app):

        with open('themes.json') as f:
            self.themes = json.load(f)

        self.master = master
        self.master.geometry('640x800')
        self.master.minsize(512, 640)
        self.master.title('P1X LLaMA Assistant')
        self.master.config(bg='#1e2229')
        self.custom_font = tkfont.Font(family="Share Tech Mono", size=12)

        self.app = app
        self.master.withdraw()  # Hide the main window until setup is done

        self.setup_window = tk.Toplevel(self.master)
        self.setup_window.geometry('512x640')
        self.setup_window.minsize(512, 640)
        self.setup_window.title("P1X LLaMA Assistant // Setup")
        self.setup_window.config(bg='#1e2229')

        self.header_image = tk.PhotoImage(file='header.png')
        header_label = tk.Label(self.setup_window, image=self.header_image)
        header_label.pack(pady=8)

        self.label_welcome = tk.Label(self.setup_window, text="Welcome to the P1X LLaMA Assistant\n\nUse [CTRL]+[S] to save the chat log.\n\nChoose the chatbot and theme:")
        self.label_welcome.config(bg='#1e2229', fg='#17a488', font=self.custom_font)
        self.label_welcome.pack(padx=32,pady=8)

        self.var_binary = tk.StringVar(self.setup_window)
        self.var_binary.set("./cyberpunk.sh")  # default value
        self.dropdown = tk.OptionMenu(self.setup_window, self.var_binary, "./cyberpunk.sh", "./chatbot.sh",  "./email.sh", "./chatbot-pi4.sh", "./chatbot-steamdeck.sh", "./email-steamdeck.sh")
        self.dropdown.config(bg='#1e2229', fg='#17a488', font=self.custom_font)
        self.dropdown.pack(padx=32,pady=4)

        self.theme_var = tk.StringVar(self.setup_window)
        self.theme_var.set("cyberpunk")  # default value
        self.theme_dropdown = tk.OptionMenu(self.setup_window, self.theme_var, *self.themes.keys())
        self.theme_dropdown.config(bg='#1e2229', fg='#17a488', font=self.custom_font)
        self.theme_dropdown.pack(padx=32,pady=4)

        self.model_files = glob.glob("./models/*.bin")
        if not self.model_files:
            self.label_no_model = tk.Label(self.setup_window, text="No model files found in /models/. Please download a model.")
            self.label_no_model.config(bg='#1e2229', fg='#aaa488', font=self.custom_font)
            self.label_no_model.pack(padx=32,pady=8)
        else:
            self.start_button = tk.Button(self.setup_window, text="Start", command=self.start, bd=0, activebackground='#47a349', activeforeground='#1e2229')
            self.start_button.config(bg='#1e2229', fg='#17a488', font=self.custom_font)
            self.start_button.pack(side='right', padx=32,pady=8)

        self.quit_button = tk.Button(self.setup_window, text="Quit", command=self.quit, bd=0, activebackground='#47a349', activeforeground='#1e2229')
        self.quit_button.config(bg='#1e2229', fg='#17a488', font=self.custom_font)
        self.quit_button.pack(side='left', padx=32,pady=8)

        self.app.audio_queue.put("Welcome to the PIX LLaMA Assistant")

    def quit(self):
        self.setup_window.destroy()
        self.master.quit()

    def start(self):
        self.setup_window.destroy()
        self.master.deiconify()  # Show the main window
        self.app.start_chatbot(self.var_binary.get(), self.themes[self.theme_var.get()])

class ChatApp:
    def __init__(self, master):
        self.image_generation = False
        self.read_enabled = False
        self.master = master
        self.master.geometry('640x800')
        self.master.minsize(512, 800)
        self.master.maxsize(512, 1920)
        self.master.title('P1X LLaMA Assistant')

        self.custom_font = tkfont.Font(family="Share Tech Mono", size=12)
        self.custom_font_banner = tkfont.Font(family="Share Tech Mono", size=80)

        self.image_label = tk.Label(master,text="(o.O)",font=self.custom_font_banner)
        self.image_label.pack(pady=8)

        self.text_area = tk.Text(master, font=self.custom_font, bd=0, height=10)
        self.text_area.tag_config('user_input', foreground='#47a349')
        self.text_area.tag_config('bot_input', foreground='#17a488')
        self.text_area.pack(expand=True, fill='both', padx=96, pady=4)

        self.send_return_button = tk.Button(master, text="Continue", command=self.send_return, font=self.custom_font, bd=0)
        self.send_return_button.pack(padx=96)

        self.entry = tk.Entry(master, font=self.custom_font, bd=0, width=100)
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack(side='bottom', fill='x', padx=96, pady=32)

        self.entry.focus_set()

        self.master.bind('<Control-s>', self.save_content)

        self.audio_queue = Queue()
        self.speak_thread()

        self.process = None
        self.thread = None
        SetupWindow(master, self)  # Display setup window

    def start_chatbot(self, binary_name, theme):
        self.master.config(bg=theme['bg_color'])
        self.text_area.config(bg=theme['bg_color'], fg=theme['fg_color'])
        self.entry.config(bg=theme['bg_color'], fg=theme['fg_color'])
        self.text_area.config(highlightbackground=theme['bg_color'], highlightcolor=theme['bg_color'], insertbackground=theme['fg_color'])
        self.entry.config(highlightbackground=theme['fg_color'], highlightcolor=theme['fg_color'], insertbackground=theme['fg_color'])
        self.send_return_button.config(bg=theme['bg_color'], fg=theme['fg_color'], activebackground=theme['fg_color'], activeforeground=theme['bg_color'])
        self.image_label.config(bg=theme['bg_color'], fg=theme['fg_color'])

        # self.generate_image("book cover, robot, ai, abstract")
        self.audio_queue.put("Loading LLaMA model...")
        self.process = Popen(["stdbuf", "-o0", "./" + binary_name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.thread = threading.Thread(target=self.read_output, daemon=True)
        self.thread.start()

    def extract_last_emoticon(self, chat_log):
        emoticon_pattern = r'\(([^)]+)\)'
        emoticons = re.findall(emoticon_pattern, chat_log)
        if emoticons:
            return "(" + emoticons[-1] + ")" # Return the last emoticon found
        else:
            return "( ^^ )"

    def process_chat_log(self, chat_log):
        last_emoticon = self.extract_last_emoticon(chat_log)
        return last_emoticon

    def toggle_reading(self):
        self.read_enabled = not self.read_enabled
        if self.read_enabled:
            self.read_button.config(text="Reading")
        else:
            self.read_button.config(text="Enable screen reader")

    def speak_thread(self):
        def run():
            while True:
                text = self.audio_queue.get().strip()
                if any(char.isalnum() for char in text):
                    subprocess.run(['spd-say', '-p', '-20', '-l', 'us', text])
                self.audio_queue.task_done()

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
        description_tag_open = "[image_prompt]"
        description_tag_close = "[end]"
        capture_description = False
        description_text = ""
        buffer = ""
        tag_buffer = ""

        while True:
            try:
                output = self.process.stdout.read(1).decode()
            except UnicodeDecodeError:
                continue
            if output == '' and self.process.poll() is not None:
                break
            if output:
                if not self.image_generation and "Voice enabled." in self.text_area.get("1.0", 'end'):
                    self.image_generation = True
                    self.read_enabled = True

                if self.read_enabled:
                    buffer += output
                    if output == '\n' or output == '.' or output == '?' or output == '!':
                        buffer = buffer.replace("Computer: ", "", 1)
                        self.audio_queue.put(buffer)
                        buffer = ''
                        self.image_label.config(text=self.process_chat_log( self.text_area.get("1.0", tk.END)))

                self.text_area.insert('end', output, 'bot_output')
                self.text_area.see('end')

                if self.image_generation:
                    tag_buffer += output
                    if capture_description:
                        description_text += output
                        if description_tag_close in description_text:
                            description_text = description_text.replace(description_tag_open, "").replace(description_tag_close, "")
                            self.generate_image(description_text.strip())
                            capture_description = False
                            self.read_enabled = True
                            description_text = ''
                            buffer = ''
                            tag_buffer = ''
                    else:
                        if description_tag_open in tag_buffer:
                            capture_description = True
                            self.read_enabled = False


    def generate_image(self, prompt):
        print("GENERATE IMAGE... " + prompt)
        prompt_preffix = "Cyberpunk concept art of "
        prompt_suffix = ". cinematic lighting, details, award winning. <lora:CyberPunkAI:0.2> CyberPunkAI"
        model = ""
        payload = {
            "prompt": prompt_preffix + prompt + prompt_suffix,
            "sampling_method": "other_method",
            "model": "deliberate_v2.safetensors",
            "sampling_method": "Euler a",
            "steps": 24,
            "cfg_scale": 5,
            "width": 1024,
            "height":512
        }
        def send_request():
            response = requests.post(url=f'http://{args.ip}:7860/sdapi/v1/txt2img', json=payload)
            r = response.json()
            for i in r['images']:
                image_data = i
                if "," in i:
                    image_data = i.split(",", 1)[1]
                image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                width, height = image.size
                image = image.resize((int(width*0.5), int(height*0.5)), Image.LANCZOS)

                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo

        thread = threading.Thread(target=send_request)
        thread.start()


    def save_content(self, event=None):
        content = self.text_area.get('1.0', 'end-1c')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f'chatlog_{timestamp}.txt', 'w') as f:
            f.write(content)
        self.text_area.insert('end', '\n> Chat log saved to chatlog_'+timestamp+'.txt\n', 'user_input')


root = tk.Tk()
app = ChatApp(root)
root.mainloop()
