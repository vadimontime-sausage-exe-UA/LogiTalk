from email import message

from customtkinter import *
from socket import *
import threading
class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.title("Logitalk")
        self.resizable(False, False)

        self.is_show_menu = False
        self.chat_field = CTkScrollableFrame(self, width=520, height=310)
        self.chat_field.place(x=65, y=10)



        self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення:', width=450, height=40)
        self.message_entry.place(x=65, y=340)

        self.send_button = CTkButton(self, text='>', width=50, height=40, command=self.send_message)
        self.send_button.place(x=530, y=340)

        self.menu_frame = CTkFrame(self, width=50, height=400)
        self.menu_frame.place(x=0, y=0)
        self.menu_frame.pack_propagate(False)

        self.btn = CTkButton(self.menu_frame, text='▶️', command=self.toggle_menu, width=35)
        self.btn.place(x=7, y=10)

        self.menu_content = CTkFrame(self.menu_frame, width=180, height=330, fg_color="transparent")
        CTkLabel(self.menu_content, text='Імʼя:').pack(pady=(10, 5))
        self.username_entry = CTkEntry(self.menu_content, width=140)
        self.username_entry.pack(padx=10)
        self.clear_message = CTkButton(self.menu_content, command=self.clear_message, width=35, text="Очистити чат")
        self.clear_message.pack(pady=(20, 5))
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('4.tcp.eu.ngrok.io', 22283))
            thread = threading.Thread(target=self.recv_message).start()
        except Exception as e:
            self.add_message(f"Помилка підключення: {e}")

    def clear_message(self):
        def _update():
            for widget in self.chat_field.winfo_children():
                widget.destroy()

        self.after(0, _update)
    def toggle_menu(self):
        if self.is_show_menu:
            self.menu_content.place_forget()
            self.menu_frame.configure(width=50)
            self.btn.configure(text='▶️')
            self.is_show_menu = False
        else:
            self.menu_frame.configure(width=200)
            self.menu_content.place(x=10, y=50)
            self.btn.configure(text='◀️')
            self.is_show_menu = True
    def add_message(self, txt):
        def _update():
            msg_label = CTkLabel(self.chat_field, text=txt, anchor='nw', justify='left')
            msg_label.pack(fill = 'x', padx= 5, pady= 2)
        self.after(0, _update)
    def send_message(self):
        name = (self.username_entry.get().strip() or "User")
        message = (self.message_entry.get().strip())
        if message:
            full_text = f"{name}: {message}"
            self.add_message(f"Я: {message}")
            try:
                self.sock.send(bytes(full_text.encode()))
            except:
                pass
            self.message_entry.delete(0, 'end')
    def recv_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.add_message(message)
            except:
                break


win = MainWindow()
win.mainloop()