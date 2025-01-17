import os
import tkinter as tk
import credentials
from PIL import Image, ImageTk


class CreateAccountScreen(tk.Frame):
    def __init__(self, master, screen_callback, client):
        tk.Frame.__init__(self, master)
        self.master = master
        self.client = client
        self.login_screen = screen_callback
        self.master.minsize(100, 100)

        custom_font = ('Classic Console Neue', 16)
        # Configures frame background
        self.configure(bg="#292929")
        self.option_add("*Font", custom_font)

        self.create_widgets()
        self.create_buttons()
        self.grid_placement()

    def create_widgets(self):
        # Using getcwd because Linux did not understand the path as Windows did
        logo_path = rf"{os.getcwd()}/assets/images/logo/asfaliord_logo.png"
        logo_image = Image.open(logo_path)
        logo_size = (150, int((logo_image.size[1] / logo_image.size[0]) * 150))

        self.logo = ImageTk.PhotoImage(logo_image.resize(logo_size))
        self.label_logo = tk.Label(self, image=self.logo, background="#292929")
        self.label_logo.image = self.logo
        self.label_logo.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        self.label_server = tk.Label(self, text=f"  Create account on server: \n{credentials.tor_address[7:17]}[...]{credentials.tor_address[-16:-6]}",
                                     foreground='#04FF00', background="#292929", font=("Classic Console Neue", 12))
        self.label_username = tk.Label(self, text="Username", foreground='#04FF00', background="#292929")
        self.label_password = tk.Label(self, text="Password", foreground='#04FF00', background="#292929")
        self.label_gpg_key = tk.Label(self, text="GPG Public Key", foreground='#04FF00', background="#292929")
        # Password error label for password non-conformity
        self.label_password_error = tk.Label(self, text="", foreground='red', background="#292929", justify="left")

        self.entry_username = tk.Entry(self, foreground='#04FF00', bg='#000F44')
        self.entry_password = tk.Entry(self, show="*", foreground='#04FF00', bg='#000F44')
        self.entry_gpg_key = tk.Entry(self, foreground='#04FF00', bg='#000F44')

    def create_buttons(self):
        self.button_back = tk.Button(self, text="Back", command=self.login_screen, background='#2937FF',
                                      foreground='#04FF00', activebackground='#4DC9FF', activeforeground='#04FF00')
        self.button_create_account = tk.Button(self, text="Create Account", command=self.create_account,
                                               background='#2937FF',
                                               foreground='#04FF00', activebackground='#4DC9FF',
                                               activeforeground='#04FF00')

    def grid_placement(self):
        self.label_server.grid(row=1, column=0, columnspan=2, sticky=tk.EW)
        self.label_username.grid(row=2, column=0, padx=10, sticky=tk.E)
        self.label_password.grid(row=3, column=0, padx=10, sticky=tk.E)
        self.label_gpg_key.grid(row=4, column=0, padx=10, sticky=tk.E)
        self.entry_username.grid(row=2, column=1, pady=10)
        self.entry_password.grid(row=3, column=1, pady=10)
        self.entry_gpg_key.grid(row=4, column=1, pady=10)
        self.label_password_error.grid(row=1, column=2, rowspan=4, padx=10, sticky=tk.W)
        self.button_back.grid(row=5, column=0, padx=10, pady=10)
        self.button_create_account.grid(row=5, column=1, padx=10, pady=30)
        # Configure for responsive app
        for i in range(5):
            self.grid_columnconfigure(i, weight=0)

    def create_account(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        gpg_key = self.entry_gpg_key.get()
        # Calls client.create_account method, returns True or False
        if self.client.create_account(username, password, gpg_key):
            self.label_success = tk.Label(self, text="Account Creation Successful", foreground='#04FF00', background="#292929")
            self.label_success.grid(row=6, column=0, pady=10)
            self.master.after(3000, self.login_screen)


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(360, (400))
    login_screen = CreateAccountScreen(root)
    root.mainloop()
