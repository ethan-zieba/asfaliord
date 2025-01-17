from client import Client
import os
import sys
sys.path.insert(1, f'{os.getcwd()}/../..')
import credentials
import tkinter as tk
from client_login_screen import LoginScreen
from client_create_account_screen import CreateAccountScreen
from client_main_interface import MainInterfaceScreen


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("365x438")
        self.configure(bg="#292929")
        self.title("Asfaliord")
        # Here, ico format is not usable on Linux, so we commented it
        # self.iconbitmap(f"{os.getcwd()}/client/assets/images/logo/asfaliord_logo.ico")
        self.client = Client(credentials.tor_address)
        self.main_interface = MainInterfaceScreen(self, self.client, self.go_to_login)
        self.cr_account_screen = CreateAccountScreen(self, self.go_to_login, self.client)
        self.login_screen = LoginScreen(self, self.go_to_create_account, self.go_to_main_interface, self.client)
        self.current_screen = self.login_screen
        self.show_screen(self.current_screen)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def go_to_login(self):
        # Login callback, calls the login_screen
        self.geometry("365x438")
        self.client = Client(credentials.tor_address)
        self.login_screen.client = self.client
        self.show_screen(self.login_screen)

    def go_to_create_account(self):
        # Calls the create_account screen
        # Try to put the object instance directly here when go_to_create_account is called
        self.geometry("410x410")
        self.show_screen(self.cr_account_screen)

    def go_to_main_interface(self):
        # Calls the main_interface screen
        # Try to put the object instance directly here when go_to_main_interface is called
        self.geometry("1400x700")
        self.main_interface.client = self.client
        self.main_interface.disconnect = False
        self.main_interface.start_messages_coroutine()
        self.main_interface.thread_get_server_infos()
        self.main_interface.create_left_buttons()
        self.show_screen(self.main_interface)

    def show_screen(self, screen):
        if self.current_screen:
            self.current_screen.grid_forget()
        self.current_screen = screen
        # Resets the grid position of the current screen
        self.current_screen.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.title = "Asfaliord"
    app.mainloop()
