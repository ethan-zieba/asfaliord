import customtkinter
import tkinter
from threading import Thread
import requests
import subprocess
from config_values import *

class URL:
    def __init__(self):
        customtkinter.set_appearance_mode(BACKGROUND_COLOR)
        customtkinter.set_default_color_theme(DEFAULT_COLOR_THEME)

        self.app = customtkinter.CTk()
        self.app.title("Asfaliord")
        self.app.geometry(WINDOW_SIZE)

        # Logo
        logo_path = "asfaliord.png"  
        logo_image = tkinter.PhotoImage(file=logo_path).subsample(10, 10)
        logo_label = tkinter.Label(self.app, image=logo_image, bd=10, relief="flat", bg="black")
        logo_label.grid(row=0, column=0, pady=LABEL_PADY, padx=20, sticky="e")

        # Title in bold next to the logo
        title_label = customtkinter.CTkLabel(self.app, text="Asfaliord", font=LOGIN_TITLE_FONT, fg_color=LOGIN_SUCCESS_COLOR)
        title_label.grid(row=0, column=1, pady=0.01, padx=0.01)

        # Entry for URL
        self.entry_url = customtkinter.CTkEntry(self.app, width=500, font=DEFAULT_FONT)
        self.entry_url.grid(row=1, column=0, columnspan=2, padx=5, pady=ENTRY_PADY)

        # Button to connect
        self.button_connect = customtkinter.CTkButton(master=self.app, text="Connecter", command=self.handle_connect_button, font=DEFAULT_FONT, fg_color=LOGIN_SUCCESS_COLOR)
        self.button_connect.grid(row=2, column=0, columnspan=2, pady=BUTTON_PADY)

        # Loading screen
        self.loading_label = customtkinter.CTkLabel(self.app, text="Connexion en cours...", font=DEFAULT_FONT)
        self.loading_label.grid(row=3, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        self.loading_label.grid_remove()

        # Timeout screen
        self.timeout_label = customtkinter.CTkLabel(self.app, text="Url invalide", font=DEFAULT_FONT, fg_color=LOGIN_FAILED_COLOR)
        self.timeout_label.grid(row=4, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        self.timeout_label.grid_remove()

        # Success screen
        self.success_label = customtkinter.CTkLabel(self.app, text="Connexion Réussie!", font=DEFAULT_FONT, fg_color=LOGIN_SUCCESS_COLOR)
        self.success_label.grid(row=4, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        self.success_label.grid_remove()

        self.app.mainloop()

    def handle_connect_button(self):
        url = self.entry_url.get()

        # Add a loading screen or other UI updates here
        self.loading_label.grid(row=3, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)

        # Start a thread to connect to the service and avoid blocking the UI
        connection_thread = Thread(target=self.connect_to_service, args=(url,))
        connection_thread.start()

    def connect_to_service(self, url):
        try:
            # Validate the URL using requests
            response = requests.get(url, timeout=5)

            if "asfaliord" in url.lower():
                # If the URL contains "asfaliord", execute the Login class from screen2.py
                self.open_login_screen()
                return
            elif response.status_code == 200:
                # If the connection succeeds and it's not "asfaliord", update the UI or perform actions accordingly
                self.success_label.grid(row=4, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
                # Change the button text to "Continuer"
                self.button_connect.config(text="Continuer")
            else:
                # If the status code is different from 200, display a timeout screen
                self.timeout_label.grid(row=4, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)
        except requests.exceptions.RequestException:
            # In case of timeout or other connection error, display a timeout screen
            self.timeout_label.grid(row=4, column=0, columnspan=2, pady=LOGIN_SUCCESS_PADY)

        # Hide the loading screen after the connection attempt
        self.loading_label.grid_remove()

    def open_login_screen(self):
        # Import the Login class from screen2.py and instantiate it
        from screen2 import Login
        login_instance = Login(self.app)  # Pass the main app instance to the Login class
        login_instance.run_login()

    def open_screen2(self):
        # Open screen2.py or any other action you want to perform
        subprocess.Popen(["python", "screen2.py"])

# Create an instance of the URL class
url_instance = URL()
