import tkinter as tk
from PIL import Image, ImageTk


class LoginScreen:
    def __init__(self, window, client):
        self.window = window
        self.client = client

        window.title("Login")
        window.configure(bg="#292929")

        logo_path = "assets/images/logo/asfaliord_logo.png"
        logo_image = Image.open(logo_path)
        logo_size = (150, int((logo_image.size[1]/logo_image.size[0]) * 150))

        self.logo = ImageTk.PhotoImage(logo_image.resize(logo_size))
        self.label_logo = tk.Label(window, image=self.logo, background="#292929")
        self.label_logo.image = self.logo
        self.label_logo.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

        custom_font = ('Classic Console Neue', 16)
        window.option_add("*Font", custom_font)

        self.label_username = tk.Label(window, text="Username", foreground='#04FF00', background="#292929")
        self.label_password = tk.Label(window, text="Password", foreground='#04FF00', background="#292929")

        self.entry_username = tk.Entry(window, foreground='#04FF00', bg='#000F44')
        self.entry_password = tk.Entry(window, show="*", foreground='#04FF00', bg='#000F44')

        self.remember_user = tk.IntVar()
        self.checkbox_remember = tk.Checkbutton(window, text="Remember me", background="#292929", foreground='#04FF00',
                                                activebackground="#292929", highlightbackground="#292929", variable=self.remember_user,
                                                selectcolor="#000F44")

        self.create_buttons(window)

        # Placement des widgets dans la grille
        self.label_username.grid(row=1, column=0, sticky=tk.E)
        self.label_password.grid(row=2, column=0, sticky=tk.E)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        self.checkbox_remember.grid(row=3, column=0, columnspan=2, padx=80, pady=5, sticky=tk.EW)
        self.button_login.grid(row=4, column=0, columnspan=2, padx=80, pady=5, sticky=tk.EW)
        self.button_create_account.grid(row=5, column=0, columnspan=2, rowspan=2, padx=80, pady=10, sticky=tk.EW)

        for i in range(5):
            self.window.grid_rowconfigure(i, weight=2)
        for i in range(2):
            self.window.grid_columnconfigure(i, weight=2)

    def create_buttons(self, window):
        self.button_login = tk.Button(window, text="Login", command=self.login, background='#2937FF',
                                      foreground='#04FF00', activebackground='#4DC9FF', activeforeground='#04FF00')
        self.button_create_account = tk.Button(window, text="Create Account", command=self.create_account,
                                               background='#2937FF',
                                               foreground='#04FF00', activebackground='#4DC9FF',
                                               activeforeground='#04FF00')

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.client.authenticate(username, password)

    def create_account(self):
        # Ajoutez ici le code pour afficher l'écran de création de compte
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(360, (400))
    login_screen = LoginScreen(root)
    root.mainloop()