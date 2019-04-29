import spotipy
import connect_lastfm_api
import dislike_artist_list
import create_playlist_to_Spotify_etc
import re
import artist_filter
import error_class
from spotify_token import Spotify_token

api_key =  "" # last.fmのAPIキー
username = "" # SpotifyのユーザーID

def get_current_playing_track():
    """
    Spotifyから現在再生されている曲の情報を取得し、lastfmのAPIに送れるように情報を加工する
    """
    result = sp.current_user_playing_track() # 現在再生中の楽曲情報を取得
    spotify_artist = result['item']['artists'][0]['name'] # 楽曲情報からアーティストを取得
    print(spotify_artist)
    artist = artist_filter.wikipedia(spotify_artist) # 英語版wikipediaからリンクされている日本語ページのタイトルを取得
    if artist == None:
        artist = artist_filter.artist_filer(spotify_artist) # リンクが無かった場合には、個別に翻訳設定
    song = result['item']['name']
    print(artist)
    yes_or_no = input("これで正しいですか？(y/n)") # アーティストの翻訳結果が正しいか確認
    if yes_or_no == "y":
        print(song)
        create_playlist(artist, song)
    else:
        print("end")

def create_playlist(artist, song):
    """
    受け取った楽曲情報をもとにプレイリストを作成する
    """
    playlist = []
    count = 0 # 無限にループを防ぐための変数
    playlist_limit = 15 # プレイリストに入れる最大曲数
    q = (artist, song)
    similar_track_data_dict = {}
    remove_artist = dislike_artist_list.dislike_artist() # 嫌いなアーティストの登録(オプション機能)
    remove_list = connect_lastfm_api.recent_play_song(api_key) # 直近で聞いた曲など
    q_list = [] # 一度検索した曲の再検索を防ぐ
    track_dict = connect_lastfm_api.create_playlist(q, api_key, similar_track_data_dict, remove_list, count,
                                                    playlist_limit, 1.0, remove_artist, q_list)
    try:
        if track_dict == {}:
            raise error_class.NoTrackError
        print(track_dict)
        for track in track_dict:
            playlist.append(track)
            if len(playlist) == playlist_limit:
                break
        print(playlist)
        get_empty_Spotify_playlist(playlist)
    except error_class.NoTrackError:
        print("楽曲名が間違っているか、再生数が極端に少ないためDBに登録されていない可能性があります")

def get_empty_Spotify_playlist(playlist):
    """
    Spotifyで新規にプレイリストを作成し、Spotifyで再生可能な曲を抽出する
    """
    playlist_name = f"{playlist[0][0]}の{playlist[0][1]}から始まるおすすめプレイリスト" # Spotifyのプレイリスト名
    playlistts = sp.user_playlist_create(username, playlist_name)
    playlist_id = playlistts["id"]
    print(playlist_id)
    song_ids = []
    not_append_list = []
    for i in range(len(playlist)):
        if i == 0:
            current_track = sp.current_user_playing_track()
            song_id = current_track['item']['id']
            song_ids.append(song_id)
        else:
            search_str = playlist[i]
            s_artist = search_str[0]
            s_song = search_str[1]
            search_str = s_artist + " " + s_song # SpotifyのAPIに投げるqueryの作成
            result = sp.search(search_str, limit=1, market="JP")
            tracks = result["tracks"]
            items = tracks["items"]
            similar_artist_list = connect_lastfm_api.get_similar_artist_list(s_artist, api_key)
            if items == []: # 0件ヒット
                not_append_song = (s_artist, s_song)
                not_append_list.append(not_append_song)
                continue
            api_artist = items[0]["album"]["artists"][0]["name"]
            print(api_artist)
            api_song = items[0]["name"]
            api_song = re.sub("\t", "", api_song)
            song_id = items[0]["id"]
            print(api_song)
            search_data = (s_artist, s_song)
            api_data = (api_artist, api_song)
            result = create_playlist_to_Spotify_etc.create_playlist(search_data, api_data,
                                                                    similar_artist_list)  # 拾った曲の真偽判定
            if result == "add":
                song_ids.append(song_id)
            else:
                not_append_song = (s_artist, s_song)
                not_append_list.append(not_append_song)
    Spotify_playlist_input(playlist_id, song_ids, not_append_list)


def Spotify_playlist_input(playlist_id, song_ids, not_append_list):
    """
    抽出された曲をSpotifyのプレイリストに投入する
    """
    if token:
        results = sp.user_playlist_add_tracks(username, playlist_id, song_ids)
        print(results)
        if len(not_append_list) != 0:
            print("以下の曲はSpotifyで配信されていません")
            for not_list_song in not_append_list:
                print(not_list_song)
        Spotify_auto_start_playlist(playlist_id, song_ids)
    else:
        print("Can't get token for", username)

def Spotify_auto_start_playlist(playlist_id, song_ids):
    """
    実際に作成したプレイリストを再生する
    """
    result = sp.devices()
    device_id_list = result['devices']
    for device_ids in device_id_list:
        print(device_ids)
        device_id = device_ids['id']
        if device_ids['is_active'] == True: # 現在再生中の機器を抽出
            break
        else:
            continue
    context_uri = "spotify:playlist:" + playlist_id
    sp.pause_playback(device_id) # 一旦曲を停止
    current_track = sp.current_user_playing_track()
    print(current_track)
    song_id = current_track['item']['id']
    if song_id == song_ids[0]: # プレイリストの先頭と同じ場合は再生位置を修正
        progress_ms = current_track['progress_ms'] - 500
    else:
        progress_ms = 0
    sp.start_playback(device_id, context_uri, position_ms=progress_ms) # 指定した位置からプレイリストを再生


ST = Spotify_token(username)
token = ST.set()
sp = spotipy.Spotify(auth=token)
get_current_playing_track()