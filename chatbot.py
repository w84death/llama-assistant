import tkinter as tk
from subprocess import Popen, PIPE
import threading

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry('480x640')
        self.master.title('Chat with P1XBOT')

        self.text_area = tk.Text(master)
        self.text_area.pack()

        self.entry = tk.Entry(master)
        self.entry.bind("<Return>", self.send_message)
        self.entry.pack()

        self.process = Popen(["stdbuf", "-o0", "./chatbot.sh"], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
        self.thread = threading.Thread(target=self.read_output, daemon=True)
        self.thread.start()

    def send_message(self, event=None):
        message = self.entry.get()
        self.text_area.insert('end', "You: " + message + '\n')
        self.text_area.see('end')
        self.process.stdin.write(bytes(message + '\n', 'utf-8'))
        self.process.stdin.flush()
        self.entry.delete(0, 'end')

    def read_output(self):
        while True:
            output = self.process.stdout.read(1).decode()
            if output == '' and self.process.poll() is not None:
                break
            if output:
                self.text_area.insert('end', output)
                self.text_area.see('end')


root = tk.Tk()
app = ChatApp(root)
root.mainloop()
