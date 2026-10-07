import re
import threading
import customtkinter as ctk
from urllib.parse import unquote
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

class TranscricaoDoVideo(ctk.CTkFrame):
    def __init__(self, master, titulo, url=None):
        super().__init__(master)

        # Configuração de colunas e exibição de título
        self.columnconfigure(0, weight=1)
        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            fg_color="gray30",
            corner_radius=6
        )
        self.titulo.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='we')

        # Configura o frame que vai receber a transcrição
        self.caixa_transcricao = ctk.CTkTextbox(self, wrap='word', height=180)
        self.caixa_transcricao.configure(state='disabled')
        self.caixa_transcricao.grid(row=1, column=0, padx=10,
                                    pady=(5, 10), sticky='swe')

        # Chama a função a atuliza o texto exibido
        self.requisicao_atual = 0
        if url:
            self.atualizar_transcricao(url)

    def atualizar_transcricao(self, url):
        if not url:
            self.mostrar_texto(
                "Cole um link do YouTube para ver a transcrição.")
            return

        video_id = self.extrair_video_id(url)
        if not video_id:
            self.mostrar_texto("Link inválido (aguardando link do YouTube)...")
            return

        self.mostrar_texto("Carregando transcrição...")

        self.requisicao_atual += 1
        requisicao = self.requisicao_atual

        threading.Thread(
            target=self.buscar_transcricao_em_thread,
            args=(video_id, requisicao),
            daemon=True
        ).start()

    def buscar_transcricao_em_thread(self, url, requisicao):
        texto = self.obter_transcricao(url)
        if requisicao == self.requisicao_atual:
            self.after(0, self.mostrar_texto, texto)

    def mostrar_texto(self, texto):
        self.caixa_transcricao.configure(state='normal')
        self.caixa_transcricao.delete('1.0', 'end')
        self.caixa_transcricao.insert('1.0', texto)
        self.caixa_transcricao.configure(state='disabled')

    def obter_transcricao(self, video_id):
        try:
            if video_id:
                transcricao = YouTubeTranscriptApi().fetch(
                    video_id, languages=['pt', 'en'])
                texto = " ".join(segmento.text for segmento in transcricao)
                return texto

            else:
                return "Link inválido"

        except TranscriptsDisabled:
            return "vídeo sem legendas."
        except NoTranscriptFound:
            return "Nenhum dos idiomas pedidos disponível."
        except VideoUnavailable:
            return "vídeo privado/removido."
        except Exception as e:
            return f"Erro ao buscar transcrição: {e}"

    def extrair_video_id(self, url):
        if not isinstance(url, str):
            return None

        url_dec = unquote(url)

        if not re.search(r"(?:youtube\.com|youtu\.be)", url_dec):
            return None

        padrao = r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/|/live/)([A-Za-z0-9_-]{11})"
        m = re.search(padrao, url_dec)
        return m.group(1) if m else None
