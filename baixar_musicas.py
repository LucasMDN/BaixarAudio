import os
import csv
import sys
import subprocess
import yt_dlp
import shutil
from pathlib import Path

def baixar_musica(youtube_url, destino="musicas", tipo="mp3"):
    if youtube_url and not youtube_url.strip():
        print("Erro: Nenhuma URL fornecida!")
        return

    os.makedirs(destino, exist_ok=True)
 
    output_template = os.path.join(destino, "%(title)s.%(ext)s")

    comando = [
        sys.executable, "-m", "yt_dlp", "-U",
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", tipo,
        "-o", output_template,
        youtube_url
    ]

    try:
        subprocess.run(comando, check=True, encoding='utf-8')
        print("Música baixada com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao baixar a música: {e}")

def download_audio(url, destino=".", extencao="mp3", ignoraplaylist=True):
    """
    Baixa o áudio de um vídeo usando yt-dlp.

    Args:
        url (str): O URL do vídeo.
    """
    os.makedirs(destino, exist_ok=True)
    
    if not os.path.exists(destino):
        os.makedirs(destino)
        print(f"Diretório de destino criado: {destino}")
    else:
        print(f"Diretório de destino existente: {destino}")
    # destino = os.path.abspath(destino)
    
    # Opções para o yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Seleciona a melhor qualidade de áudio
        'postprocessors': 
        [
            {
                'key': 'FFmpegExtractAudio',  # Usa o FFmpeg para extrair o áudio
                'preferredcodec': extencao,      # Formato de áudio preferido (mp3)
                'preferredquality': '192',    # Qualidade de áudio preferida (192kbps)
            },
        ],
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'), # Salva no diretório atual com o título do vídeo
        'noplaylist': True, # Ignora playlists
        'verbose': False, # Desativa a saída detalhada
        'noprogress': False, # Mostra a barra de progresso
        'restrictfilenames': False
    }
    
    try:
        print(f"Tentando baixar áudio de: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            print(f"\nDownload concluído. Arquivo salvo como: {filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')}")
    
        if not os.path.exists(destino):
            os.makedirs(destino)        

        # mover_arquivo('./musicas/', destino)
    except Exception as e:
        print(f"\nOcorreu um erro durante o download: {e}")
        print("Certifique-se de que o URL é válido e que o yt-dlp e o ffmpeg estão instalados e acessíveis.")

def mover_arquivo(caminho_origem, caminho_destino):
    """
    Move um arquivo de um local para outro.

    Args:
        caminho_origem (str): O caminho do arquivo de origem.
        caminho_destino (str): O caminho do arquivo de destino.
    """
    musica_list = Path(caminho_origem).glob('*.mp3')
    try:
        for musica in musica_list:
            path = Path(musica).absolute
            shutil.move(musica, caminho_destino)
        print(f"Arquivo movido de {caminho_origem} para {caminho_destino}")
    except Exception as e:
        print(f"Erro ao mover o arquivo: {e}")

musica_list = []
with open('musicas.csv', 'r', encoding='utf-8') as file:
    musica_list = csv.reader(file, delimiter=';')
    
    for url_dict in musica_list:
        if len(url_dict) >= 2:
            print('Tipo: %s' % url_dict[0], 'Download: %s' % url_dict[1])
            destino_final = r"C:\Users\lucas\Music\baixadosJandy"
            destino_final = r"baixadosJandy"
            # baixar_musica(url_dict[1].strip(), destino=destino_final, tipo=url_dict[0].strip())
            ignoraplaylist = url_dict[2].strip()=='0' and False or True
            download_audio(url_dict[1].strip(), destino=destino_final, extencao=url_dict[0].strip(), ignoraplaylist=ignoraplaylist)
            
    # mover_arquivo('./musicas/', destino_final)