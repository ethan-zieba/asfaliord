import datetime
import random
import tkinter as tk
import urllib.parse

from PIL import Image, ImageTk
from tkinter import ttk
import json
import threading

import credentials
from asfaliord.client import client


class MainInterfaceScreen(tk.Frame):
    def __init__(self, master, client):
        tk.Frame.__init__(self, master)
        master.bind("<Return>", self.get_message_input)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Vertical.TScrollbar",
                        background="#000F44",
                        troughcolor="#000F44",
                        arrowcolor="#04FF00",
                        bordercolor="#000F44",
                        gripcount=0,
                        gripbackground="#04FF00",
                        gripforeground="#7B61FF")

        custom_font = ('Classic Console Neue', 16)
        self.configure(bg="#292929")
        self.option_add("*Font", custom_font)
        self.client = client
        self.grid(row=0, column=0, sticky=tk.NSEW)

        # Logo in the top left corner
        self.left_frame()
        # Chat in the center
        self.center_frame()
        # Users list on the right
        self.right_frame()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=0)

        self.current_channel = 1
        self.dict_messages = {"1": ["Now - SYSTEM - Fetching all messages..."]}
        self.display_messages(self.dict_messages)

    def left_frame(self):
        logo_path = "assets/images/logo/asfaliord_logo.png"
        logo_image = Image.open(logo_path)
        logo_size = (150, int((logo_image.size[1] / logo_image.size[0]) * 150))
        self.logo = ImageTk.PhotoImage(logo_image.resize(logo_size))
        self.logo_label = tk.Label(self, image=self.logo, background="#292929")
        self.logo_label.grid(row=0, column=0, padx=10)

    def center_frame(self):
        self.middle_frame = tk.Frame(self, bg="#292929")
        self.middle_frame.grid(row=0, column=1, sticky="nsew", pady=10)
        self.middle_frame.grid_rowconfigure(0, weight=2)
        self.middle_frame.grid_columnconfigure(0, weight=2)
        self.chat_history = tk.Text(self.middle_frame, state="disabled", wrap="word",
                                    background="#000F44", foreground="#04FF00", font=("Classic Console Neue", 10))
        self.chat_history.grid(row=0, column=0, sticky="nsew")
        self.chat_history_scroll = ttk.Scrollbar(self.middle_frame, command=self.chat_history.yview, orient=tk.VERTICAL)
        self.chat_history_scroll.grid(row=0, column=1, sticky="ns")
        self.chat_history['yscrollcommand'] = self.chat_history_scroll.set
        self.input_field = tk.Entry(self.middle_frame, foreground='#04FF00', bg='#000F44')
        self.input_field.grid(row=1, column=0, sticky="ew", pady=10, padx=10)
        self.send_button = tk.Button(self.middle_frame, text="Send", command=self.get_message_input,
                                     background='#2937FF',
                                     foreground='#04FF00', activebackground='#4DC9FF', activeforeground='#04FF00')
        self.send_button.grid(row=1, column=1, pady=30)

    def right_frame(self):
        self.right_frame = tk.Frame(self, bg="#292929")
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=30)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.users_label = tk.Label(self.right_frame, text="Users", background="#000F44", foreground="#04FF00")
        self.users_label.grid(row=0, column=0, sticky=tk.EW, pady=1)
        self.user_list = tk.Listbox(self.right_frame, background="#000F44", foreground="#FF9C38")
        self.user_list.grid(row=1, column=0, sticky="nsew")
        self.user_list.bind("<<ListboxSelect>>", self.on_user_select)
        self.user_list_scroll = ttk.Scrollbar(self.right_frame, command=self.user_list.yview)
        self.user_list_scroll.grid(row=1, column=1, sticky="ns")
        self.user_list['yscrollcommand'] = self.user_list_scroll.set

    def on_user_select(self, event):
        index = self.user_list.curselection()
        if index:
            selected_user = self.user_list.get(index)
            self.input_field.insert(tk.END, selected_user)

    def get_message_input(self, event):
        message_to_send = self.input_field.get()
        self.input_field.delete(0, tk.END)
        threading.Thread(target=self.send_message_background_call(message_to_send)).start()

    def send_message_background_call(self, message_to_send):
        self.send_message_local(message_to_send)
        threading.Thread(target=lambda: self.client.send_message(message_to_send)).start()

    # Updates instantly when we send a message,
    # so we don't have to wait for the get_messages coroutine to see what we sent
    def send_message_local(self, message_sent):
        self.chat_history.config(state="normal")
        self.dict_messages[str(self.current_channel)].append(
            f"{datetime.date.today().strftime('%Y/%m/%d')} - {self.client.username}: {message_sent}")
        self.chat_history.insert(tk.END, f"{datetime.date.today().strftime('%Y/%m/%d')}", "date")
        self.chat_history.insert(tk.END, f" - {self.client.username}", "name")
        self.chat_history.insert(tk.END, f": {message_sent}\n")
        self.chat_history.config(state="disabled")

    def start_messages_coroutine(self):
        self.after(2000 + random.randint(1000, 3000), self.get_messages_coroutine)

    def get_messages_coroutine(self):
        threading.Thread(target=self.messages_background_call).start()
        print("Getting messages...")
        self.start_messages_coroutine()

    def messages_background_call(self):
        self.previous_dict_messages = self.dict_messages
        raw_messages = self.client.get_messages()
        self.dict_messages = json.loads(raw_messages)
        if self.dict_messages[str(self.current_channel)] != self.previous_dict_messages[str(self.current_channel)]:
            print("NEW MESSAGE: REFRESHING TEXT BOX")
            self.display_messages(self.dict_messages)
        else:
            print("NO NEW MESSAGE: NOT REFRESHING TEXT BOX")

    def display_messages(self, messages_dict):
        # Compare actual chat history with messages asked
        # If nothing new: stay the same
        self.chat_history.config(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.config(state="disabled")
        for message in messages_dict[str(self.current_channel)]:
            date, author, text = message.split(" - ")
            text = urllib.parse.unquote_plus(text)
            self.chat_history.config(state="normal")
            self.chat_history.insert(tk.END, date, "date")
            self.chat_history.insert(tk.END, f" - {author}", "name")
            self.chat_history.insert(tk.END, f": {text}\n")
            self.chat_history.tag_configure("name", foreground="#FF9C38")
            self.chat_history.tag_configure("date", foreground="#4AE4FF")
            self.chat_history.config(state="disabled")
            self.chat_history.see(tk.END)

    def get_channels(self):
        pass

    def display_channels(self, channels_list):
        # Creates a button for each channel, with the channel name and type
        pass

    def get_users(self):
        # Gets a tuple of (username, isConnected)
        pass

    def display_users(self, users_list):
        self.user_list.delete(0, "end")
        for user in users_list:
            self.user_list.insert(tk.END, user)

    def get_server_name(self):
        # Gets the server name when connecting to it
        pass

    def display_server_name(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_interface = MainInterfaceScreen(root, client.Client(credentials.tor_address))
    root.mainloop()