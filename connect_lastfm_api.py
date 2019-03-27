import urllib.request
import urllib.parse
import json
import time
import itemfilter

# 現在では不使用となったものも含まれる

user_name = "" # last.fmのデータを連携したいユーザー名

def get_search_song_list(artist, api_key, page):
    """
    アーティストごとの楽曲をlast.fmでの再生回数の多い順に取得する関数
    :param artist: 検索をかけたいアーティスト
    :param api_key: last.fmのAPIキー
    :param page: ページ
    :return: 楽曲のリスト
    """
    song_list = []
    artist = urllib.parse.quote(artist)
    artist_api1 = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist="
    artist_api2 = "&autocorrect=1&page="
    page = str(page)
    artist_api3 = "&api_key="
    artist_api4 = "&format=json"
    call_api = artist_api1 + artist + artist_api2 + page + artist_api3 + api_key + artist_api4
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    track = data["toptracks"]
    list = track["track"]
    for song in list:
        song = song["name"]
        song_list.append(song)
    return song_list

def get_similar_track(artist, song, api_key):
    """
    楽曲ごとに似ている楽曲の情報を取得する関数(不使用)
    :param artist: 検索をかけたいアーティスト
    :param song: 検索をかけたい楽曲
    :param api_key: last.fmのAPIキー
    :return: 似ている楽曲のリスト
    """
    similar_track_list = []
    first_track = (artist, song)
    similar_track_list.append(first_track)
    artist = urllib.parse.quote(artist)
    song = urllib.parse.quote(song)
    track_api1 = "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist="
    track_api2 = "&track="
    track_api3 = "&autocorrect=1&api_key="
    track_api4 = "&format=json"
    call_api = track_api1 + artist + track_api2 + song + track_api3 + api_key + track_api4
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    similartracks = data["similartracks"]
    track = similartracks["track"]
    print(track)
    for i in range(len(track)):
        list = track[i]
        match = list["match"]
        print(match)
        print(type(match))
        if match < 0.1:
            continue
        else:
            song = list["name"]
            similar_song_artist = list["artist"]["name"]
            similar_track = (similar_song_artist, song)
            similar_track_list.append(similar_track)
    return similar_track_list

def similar_artist_search(artist, api_key):
    """
    アーティストごとに似ているアーティストの情報を取得する関数(不使用)
    :param artist: 検索をかけたいアーティスト
    :param api_key: last.fmのAPIキー
    :return: アーティストのリスト
    """
    artist = urllib.parse.quote(artist)
    artist_api1 = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="
    artist_api2 = "&autocorrect=1&api_key="
    artist_api3 = "&format=json"
    call_api = artist_api1 + artist + artist_api2 + api_key + artist_api3
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    similarartists = data["similarartists"]
    artist_list = similarartists["artist"]
    list = artist_list[0]
    most_similar_artist = list["name"]
    return most_similar_artist

def recent_play_song(api_key):
    """
    指定した範囲内で再生された曲を取得する関数
    :param api_key: last.fmのAPIキー
    :return: 楽曲のリスト
    """
    now = time.time()
    recent = int(now) - 172800 # 現状は48時間で設定(1秒単位で変更可能)
    recent = str(recent)
    recent_api1 = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&limit=200&user="
    recent_api2 = "&from="
    recent_api3 = "&api_key="
    recent_api4 = "&format=json"
    call_api = recent_api1 + user_name + recent_api2 + recent + recent_api3 + api_key + recent_api4
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    recenttracks = data["recenttracks"]
    attr = recenttracks["@attr"]
    total = attr["total"]
    total = int(total)
    recent_api1 = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&limit="
    recent_api2 = "&user="
    recent_api3 = "&page="
    recent_api4 = "&from="
    recent_api5 = "&api_key="
    recent_api6 = "&format=json"
    if total < 201:
        total = str(total)
        totalpage = 1
    else:
        total = 200
        totalpage = attr["totalPages"]
        totalpage = int(totalpage)
        total = str(total)
    recent_track_list = []
    for i in range(totalpage + 1):
        count = i
        if count == 0:
            continue
        count = str(count)
        call_api = recent_api1 + total + recent_api2 + user_name + recent_api3 + count + recent_api4 + recent + recent_api5 + api_key + recent_api6
        print(call_api)
        address_json = urllib.request.urlopen(call_api)
        data = json.loads(address_json.read())
        try:
            recenttracks = data["recenttracks"]
            track = recenttracks["track"]
            for i in range(len(track)):
                list = track[i]
                artist = list["artist"]["#text"]
                song = list["name"]
                recent_track = (artist, song)
                recent_track = itemfilter.convert_to_last_fm_format(recent_track)
                if recent_track in recent_track_list:
                    continue
                else:
                    recent_track_list.append(recent_track)
        except KeyError:
            break
    return recent_track_list

