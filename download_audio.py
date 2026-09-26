import os
import yt_dlp
from re import compile

os.environ['PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT'] = '1'


def ler_arquivo(caminho):
    musica = []
    with open(caminho, 'r') as file:
        musica = file.readlines()

    return musica


def veirifar_conteudo(conteudo):
    try:
        tamanho_conteudo = len(conteudo)
        if tamanho_conteudo != 2:
            return False

        tipo = conteudo[0]
        if tipo not in ['audio', 'video', 'playlist']:
            return False

        url = conteudo[1]
        if not url:
            return False

        youtube_regex = compile(
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be|youtube-nocookie\.com)/')
        if not youtube_regex.search(url):
            return False

        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'extract_flat': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info.get('extractor_key', '').startswith("Youtube"):
                return False

        return True

    except Exception:
        return False


def converter_conteudo(lista_conteudo):
    arq_compativel = []
    arq_incompativel = []

    for item in lista_conteudo:
        item = item.strip()
        dados = item.split(';')

        dados_corretos = veirifar_conteudo(dados)

        if dados_corretos:
            arq_compativel.append({
                'tipo': dados[0],
                'url': dados[1]
            })

        else:
            url = '' if len(dados) <= 1 else dados[1]
            arq_incompativel.append({'tip0': dados[0], 'url': url})

    if arq_incompativel:
        print('Não foi possível baixar os links:')
        for index, item in enumerate(arq_incompativel):
            print(f"{index+1} -- {item['url']}")
        print('\n')

    return arq_compativel

def cria_pastas():
    try:
        diretorio = os.path.dirname(os.path.abspath(__file__))
        for item in ['Musicas', 'Videos', 'Playlist']:
            pasta = os.path.join(diretorio, item)
            os.makedirs(pasta, exist_ok=True)
        return True

    except Exception as erro:
        print('Não foi possível criar as pastas: %s', erro)
        return False


def pegar_destino(tipo):
    match tipo:
        case 'audio':
            return os.path.abspath('Musicas')
        case 'video':
            return os.path.abspath('Videos')
        case 'playlist':
            return os.path.abspath('Playlist')


def download_audio(audio_url, destino):
    try:
        # yt-dlp é mais compatível com as alterações recentes do YouTube
        opcoes = {
            'format': 'bestaudio/best',
            'outtmpl':  f'{destino}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
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


def download_playlist(playlist_url, destino):
    try:
        opcoes = {
            'format': 'bestaudio/best',
            'outtmpl': f'{destino}/%(title)s.%(ext)s',
            'noplaylist': False,
            'quiet': True,
            'playlist_items': '1:10',  # Baixa do item 1 ao 10
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': 192
            }]
        }

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([playlist_url])
            print("Download concluído!")

    except Exception as erro:
        print(f"Erro ao baixar o áudio: {erro}")


def download_video(video_url, destino):
    try:
        opcoes = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl':  f'{destino}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }]
        }

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([video_url])
            print("Download concluido!")
    except Exception as erro:
        print(f"Erro ao baixar o vídeo: {erro}")

if __name__ == '__main__':
    pastas = cria_pastas()
    if pastas:
        arquivo = ler_arquivo('musicas.csv')
        musica_list = converter_conteudo(arquivo)

        for index, url_dict in enumerate(musica_list):
            print('Baixando (%s/%s) ... %s' %
                  (index + 1, len(musica_list), url_dict['url']))

            if url_dict['tipo'] == 'audio':
                caminho = pegar_destino(url_dict['tipo'])
                download_audio(url_dict['url'], caminho)

            if url_dict['tipo'] == 'playlist':
                caminho = pegar_destino(url_dict['tipo'])
                download_playlist(url_dict['url'], caminho)

            if url_dict['tipo'] == 'video':
                caminho = pegar_destino(url_dict['tipo'])
                download_video(url_dict['url'], caminho)

            print('Finaizado a URL %s' % url_dict['url'])
