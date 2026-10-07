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


def criar_lista_com_todas_as_urls(caminho_arquivo):
    lista_de_download = []
    arquivo = ler_arquivo(caminho_arquivo)
    for lista_de_informacoes in arquivo:
        lista_de_informacoes = lista_de_informacoes.strip().split(";")

        tipo = lista_de_informacoes[0]
        url = lista_de_informacoes[1]
        destino = lista_de_informacoes[2]

        if tipo == "playlist":
            urls_isoladas = obter_urls_da_playlist(url)
            for url_isolada in urls_isoladas:
                lista_de_download.append([
                    tipo,
                    url_isolada,
                    destino
                ])

        else:
            lista_de_download.append([
                tipo,
                url,
                destino
            ])

    return lista_de_download


def converter_lista_de_url_para_dicionario(lista_de_donwload):
    arq_compativel = []
    arq_incompativel = []

    for item in lista_de_donwload:
        dados_corretos = veirifar_conteudo(item)

        if dados_corretos:
            arq_compativel.append({
                'tipo': item[0],
                'url': item[1],
                'destino': item[2]
            })

        else:
            arq_incompativel.append([item[0], item[1]])

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
            #ydl.download([url])
            print(f"Download número {index + 1} concluido!")



    except Exception as erro:
        print(f"Erro ao baixar o vídeo: {erro}")


def config_download(tipo, destino):
    
    opcoes = {
        "format": "bestvideo+bestaudio/best" if tipo == 'video' else "bestaudio/best",
        "outtmpl": f"{destino}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True
    }

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


def cria_lista_download(caminho_arquivo):
    lista_completa_de_ownloads = criar_lista_com_todas_as_urls(caminho_arquivo)
    dicionario_download = converter_lista_de_url_para_dicionario(lista_completa_de_ownloads)

    return dicionario_download


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
   
