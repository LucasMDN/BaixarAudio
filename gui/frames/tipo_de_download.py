import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image 

class TipoDeDownload(ctk.CTkFrame):
    def __init__(self, master, titulo, valores):
        super().__init__(master)

        # Criação do  título e configurações do frame
        self.columnconfigure(0, weight=1)
       
        self.titulo = ctk.CTkLabel(self, text=titulo, fg_color="gray30", corner_radius=6)
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky='we')

        self.botoes_criados  = []
        self.botoes_em_exibicao = []
       
        self.mapa_de_icones = {
            "Áudio": {
                "claro": "gui/widgets/audio_modo_claro.png",
                "escuro": "gui/widgets/audio_modo_escuro.png"
            },
            "Vídeo": {
                "claro": "gui/widgets/video_modo_claro.png",
                "escuro": "gui/widgets/video_modo_escuro.png"
            },
            "Playlist": {
                "claro": "gui/widgets/lista_modo_claro.png",
                "escuro": "gui/widgets/lista_modo_escuro.png"
            }
        }


        # Cria o frame par organizar visualmente as opções
        self.opcoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.opcoes_frame.grid(row=1, column=0, sticky='swe')

        # Legenda do botao
        self.valores = valores

        # Variável escolhida pelo usuário
        self.tipo_escolhido = ctk.StringVar(value="")

        # Inicia o processo
        self.juntar_botao_imagem()
        self.exibir_botao()


    def exibir_botao(self):
        for index, (botao, imagem) in enumerate(self.botoes_criados):
            botao.grid(row=index, column=0, padx=5, pady=2, sticky="w")
           
            label_icone = ctk.CTkLabel(self.opcoes_frame, image=imagem, text="")
            label_icone.grid(row=index, column=1, padx=5, pady=2, sticky='w')

            self.botoes_em_exibicao.append(botao)
            self.botoes_em_exibicao.append(label_icone)



    def juntar_botao_imagem(self):
        for tipo in self.valores:
            botao = self.gerar_botao(tipo)
            imagem = ctk.CTkImage(
                light_image= Image.open(self.mapa_de_icones[tipo]["claro"]),
                dark_image= Image.open(self.mapa_de_icones[tipo]["escuro"]),
                size= (20, 20)
            )
            self.botoes_criados.append((botao, imagem))

    def gerar_botao(self, opcao):
        botao_de_opcao = ctk.CTkRadioButton(
            self.opcoes_frame,
            text = opcao,
            value= opcao,
            variable= self.tipo_escolhido
        )

        return botao_de_opcao
        


    def obter_tipo_download(self):
        if self.verificar_tipo_vazio():
            return self.tipo_escolhido.get()

        
    
    def verificar_tipo_vazio(self):
        if not self.tipo_escolhido.get():
            self.exibir_mensagem_de_aviso()
            return False
        return True

    def exibir_mensagem_de_aviso(self):
        CTkMessagebox(
            title="Campo Obrigatório", 
            message="Por favor, preencha a área 'opções de download'!",
            icon="warning",
            option_1="OK")
        