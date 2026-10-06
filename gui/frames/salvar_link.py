import customtkinter as ctk
import csv

class SalvarLink(ctk.CTkFrame):
    def __init__(self, master, pegar_tipo, pegar_destino, titulo, acionar_ao_mudar_url=None):
        super().__init__(master)

        # Configuração de coluna e exibição do título
        self.columnconfigure(0, weight=1)
        self.titulo = ctk.CTkLabel(
            self, 
            text=titulo, 
            fg_color="gray30", 
            corner_radius=6
        ) 
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky='new')

        self.limpa_lista_downloads()

        self.ultima_informacao_salva = None

        # Criando a variavel que recebe a url
        self.url = ctk.StringVar()
        self.url.trace_add("write", self.detectar_mudanca_url)

        # Recebe instâncias das classes TipoDeDownload e EscolhePastaDestino
        self.pegar_tipo = pegar_tipo
        self.pegar_destino = pegar_destino

        # Cria o input para o usuári informar a url
        self.entrada_link = ctk.CTkEntry(self, textvariable=self.url)
        self.entrada_link.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        # Cria o botão que salva tipo, url e local de armazenamento em um arquivo csv
        self.salvar_download_info_botao = ctk.CTkButton(
            self, text='Guardar link', 
            command=self.escreve_lista_de_download_em_csv
        )
        self.salvar_download_info_botao.grid(
            row=2, column=0, padx=10, pady=10, sticky='sew')

        # Exibe a quantidade de url que foram salvas urante a execução do programa
        self.quantidade_links = 0
        self.exibir_quantidade_links = ctk.CTkLabel(
            self, text=f"Links salvos - {self.quantidade_links}",
            fg_color="transparent"
        )
        self.exibir_quantidade_links.grid(row=3, column=0, padx=5, pady=5, sticky='swe')

        # Variáveis que auxiliam no registro e salvamento das mudanças na url
        self.acionar_ao_mudar_url = acionar_ao_mudar_url
        self.id_temporizador = None
        self.ultima_mudanca_url = ""

    # Faz o reconhecimento automático do link antes e depois de salvar
    def detectar_mudanca_url(self, *args):
        if self.id_temporizador is not None:
            self.after_cancel(self.id_temporizador)

        self.id_temporizador = self.after(700, self.notificar_mudanca)

    def notificar_mudanca(self):
        url = self.url.get()
        if url == self.ultima_mudanca_url:
            return

        self.ultima_mudanca_url = url
        if self.acionar_ao_mudar_url:
            self.acionar_ao_mudar_url(url)


    # Junta as informações necessárias faz a validação e salva
    def juntar_tipo_url_local(self):
        destino_existe = self.pegar_destino.verificar_destino_vazio()
        tipo_nao_vazio = self.pegar_tipo.verificar_tipo_vazio()

        if (destino_existe and tipo_nao_vazio):
            tipo_download = self.pegar_tipo.receber_tipo_download()
            pasta_destino = self.pegar_destino.receber_local_destino()
            url = self.entrada_link.get()

            mapa_tipo = {
                "Áudio": "audio",
                "Vídeo": "video",
                "Playlist": "playlist"}
            
            tipo_download_convertido = mapa_tipo[tipo_download]
        return [tipo_download_convertido, url, pasta_destino]

    def escreve_lista_de_download_em_csv(self):
        informacao_download = self.juntar_tipo_url_local()

        if informacao_download == self.ultima_informacao_salva:
            return

        
        with open("gui/frames/urls_salvas.csv", "a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')
            escritor.writerow([informacao_download[0], informacao_download[1], informacao_download[2]])

        self.quantidade_links += 1
        self.ultima_informacao_salva = informacao_download
        self.atualizar_contador_links()

    def atualizar_contador_links(self):
        self.exibir_quantidade_links.configure(
            text=f"Links salvos - {self.quantidade_links}"
        )

    def limpa_lista_downloads(self):
        with open('gui/frames/urls_salvas.csv', "w"):
            pass
    


    