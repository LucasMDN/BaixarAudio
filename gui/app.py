import customtkinter as ctk
from PIL import Image, ImageTk

class RadiobuttonFrame(ctk.CTkFrame):
    def __init__(self, master, titulo, valores):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.valores = valores
        self.radiobuttons  = []
        self.variavel = ctk.StringVar(value='')

        self.audio_img = ctk.CTkImage(light_image=Image.open("gui/widgets/dark_audio_img.png"),
                                 dark_image=Image.open("gui/widgets/light_audio_img.png"),
                                 size=(20,20))

        self.video_img = ctk.CTkImage(light_image=Image.open("gui/widgets/dark_video_img.png"),
                                         dark_image=Image.open("gui/widgets/light_video_img.png"),
                                         size=(20,20))

        self.playlist_img = ctk.CTkImage(light_image=Image.open("gui/widgets/dark_lista_img.png"),
                                         dark_image=Image.open("gui/widgets/light_lista_img.png"),
                                         size=(20,20))
        
        self.imgs = [self.audio_img, self.video_img, self.playlist_img]

        self.titulo = ctk.CTkLabel(self, text=titulo, fg_color="gray30", corner_radius=6)
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky='we')

        for index, valor in enumerate(self.valores):
            linha_frame = ctk.CTkFrame(self, fg_color="transparent")
            linha_frame.grid(row=index + 1, column=0, padx=10, pady=10, sticky="w")

            radiobutton = ctk.CTkRadioButton(
                linha_frame,
                text=valor,
                value=valor,
                variable=self.variavel
            )
            radiobutton.grid(row=0, column=0, sticky="w")

            
            label_img = ctk.CTkLabel(linha_frame, image=self.imgs[index], text="")
            label_img.grid(row=0, column=1, padx=(0, 8))
            

            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variavel.get()

    def set(self, value):
        self.variavel.set(value)


class LinkFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, titulo):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        
        self.titulo = ctk.CTkLabel(self, text=titulo, fg_color="gray30", corner_radius=6)
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.entrada_link = ctk.CTkEntry(self)
        self.entrada_link.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.salvarlink_botao = ctk.CTkButton(self, text='Guardar link', command=self.guardar_link)
        self.salvarlink_botao.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

    def guardar_link(self):
        print('link guarado')


class LocalArmazenamentoFrame(ctk.CTkFrame):
    def __init__(self, master, titulo):
        super().__init__(master)

        self.titulo = ctk.CTkLabel(self, text=titulo, fg_color="gray30", corner_radius=6)
        self.titulo.grid(row=0, column=1, padx=10, pady=10, sticky='we')


class YoutubeTranscricaoFrame(ctk.CTkFrame):
    def __init__(self, master, titulo, conteudo):
        super().__init__(master)
        self.columnconfigure(0, weight=1)

        self.titulo = ctk.CTkLabel(self, text=titulo, fg_color="gray30", corner_radius=6)
        self.titulo.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='we')

        self.transcricao = ctk.CTkTextbox(self, wrap='word', height=120)
        self.transcricao.insert('1.0', conteudo)
        self.transcricao.configure(state='disabled') 
        self.transcricao.grid(row=1, column=0, padx=10, pady=(5,10), sticky='we')


class YoutubeVideoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class YoutubeFrame(ctk.CTkFrame):
    def __init__(self, master, titulo):
        super().__init__(master)

        self.columnconfigure((0,1), weight=1)

        self.transcricao = YoutubeTranscricaoFrame(self, titulo, conteudo='''
                Lorem ipsum dolor sit amet. Aut quia voluptatum et molestias iusto ab voluptate 
                voluptatem eum consequatur quia. Vel accusantium doloribus sed quas corporis et 
                accusamus nihil sed voluptatem consequatur qui cupiditate sunt et fugit molestiae.
        ''')
        self.transcricao.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.video = YoutubeVideoFrame(self)
        self.video.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')


class DownloadButton(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.botao_download = ctk.CTkButton(self, text="Baixar links salvos", command=self.button_callback)
        self.botao_download.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")


    def button_callback(self):
            print("Baixando")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela mãe
        self.title("Download de Mídia")
        self.geometry("700x500")
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.iconbitmap("gui/widgets/download_icon.ico")
        
        # Lina 0
        self.opcoes_frame = RadiobuttonFrame(self, titulo = 'Opções de download', valores = ['Áudio', 'Vídeo', 'Playlist'])
        self.opcoes_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.link_frame = LinkFrame(self, titulo='Cole o link aqui')
        self.link_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.amazenamento_frame = LocalArmazenamentoFrame(self, titulo="Armazenamento")
        self.amazenamento_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # Linha 1
        self.youtube_frame = YoutubeFrame(self, titulo='Transcrição')
        self.youtube_frame.grid(row=1, column=0, padx=10, columnspan=3,  pady=10, sticky='nsew')

        # Linha 2
        self.botaodownload_frame = DownloadButton(self)
        self.botaodownload_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        

    

