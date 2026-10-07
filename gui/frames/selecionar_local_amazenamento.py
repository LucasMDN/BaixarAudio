import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

class EscolhePastaDestino(ctk.CTkFrame):
    def __init__(self, master, titulo):
        super().__init__(master)

        self.destino_selecionado = ctk.StringVar(value="")
        self.mensagem = "Destino não selecionado."
        
        self.titulo = ctk.CTkLabel(self, text=titulo, fg_color='gray30', corner_radius=6)
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky='nwe')

        botao = ctk.CTkButton(self, text="Escolha a pasta de destino", command=self.selecionar_pasta)
        botao.grid(row=1, column=0, padx=10, pady=10, sticky='swe')

        self.mostrar_destino = ctk.CTkTextbox(self, wrap='word', height=75)
        self.mostrar_destino.insert('1.0', self.mensagem)
        self.mostrar_destino.configure(state='disabled')
        self.mostrar_destino.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='we')

    def receber_local_destino(self):
        return self.destino_selecionado.get()


    def selecionar_pasta(self):
        pasta =  filedialog.askdirectory(
            title = "Seletor de pastas",
            mustexist = True)
        
        self.atualiza_interface(pasta)
        return pasta
    
    def atualiza_interface(self, destino):
        if destino:
            self.destino_selecionado.set(destino)
            self.mostrar_destino.configure(state='normal')   
            self.mostrar_destino.delete('1.0', 'end')        
            self.mostrar_destino.insert('1.0', destino)        
            self.mostrar_destino.configure(state='disabled') 
        
    def verificar_destino_vazio(self):
        destino_vazio = self.destino_selecionado.get()

        if not destino_vazio:
            self.exibir_mensagem_de_aviso()
            return False
        else: 
            return True

    def exibir_mensagem_de_aviso(self):
        CTkMessagebox(
            title="Campo Obrigatório", 
            message="Por favor, escolha o destino do download!",
            icon="warning",
            option_1="OK")
