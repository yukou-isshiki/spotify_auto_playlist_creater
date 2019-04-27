# このプログラムについて

このプログラムはユーザー自身がSpotifyで聴いている曲から自動でプレイリストを生成し、生成したプレイリストを自動再生するプログラムです。

# 書籍について

このプログラムの開発に関する事は、技術書典6にて頒布した「CoLabユーザーで技術書を書いてみた」にまとめられています。

## 書籍との差分

現在無し

# このプログラムの構成

※ カスタマイズ可能となっているファイルは、ユーザー個人で追加していく事を想定しています

* auto_create_playlist.py メインファイル
* artist_filter.py Spotifyのアーティスト表記を日本語化するためのファイル(一部カスタマイズ可能)
* connect_lastfm_api.py Last.fmに接続するためのファイル
* connect_watson_translate.py watsonのAPIに送って翻訳するファイル
* create_playlist_to_Spotify_etc.py SpotifyのAPIから受け取った曲のデータをプレイリストに追加するかを判定するファイル
* dislike_artist_list.py 嫌いなアーティストを入れておくファイル(カスタマイズ可能)
* itemfilter.py 表記の差異で上手く動作しない場合に使うファイル(カスタマイズ可能)
* lev_distance.py レーベンシュタイン距離の比較ファイル
* spotify_token.py SpotifyのAPIを使う時にトークンを発行するファイル

# このプログラムを使うにあたって

Last.fm及びSpotify、IBM cloudのAPIに登録してキーを取得する必要があります。

## spotifyのAPIのローカルへの登録方法

spotifyのAPIの情報を".bash_profile"に記載する。

export SPOTIPY_CLIENT_ID=''　(userIDとは別)  
export SPOTIPY_CLIENT_SECRET=''  
export SPOTIPY_REDIRECT_URI='https://lastfm-playlist-generator-beta.herokuapp.com/'  
(リダイレクト先はどこでも構いませんが、こちらでは以上のリダイレクト先を用意しています。)

## ファイルにAPIキー等を記述する場所

* spotifyのユーザー名・Last.fmのAPIキー
** auto_create_playlist.py

* Last.fmのユーザー名
** connect_lastfm_api.py

* watsonのユーザー名とパスワード
** connect_watson_translate.py

## 初回認証方法

初回使用のみ認証が必要です。Spotify側の確認画面が出ます。また、ブラウザが開いてリダイレク
ト先のページが表示されます。そのURLをCLIの指定された位置に貼り付けてEnterを押して下さい。