def get_loved_track(api_key):
    """
    指定したユーザーの好きな楽曲を取得する関数
    :param api_key: last.fmのAPIキー
    :return: 好きな楽曲のリスト
    """
    loved_api1 = "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user="
    loved_api2 = "&api_key="
    loved_api3 = "&format=json"
    call_api = loved_api1 + user_name + loved_api2 + api_key + loved_api3
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    lovedtracks = data["lovedtracks"]
    attr = lovedtracks["@attr"]
    limit = attr["total"]
    limit_api = "&limit="
    call_api = loved_api1 + user_name + limit_api + limit + loved_api2 + api_key + loved_api3
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    lovedtracks = data["lovedtracks"]
    track = lovedtracks["track"]
    loved_list = []
    for i in range(len(track)):
        list = track[i]
        try:
            song = list["name"]
            artist = list["artist"]["name"]
            loved_data = (song, artist)
            loved_list.append(loved_data)
        except KeyError:
            continue
    return loved_list

def get_similar_artist_list(artist,api_key):
    """
    アーティストごとに似ているアーティストの情報を取得する関数
    :param artist: 検索をかけたいアーティスト
    :param api_key: last.fmのAPIキー
    :return: アーティストのリスト
    """
    artist = urllib.parse.quote(artist)
    artist_api1 = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="
    artist_api2 = "&autocorrect=1&api_key="
    artist_api3 = "&format=json"
    call_api = artist_api1 + artist + artist_api2 + api_key + artist_api3
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    try:
        similarartists = data["similarartists"]
        artist_list = similarartists["artist"]
        similar_artist_list = []
        for i in range(len(artist_list)):
            list = artist_list[i]
            similar_artist = list["name"]
            match = list["match"]
            match = float(match)
            if match < 0.1:
                continue
            else:
                artist_data = (similar_artist, match)
                similar_artist_list.append(artist_data)
        return similar_artist_list
    except KeyError:
        similar_artist_list = []
        return similar_artist_list

def generate_similar_track(artist, song, api_key):
    """
    楽曲ごとに似ている楽曲の情報を取得する関数(不使用)
    :param artist: 検索をかけたいアーティスト
    :param song: 検索をかけたい楽曲
    :param api_key: last.fmのAPIキー
    :return: 似ている楽曲のリスト
    """
    similar_track_list = []
    q_artist = urllib.parse.quote(artist)
    q_song = urllib.parse.quote(song)
    track_api1 = "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist="
    track_api2 = "&track="
    track_api3 = "&autocorrect=1&api_key="
    track_api4 = "&format=json"
    call_api = track_api1 + q_artist + track_api2 + q_song + track_api3 + api_key + track_api4
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    similartracks = data["similartracks"]
    track = similartracks["track"]
    for i in range(len(track)):
        list = track[i]
        match = list["match"]
        if match < 0.5:
            continue
        else:
            song = list["name"]
            similar_song_artist = list["artist"]["name"]
            similar_track = (similar_song_artist, song)
            similar_track_list.append(similar_track)
    if similar_track_list == []:
        artist_api1 = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="
        artist_api2 = "&autocorrect=1&api_key="
        artist_api3 = "&format=json"
        call_api = artist_api1 + q_artist + artist_api2 + api_key + artist_api3
        print(call_api)
        address_json = urllib.request.urlopen(call_api)
        data = json.loads(address_json.read())
        try:
            similarartists = data["similarartists"]
            artist_list = similarartists["artist"]
            similar_track_dict = {}
            v_dict = {}
            for list in artist_list:
                similar_artist = list["name"]
                artist_match = float(list["match"])
                if artist_match < 0.5:
                    break
                else:
                    q_artist = urllib.parse.quote(similar_artist)
                    artist_api1 = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist="
                    artist_api2 = "&autocorrect=1&page="
                    page = str(1)
                    artist_api3 = "&api_key="
                    artist_api4 = "&format=json"
                    call_api = artist_api1 + q_artist + artist_api2 + page + artist_api3 + api_key + artist_api4
                    print(call_api)
                    address_json = urllib.request.urlopen(call_api)
                    data = json.loads(address_json.read())
                    track = data["toptracks"]
                    list = track["track"]
                    top_count = int(list[0]["listeners"])
                    for songs in list:
                        song = songs["name"]
                        similar_track = (similar_artist, song)
                        count_int = (int(songs["listeners"]) / top_count)
                        all_match = count_int * artist_match
                        if all_match > 0.5:
                            similar_track_dict[similar_track] = all_match
                        else:
                            break
            v_list = []
            for k, v in similar_track_dict.items():
                v_list.append(v)
            v_list.sort()
            v_list.reverse()
            for k2, v2 in similar_track_dict.items():
                v_index =  v_list.index(v2)
                v_dict[k2] = v_index
            p = sorted(v_dict.items(), key=lambda x:x[1])
            for q in p:
                similar_track_list.append(q[0])
        except KeyError:
            similar_track_list = []
    print(similar_track_list)
    return similar_track_list


def get_top_artist(api_key):
    """
    アーティストごとにlast.fmで一番再生されている曲の情報を取得する関数
    :param api_key: last.fmのAPIキー
    :return: 一番再生されている曲の情報
    """
    top_artist_api1 = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="
    top_artist_api2 = "&api_key="
    top_artist_api3 = "&format=json"
    call_api = top_artist_api1 + user_name + top_artist_api2 + api_key + top_artist_api3
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    artists = data["topartists"]["artist"]
    top_artist_list = []
    for artist_data in artists:
        artist = artist_data["name"]
        top_artist_list.append(artist)
    return top_artist_list


