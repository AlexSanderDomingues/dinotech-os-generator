
from ui.tela_login import tela_login

if __name__ == "__main__":
    import customtkinter as ctk 
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Apenas no Windows
    except:
        pass
        
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)

    root = ctk.CTk()
    root.geometry("600x700")
    root.resizable(False,False)
    tela_login(root)

    root.mainloop()