import customtkinter as ctk
from gui.frames import (
    pegar_transcricao_video, 
    player_da_url_selecionada, 
    salvar_link, 
    selecionar_local_amazenamento, 
    selecionar_tipo_download, 
    botao_de_download
)



class YoutubeFrame(ctk.CTkFrame):
    def __init__(self, master, titulo):
        super().__init__(master)

        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(0, weight=2)

        self.transcricao = pegar_transcricao_video.TranscricaoDoVideo(self, titulo)
        self.transcricao.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.video = player_da_url_selecionada.PlayerDoVideo(self)
        self.video.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    def atualizar_url(self,url):
        self.transcricao.atualizar_transcricao(url)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela mãe
        self.title("Download de Mídia")
        self.geometry("700x530")
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.iconbitmap("gui/widgets/download_icon.ico")


         # Linha 1
        self.youtube_frame = YoutubeFrame(
            self, 
            titulo='Legendas'
            )
        self.youtube_frame.grid(row=1, column=0, padx=10, columnspan=3,  pady=5, sticky='nsew')
        
    
        # Lina 0
        self.opcoes_frame = selecionar_tipo_download.TipoDeDownload(
            self, 
            titulo = 'Opções de download', 
            valores = ['Áudio', 'Vídeo', 'Playlist']
            )
        self.opcoes_frame.grid(row=0, column=0, padx=10, pady=(10,5), sticky='nsew')
        
        self.amazenamento_frame = selecionar_local_amazenamento.EscolhePastaDestino(
            self, 
            titulo="Armazenamento"
            )
        self.amazenamento_frame.grid(row=0, column=2, padx=10, pady=(10,5), sticky='nsew')

        self.link_frame = salvar_link.SalvarLink(
            self, 
            self.opcoes_frame, 
            self.amazenamento_frame, 
            titulo='Cole o link aqui',
            acionar_ao_mudar_url=self.youtube_frame.atualizar_url
            )
        self.link_frame.grid(row=0, column=1, padx=5, pady=(10,5), sticky='nsew')

       
        # Linha 2
        self.botaodownload_frame = botao_de_download.BotaoDeDownload(self)
        self.botaodownload_frame.grid(row=2, column=0, columnspan=3, padx=(10), pady=(5,10), sticky='we')

