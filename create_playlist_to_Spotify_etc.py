import lev_distance
import artist_filter


def create_playlist(search_data, api_data, similar_artist_list):
    s_artist = search_data[0]
    s_song = search_data[1]
    api_artist = api_data[0]
    api_artist = artist_filter.wikipedia(api_artist)
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
                result = "not"
    else:
        result = "not"
    return result
