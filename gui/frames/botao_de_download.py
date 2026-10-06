import customtkinter as ctk
import os
from core.youtube import chama_download

class BotaoDeDownload(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.botao_download = ctk.CTkButton(self, text="Baixar links salvos", command=self.iniciar_download)
        self.botao_download.grid(row=0, column=0, padx=10, pady=(10), sticky="ew")

    def iniciar_download(self):
        if os.path.exists('gui/frames/urls_salvas.csv'):
            chama_download('gui/frames/urls_salvas.csv')
            self.limpa_lista_downloads()

    def limpa_lista_downloads(self):
       with open('gui/frames/urls_salvas.csv', "w"):
           pass
