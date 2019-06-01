from bs4 import BeautifulSoup
from urllib import request, error


def wikipedia(input_artist):
    """
    Spotifyの表記からWikipediaの英語版にリンクされている日本語版のタイトルを取得する関数
    :param input_artist: Spotifyの表記(英語)
    :return: 日本語の表記
    """
    url_head = "https://en.wikipedia.org/wiki/"
    url = url_head + input_artist
    try:
        html = request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        li_ja = soup.find("li", class_="interlanguage-link interwiki-ja")
        a = li_ja.find("a")
        artist = a["title"].split(" – ")[0]
        # リンクされていたページが違う場合にはここで調整
        if artist == "スピッツ (バンド)":
            artist = "スピッツ"
    except error.HTTPError:
        artist = None
    except UnicodeEncodeError:
        artist = input_artist
    return artist


def artist_filer(artist):
    """
    wikipediaにリンクが無かった場合に調整する関数
    :param artist: Spotifyの表記(英語)
    :return: 日本語の表記
    """
    if artist == "Nogizaka46":
        filtered_artist = "乃木坂46"
    else:
        filtered_artist = artist
    return filtered_artist
