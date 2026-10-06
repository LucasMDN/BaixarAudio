import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import PIL 

class TipoDeDownload(ctk.CTkFrame):
    def __init__(self, master, titulo, valores):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.valores = valores
        self.radiobuttons  = []
        self.variavel = ctk.StringVar(value='')

        mapa_icones = {
            'audio': ("gui/widgets/dark_audio_img.png", "gui/widgets/light_audio_img.png"),
            'video': ("gui/widgets/dark_video_img.png", "gui/widgets/light_video_img.png"),
            'playlist': ("gui/widgets/dark_lista_img.png", "gui/widgets/light_lista_img.png")
        }

        self.audio_img = ctk.CTkImage(light_image=PIL.Image.open(mapa_icones["audio"][0]),
                                 dark_image=PIL.Image.open(mapa_icones["audio"][1]),
                                 size=(20,20))

        self.video_img = ctk.CTkImage(light_image=PIL.Image.open(mapa_icones["video"][0]),
                                         dark_image=PIL.Image.open(mapa_icones["video"][1]),
                                         size=(20,20))

        self.playlist_img = ctk.CTkImage(light_image=PIL.Image.open(mapa_icones["playlist"][0]),
                                         dark_image=PIL.Image.open(mapa_icones["playlist"][1]),
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


    def receber_tipo_download(self):
        return self.variavel.get()

    
    def verificar_tipo_vazio(self):
        tipo_vazio = self.variavel.get()
        if tipo_vazio == "":
            self.exibir_mensagem_de_aviso()
            return False
        else:
            return True
        
    def exibir_mensagem_de_aviso(self):
        CTkMessagebox(
            title="Campo Obrigatório", 
            message="Por favor, preencha a área 'opções de download'!",
            icon="warning",
            option_1="OK")
        