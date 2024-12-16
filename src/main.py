import customtkinter as ctk
from frontend.gui import GUI

if __name__ == "__main__":
    root = ctk.CTk()
    app = GUI(root)
    root.after(100, app.show_welcome_message)
    root.mainloop()