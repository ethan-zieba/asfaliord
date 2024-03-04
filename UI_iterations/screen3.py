import customtkinter
import tkinter
from config_values import *

class CreateUser:
    def __init__(self, login_instance):
        self.current_username = ""
        self.current_password = ""
        self.login_instance = login_instance

        customtkinter.set_appearance_mode(BACKGROUND_COLOR)
        customtkinter.set_default_color_theme(DEFAULT_COLOR_THEME)

        self.app = customtkinter.CTk()
        self.app.title("Asfaliord - Create Account")
        self.app.geometry(WINDOW_SIZE)

        self.account_creation_label = customtkinter.CTkLabel(self.app, text="Create an Account", font=LOGIN_TITLE_FONT)
        self.account_creation_label.grid(row=1, column=0, columnspan=2, pady=LABEL_PADY)

        self.new_username_label = customtkinter.CTkLabel(self.app, text="New Username:", font=DEFAULT_FONT)
        self.new_username_label.grid(row=2, column=0, pady=ENTRY_PADY)

        self.new_username_entry = customtkinter.CTkEntry(self.app, font=DEFAULT_FONT)
        self.new_username_entry.grid(row=2, column=1, pady=ENTRY_PADY)

        self.new_password_label = customtkinter.CTkLabel(self.app, text="New Password:", font=DEFAULT_FONT)
        self.new_password_label.grid(row=3, column=0, pady=ENTRY_PADY)

        self.new_password_entry = customtkinter.CTkEntry(self.app, show="*", font=DEFAULT_FONT)
        self.new_password_entry.grid(row=3, column=1, pady=ENTRY_PADY)

        self.create_account_button = customtkinter.CTkButton(master=self.app, text="Create Account",
                                                              command=self.create_account, font=DEFAULT_FONT)
        self.create_account_button.grid(row=4, column=0, columnspan=2, pady=BUTTON_PADY)

        self.account_created_label = customtkinter.CTkLabel(self.app, text="Account Created Successfully!",
                                                             font=DEFAULT_FONT)
        self.account_created_label.grid(row=5, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        self.account_created_label.grid_remove()

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()

    def create_account(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        self.current_username = new_username
        self.current_password = new_password

        with open("credentials.txt", "w") as file:
            file.write(f"{self.current_username}\n{self.current_password}")

        self.account_created_label.grid(row=5, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)

        self.app.destroy()
        self.login_instance.open_login_screen()

    def on_closing(self):
        self.app.destroy()