def create_playlist(q, api_key, similar_track_data_dict, remove_list, count, playlist_size, original_match,
                        remove_artist, q_list):
    """
    投げられたqueryからプレイリストを生成する関数
    :param q: アーティストと楽曲
    :param api_key: last.fmのAPIキー
    :param similar_track_data_dict: 類似曲を格納するdict
    :param remove_list: 既に再生された曲など、プレイリストに含めない楽曲のリスト
    :param count: ループ回数
    :param playlist_size: プレイリストに含める曲の上限
    :param original_match: 投げたqueryの係数
    :param remove_artist: 嫌いなアーティスト
    :param q_list: 既に投げられたqueryのリスト
    :return: 生成されたプレイリスト
    """
    if playlist_size <= len(similar_track_data_dict):
        return similar_track_data_dict
    q = itemfilter.convert_to_Spotify_fomat(q)
    q_list.append(q)
    if similar_track_data_dict == {}:
        first_track = (1.1, q)
        similar_track_data_dict[q] = 1.1
        remove_list.append(q)
    artist = urllib.parse.quote(q[0])
    song = urllib.parse.quote(q[1])
    track_api1 = "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist="
    track_api2 = "&track="
    track_api3 = "&autocorrect=1&api_key="
    track_api4 = "&format=json"
    call_api = track_api1 + artist + track_api2 + song + track_api3 + api_key + track_api4
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    track_list = data["similartracks"]["track"]
    for tracks in track_list:
        if tracks["match"] * original_match < 0.1:
            break
        else:
            song = tracks["name"]
            artist = tracks["artist"]["name"]
            track_match = tracks["match"] * original_match
            track = (artist, song)
            track = itemfilter.convert_to_Spotify_fomat(track)
            if track in remove_list:
                continue
            elif artist in remove_artist:
                continue
            elif similar_track_data_dict.get(track) != None and track_match < similar_track_data_dict.get(track):
                continue
            else:
                remove_list.append(track)
                track_data = (track_match, track)
                similar_track_data_dict[track] = track_match
    print(similar_track_data_dict)
    sorted_list = sorted(similar_track_data_dict.items(), key=lambda x:x[1], reverse=True)
    new_dict = {}
    for sort in sorted_list:
        new_dict[sort[0]] = sort[1]
    print(new_dict)
    if count < 6:
        next_que = None
        match = None
        print(new_dict.items())
        for queries in new_dict.items():
            print(queries)
            match = queries[1]
            if queries[0] in q_list:
                continue
            else:
                next_que = queries[0]
                count = count + 1
                break
        print(next_que)
        if next_que != None:
            new_dict = create_playlist(next_que, api_key, new_dict, remove_list, count, playlist_size, match,
                                       remove_artist, q_list)
        else:
            similar_artist_list = get_similar_artist_list(q[0], api_key)
            similar_artist = None
            artist_match = None
            for artist_data in similar_artist_list:
                similar_artist = artist_data[0]
                artist_match = artist_data[1]
                if similar_artist in remove_artist:
                    continue
                else:
                    break
            song_list = create_similar_song_list(similar_artist, api_key, 1)
            song_match = None
            track = None
            for songs in song_list:
                song = songs[0]
                track = (similar_artist, song)
                track = itemfilter.convert_to_Spotify_fomat(track)
                if track in remove_list:
                    continue
                else:
                    song_match = songs[1]
                    break
            next_match = artist_match * song_match
            remove_list.append(track)
            track_data = (next_match, track)
            new_dict[track] = next_match
            print(new_dict)
            new_dict = create_playlist(track, api_key, new_dict, remove_list, count, playlist_size, next_match,
                                       remove_artist, q_list)
    else:
        print(new_dict)
    return new_dict


def create_similar_song_list(artist, api_key, page):
    """
    アーティストごとに似ているアーティストの情報を取得する関数(create_playlistでデータが出てこなかった時にのみ使用)
    :param artist: 検索をかけたいアーティスト
    :param api_key: last.fmのAPIキー
    :param page: ページ
    :return: アーティストのリスト
    """
    song_list = []
    artist = urllib.parse.quote(artist)
    artist_api1 = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist="
    artist_api2 = "&autocorrect=1&page="
    page = str(page)
    artist_api3 = "&api_key="
    artist_api4 = "&format=json"
    call_api = artist_api1 + artist + artist_api2 + page + artist_api3 + api_key + artist_api4
    print(call_api)
    address_json = urllib.request.urlopen(call_api)
    data = json.loads(address_json.read())
    song_list = data["toptracks"]["track"]
    top_match = int(song_list[0]["listeners"])
    similar_song_list = []
    for songs in song_list:
        song = songs["name"]
        song_match = int(songs["listeners"]) / top_match
        data = (song, song_match)
        similar_song_list.append(data)
    return similar_song_list