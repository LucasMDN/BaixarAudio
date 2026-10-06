import os
import yt_dlp
import re
import threading
from concurrent.futures import ThreadPoolExecutor


os.environ['PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT'] = '1'


def ler_arquivo(caminho):
    links = []
    with open(caminho, 'r') as file:
        links = file.readlines()

    return links


def Formato_csv_valdido(linha_csv):
    return True if len(linha_csv) == 3 else False


def tipo_suportado(tipo):
    return True if tipo in ['audio', 'video', 'playlist'] else False


def url_valida(url):
    padrao = r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+'
    return bool(url and re.search(padrao, url))


def veirifar_conteudo(dados):
    if not Formato_csv_valdido(dados):
        return False

    tipo = dados[0]
    if not tipo_suportado(tipo):
        return False

    url = dados[1]
    if not url_valida(url):
        return False

    return True


def converter_conteudo(lista_conteudo):
    arq_compativel = []
    arq_incompativel = []

    for item in lista_conteudo:
        item = item.strip()
        dados = item.split(';')

        dados_corretos = veirifar_conteudo(dados)

        if dados_corretos:
            if dados[0] == "playlist":
                url_dos_itens_da_playlist = obter_urls_da_playlist(dados[1])

                for playlist_item_url in url_dos_itens_da_playlist:
                    if url_valida(playlist_item_url):
                        arq_compativel.append({
                            'tipo': 'audio',
                            'url': playlist_item_url,
                            'destino': dados[2]
                        })

                    else:
                        arq_incompativel.append([dados[0], playlist_item_url])

            else:
                arq_compativel.append({
                    'tipo': dados[0],
                    'url': dados[1],
                    'destino': dados[2]
                })

        else:
            arq_incompativel.append([dados[0], dados[1]])

    if arq_incompativel:
        print('Não foi possível baixar os links:')
        for index, item in enumerate(arq_incompativel):
            print(f"{index+1} -- Tipo de Download: {item[0]} / Url: {item[1]}")
      

    return arq_compativel


def obter_urls_da_playlist(url):
    with yt_dlp.YoutubeDL({
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,    
        "playlist_items": "1-10"
    }) as ydl:
        info = ydl.extract_info(url, download=False)
        return [entrada["url"] for entrada in info["entries"]]


def download(url, tipo, destino, index, tamanho_lista):
    try:
        opcoes = config_download(tipo, destino)

        print(f"Baixando ({index+1}/{tamanho_lista}) --- {url}")

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
            print(f"Download número {index + 1} concluido!")



    except Exception as erro:
        print(f"Erro ao baixar o vídeo: {erro}")


def config_download(tipo, destino):
    
    opcoes = {
        "format": "bestvideo+bestaudio/best" if tipo == 'video' else "bestaudio/best",
        "outtmpl": f"{destino}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": False if tipo == 'playlist' else True
    }

    if tipo == 'playlist':
        opcoes['playlist_items'] = '1-10'

    if tipo == 'video':
        opcoes['postprocessors'] = [{
            'key': 'FFmpegVideoRemuxer',
            'preferedformat': 'mp4'
        }]

    else:
        opcoes['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]

    return opcoes


def cria_lista_download(arquivo):
    arquivo_csv = ler_arquivo(arquivo)
    lista_links = converter_conteudo(arquivo_csv)

    return lista_links


def chama_download(arquivo):
    lista_links = cria_lista_download(arquivo)
    tamanho_lista = len(lista_links)

    with ThreadPoolExecutor(max_workers=2) as executor:
        for index, dicionario_link in enumerate(lista_links):
            executor.submit(
                download,
                dicionario_link["url"],                
                dicionario_link["tipo"],
                dicionario_link["destino"],
                index,
                tamanho_lista   
            )
    

if __name__ == "__main__":
    chama_download('links.csv')
   
