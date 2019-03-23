import lev_distance
import connect_watson_translate


def create_playlist(search_data, api_data, similar_artist_list):
    s_artist = search_data[0]
    s_song = search_data[1]
    api_artist = api_data[0]
    api_song = api_data[1]
    if api_artist == s_artist:
        print("アーティスト名完全一致")
        print("OK")
        result = "add"
    # 類似アーティストの中に含まれていた場合
    elif api_artist in similar_artist_list:
        # 曲名完全一致の場合は拾う
        if api_song == s_song:
            print("曲名完全一致")
            print("OK")
            result = "add"
        else:
            # 曲名の類似度が高ければ拾う
            song_word_distance = lev_distance.calc_distance(api_song, s_song)
            if song_word_distance < 6:
                print("曲名類似")
                print("OK")
                result = "add"
            else:
                not_append_song = (s_artist, s_song)
                result = "not"
    # 類似アーティスト内に含まれていない場合には、アーティスト名を翻訳
    else:
        api_artist = connect_watson_translate.translate_word(api_artist)
        artist_word_distance = lev_distance.calc_distance(api_artist, s_artist)
        song_word_distance = lev_distance.calc_distance(api_song, s_song)
        if artist_word_distance < 9 and song_word_distance < 9:
            print("アーティスト名類似")
            print("OK")
            result = "add"
        elif api_artist in similar_artist_list:
            print("アーティスト名類似")
            print("OK")
            result = "add"
        else:
            not_append_song = (s_artist, s_song)
            result = "not"
    return result