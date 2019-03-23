def convert_to_Spotify_fomat(similar_track):
    """
    last.fmの形式をSpotifyの形式に合うように調整する(表記の違いで上手く引っかからない時に調整する目的で使用)
    例:('AKB48', 'Aitakatta') → ('AKB48', '会いたかった')
    :param similar_track: 変換前 例:('AKB48', 'Aitakatta')
    :return: 変換後 例:('AKB48', '会いたかった')
    """
    if similar_track == ('AKB48', 'Aitakatta'):
        new_similar_track = ('AKB48', '会いたかった')
    else:
        new_similar_track = similar_track
    return new_similar_track

def convert_to_last_fm_format(recent_track):
    """
    Spotifyの形式をlast.fmの形式に変換する(既に聞いているのに上手く弾かれない場合に調整する目的で使用)
    :param recent_track: 変換前 例:('Nogizaka46', 'きっかけ')
    :return: 変換後 例:('乃木坂46', 'きっかけ')
    """
    if recent_track == ('Nogizaka46', 'きっかけ'):
        new_recent_track = ('乃木坂46', 'きっかけ')
    else:
        new_recent_track = recent_track
    return new_recent_track

# ('乃木坂46', '走れ！Bicycle') →　('乃木坂46', '走れ!Bicycle')