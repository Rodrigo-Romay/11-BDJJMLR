import customtkinter as ctk
from frontend.gui import GUI

if __name__ == "__main__":
    root = ctk.CTk()
    app = GUI(root)
    root.mainloop()