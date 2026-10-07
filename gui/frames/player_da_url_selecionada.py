import customtkinter as ctk

class PlayerDoVideo(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.janela_video = ctk.CTkCanvas(self)
        self.janela_video.grid(row=0, column=0, padx=10, pady=10, sticky='we')

       

