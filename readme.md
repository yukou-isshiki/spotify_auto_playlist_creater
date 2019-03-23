# このプログラムを使うにあたって

last.fm及びSpotifyのAPIに登録してキーを取得する必要があります。

## spotifyのAPIのローカルへの登録方法

spotifyのAPIの情報を".bash_profile"に記載する。

export SPOTIPY_CLIENT_ID=''　(userIDとは別)
export SPOTIPY_CLIENT_SECRET=''
export SPOTIPY_REDIRECT_URI='https://lastfm-playlist-generator-beta.herokuapp.com/'
(リダイレクト先はどこでも構いませんが、こちらでは以上のリダイレクト先を用意しています。)

## 初回認証方法

初回使用のみ認証が必要です。Spotify側の確認画面が出ます。また、ブラウザが開いてリダイレク
ト先のページが表示されます。そのURLをCLIの指定された位置に貼り付けてEnterを押して下さい。
