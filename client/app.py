from client import Client
import credentials
import tkinter as tk
from client_login_screen import LoginScreen
from client_create_account_screen import CreateAccountScreen


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Asfaliord")
        self.iconbitmap("assets/images/logo/asfaliord_logo.ico")
        self.login_screen = LoginScreen(self, self.go_to_create_account)
        self.cr_account_screen = CreateAccountScreen(self, self.go_to_login)

        self.current_screen = self.login_screen
        self.show_screen(self.current_screen)

    def go_to_login(self):
        self.show_screen(self.login_screen)

    def go_to_create_account(self):
        self.show_screen(self.cr_account_screen)

    def show_screen(self, screen):
        if self.current_screen:
            self.current_screen.grid_forget()
        self.current_screen = screen
        self.current_screen.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.title = "Asfaliord"
    app.mainloop()
