import customtkinter
import tkinter
from tkinter import messagebox
import subprocess
from screen3 import CreateUser
from config_values import *


class Login:
    def __init__(self):
        self.current_username = ""
        self.current_password = ""

        customtkinter.set_appearance_mode(BACKGROUND_COLOR)
        customtkinter.set_default_color_theme(DEFAULT_COLOR_THEME)

        self.load_credentials()

        self.app = customtkinter.CTk()
        self.app.title("Asfaliord - Login")
        self.app.geometry(WINDOW_SIZE)

        # Logo (Same as before)

        # Login Section
        self.login_label = customtkinter.CTkLabel(self.app, text="Login", font=LOGIN_TITLE_FONT)
        self.login_label.grid(row=1, column=0, columnspan=2, pady=LABEL_PADY)

        self.username_label = customtkinter.CTkLabel(self.app, text="Username:", font=DEFAULT_FONT)
        self.username_label.grid(row=2, column=0, pady=ENTRY_PADY)

        self.username_entry = customtkinter.CTkEntry(self.app, font=DEFAULT_FONT)
        self.username_entry.grid(row=2, column=1, pady=ENTRY_PADY)

        self.password_label = customtkinter.CTkLabel(self.app, text="Password:", font=DEFAULT_FONT)
        self.password_label.grid(row=3, column=0, pady=ENTRY_PADY)

        self.password_entry = customtkinter.CTkEntry(self.app, show="*", font=DEFAULT_FONT)
        self.password_entry.grid(row=3, column=1, pady=ENTRY_PADY)

        self.login_button = customtkinter.CTkButton(master=self.app, text="Login", command=self.authenticate, font=DEFAULT_FONT)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=BUTTON_PADY)

        self.login_success_label = customtkinter.CTkLabel(self.app, text="Login Successful!", font=DEFAULT_FONT, fg_color=LOGIN_SUCCESS_COLOR)
        self.login_success_label.grid(row=5, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        self.login_success_label.grid_remove()

        self.login_failed_label = customtkinter.CTkLabel(self.app, text="Login Failed. Please try again.", font=DEFAULT_FONT, fg_color=LOGIN_FAILED_COLOR)
        self.login_failed_label.grid(row=5, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        self.login_failed_label.grid_remove()

        self.create_account_button = customtkinter.CTkButton(master=self.app, text="Create Account", command=self.open_create_account, font=DEFAULT_FONT)
        self.create_account_button.grid(row=6, column=0, columnspan=2, pady=CREATE_ACCOUNT_BUTTON_PADY)

        logo_path = "asfaliord.png"  
        logo_image = tkinter.PhotoImage(file=logo_path).subsample(15,15)
        logo_label = tkinter.Label(self.app, image=logo_image)
        logo_label.grid(row=0, column=00, pady=LABEL_PADY)
        

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username and password match
        if username == self.current_username and password == self.current_password:
            self.login_success_label.grid(row=5, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        else:
            self.login_failed_label.grid(row=5, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)

    def open_create_account(self):
        # Create an instance of the CreateUser class and pass the Login instance
        create_account_instance = CreateUser(self)

    def open_login_screen(self):
        # Close the current window
        self.app.destroy()

        # Launch the Login screen from screen2.py
        subprocess.run(["python", "screen2.py"])

    def load_credentials(self):
        try:
            with open("credentials.txt", "r") as file:
                lines = file.readlines()
                if len(lines) == 2:
                    self.current_username = lines[0].strip()
                    self.current_password = lines[1].strip()
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.app.destroy()

# Create an instance of the Login class
login_instance = Login()
