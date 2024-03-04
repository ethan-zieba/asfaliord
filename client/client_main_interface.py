import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk


class MainInterfaceScreen(tk.Frame):
    def __init__(self, master, client):
        tk.Frame.__init__(self, master)
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

        # Logo in the top left corner
        logo_path = "assets/images/logo/asfaliord_logo.png"
        logo_image = Image.open(logo_path)
        logo_size = (150, int((logo_image.size[1] / logo_image.size[0]) * 150))
        self.logo = ImageTk.PhotoImage(logo_image.resize(logo_size))
        self.logo_label = tk.Label(self, image=self.logo, background="#292929")
        self.logo_label.grid(row=0, column=0, padx=10)

        # Chat in the center
        self.middle_frame = tk.Frame(self, bg="#292929")
        self.middle_frame.grid(row=0, column=1, sticky=tk.NSEW, pady=10)
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.chat_history = tk.Text(self.middle_frame, state="disabled", wrap="word",
                                    background="#292929", foreground="#04FF00")
        self.chat_history.grid(row=0, column=0, sticky="nsew")
        self.chat_history_scroll = ttk.Scrollbar(self.middle_frame, command=self.chat_history.yview, orient=tk.VERTICAL)
        self.chat_history_scroll.grid(row=0, column=1, sticky="ns")
        self.chat_history['yscrollcommand'] = self.chat_history_scroll.set
        self.input_field = tk.Entry(self.middle_frame, foreground='#04FF00', bg='#000F44')
        self.input_field.grid(row=1, column=0, sticky="ew", pady=10, padx=10)
        self.send_button = tk.Button(self.middle_frame, text="Send", background='#2937FF',
                                      foreground='#04FF00', activebackground='#4DC9FF', activeforeground='#04FF00')
        self.send_button.grid(row=1, column=1, pady=30)

        # Users list on the right
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

    def on_user_select(self, event):
        index = self.user_list.curselection()
        if index:
            selected_user = self.user_list.get(index)
            self.input_field.insert(tk.END, selected_user)

    def display_messages(self, messages_list):
        for message in messages_list:
            date, author, text = message.split(" - ")
            self.chat_history.config(state="normal")
            self.chat_history.insert(tk.END, date, "date")
            self.chat_history.insert(tk.END, f" - {author}", "name")
            self.chat_history.insert(tk.END, f": {text}\n")
            self.chat_history.tag_configure("name", foreground="#FF9C38")
            self.chat_history.tag_configure("date", foreground="#4AE4FF")
            self.chat_history.config(state="disabled")
            self.chat_history.see(tk.END)

    def display_users(self, users_list):
        self.user_list.delete(0, "end")
        for user in users_list:
            self.user_list.insert(tk.END, user)
