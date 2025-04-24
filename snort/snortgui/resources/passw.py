import passw
import tkinter as tk
sudo_password = None

def getPass() :
    if not passw.sudo_password :
        passw.sudo_password = tk.simpledialog.askstring("Password", "\nEnter your administrator password:\n", show='*')
    return passw.sudo_password
