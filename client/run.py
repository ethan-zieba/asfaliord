from client import Client
from client_interface import LoginScreen
import credentials
import tkinter as tk


# Here credentials is a .py file with testing credentials, for test version only
root = tk.Tk()
root.minsize(360, (400))
login_screen = LoginScreen(root, Client(credentials.tor_address))
root.mainloop()
