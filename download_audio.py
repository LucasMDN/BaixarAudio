import os
import time
from pytube import YouTube
from pytube import Playlist
import youtube_dl, yt_dlp

os.environ['PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT'] = '1'


def ler_arquivo(caminho):
    musica = []
    with open(caminho, 'r') as file:
        musica = file.readlines()
    
    return musica
        
def converter_conteudo(lista_conteudo):
    lista = []
    for item in lista_conteudo:
        item = item.strip()
        dados = item.split(';')
        lista.append({
            'tipo': dados[0],
            'url': dados[1],
            'prefixo': dados[2]
        })

    return lista

def cria_pastas():
    try:
        diretorio = os.path.dirname(os.path.abspath(__file__))
        for item in ['Musicas', 'Videos', 'Playlist']:
            pasta = os.path.join(diretorio, item)
            os.makedirs(pasta, exist_ok=True)
    except Exception as erro:
        print('Não foi possível criar as pastas: %s', erro)

def pegar_destino(tipo):
    match tipo:
        case 'audio':
            return os.path.abspath('Musicas')
        case 'video':
            return os.path.abspath('Videos')
        case 'playlist':
            return os.path.abspath('Playlist')
       


def download_audio(audio_url, destino, prefixo=None):
    try:
        
        # Na minha cabeça isso ta estranho, se o usuário não tiver baixado vai dar erro
        deno_path = os.path.join(os.environ['USERPROFILE'], '.deno', 'bin', 'deno.exe') 
        
        # yt-dlp é mais compatível com as alterações recentes do YouTube
        opcoes = {
            'format': 'bestaudio/best',
            'outtmpl':  f'{destino}/{prefixo}_%(title)s.%(ext)s',  
            'noplaylist': True,
            'js_runtimes': {'deno': {'path': deno_path}},
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([audio_url])
        print("Download concluído!")
    except Exception as erro:
        print(f"Erro ao baixar o áudio: {erro}")

def download_playlist(playlist_url, prefixo=None):
    playlist = Playlist(playlist_url)
    for url in playlist:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path='playlist', filename_prefix=prefixo)

def download_video(video_url, prefixo=None):
    yt = YouTube(video_url)
    video = yt.streams.get_highest_resolution()
    video.download(filename_prefix=prefixo)

'''
def baixar_musica(url):
  # Opções de download (salva o arquivo no formato de áudio)
  opcoes = {
    'format': 'bestaudio/best', # Baixar a melhor qualidade de áudio
    'extractaudio': True, # Extrair apenas o áudio
    'audioquality': 1, # Qualidade do áudio (1 = melhor)
    'outtmpl': '%(title)s.%(ext)s', # Nome do arquivo com o título do vídeo
    'postprocessors': [{
      'key': 'FFmpegAudioConvertor', # Usar FFmpeg para converter o arquivo para MP3
      'preferredcodec': 'mp3',
      'preferredquality': '192', # Qualidade do mp3
    }],
    'progress_hooks': [lambda d: print(d)] # Opcional: Para depuração (mostra o progresso)
  }

  # Criar o objeto yt-dlp com as opções
  with yt_dlp.YoutubeDL(opcoes) as ydl:
    ydl.download([url]) # Baixar o vídeo ou áudio

def download_audio2(url, prefixo=None):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path='.', filename='audio.mp3')
        print("Download concluído!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def download_audio22(yt_url, prefixo=None):
    opcoes = {
        'format': 'bestaudio/best',  # Baixar a melhor qualidade de áudio
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Qualidade do mp3
        }],
        'outtmpl': '%(title)s.%(ext)s',  # Nome do arquivo
        'force_generic_extractor': True,
    }
    
    try:
        with youtube_dl.YoutubeDL(opcoes) as ydl:
            ydl.download([yt_url])
        print("Download concluído!")
    except Exception as e:
        print(f"Erro ao tentar baixar o vídeo: {e}")
'''

if __name__ == '__main__':  
    
    cria_pastas() 
    musica_list = ler_arquivo('musicas.csv')
    musica_list = converter_conteudo(musica_list)
    
    for index, url_dict in enumerate(musica_list):
        print('Baixando (%s/%s) ... %s' % (index + 1, len(musica_list), url_dict['url']))
        
        if url_dict['tipo'] == 'audio':
            caminho = pegar_destino(url_dict['tipo']) 
            #Se eu chamar pegar_destino() a função aqui ela vai se repetir toda vez, se tiver 400 musica ele repete 400 vezes
            # seria melhor deixar fixo antes do for loop?
            download_audio(url_dict['url'], caminho, url_dict.get('prefixo'))
        
        if url_dict['tipo'] == 'playlist':
            caminho = pegar_destino(url_dict['tipo'])
            download_playlist(url_dict['url'], caminho, url_dict.get('prefixo'))

        if url_dict['tipo'] == 'video':
            caminho = pegar_destino(url_dict['tipo'])
            download_video(url_dict['url'], caminho, url_dict.get('prefixo'))
        
        
        print('  Finaizado a URL %s' % url_dict['url'])
