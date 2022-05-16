# Tello-Console
仲戸川式Telloクラスコントロールライブラリー
# 0.Download
ダウンロード環境は Ubuntu 20 を対象にしています。Windows でのダウンロードは今後サポート予定ですが、現在は推奨していません。
以下のコマンドをターミナルで実行してください。ホームディレクトリに追加されます。
  
ターミナルの立ち上げは、キーボードの Alt + Cntrl + T を押してください。
```bash
$ cd
$ git-clone https://github.com/GAI-313/Tello-Console.git
```
ホームディレクトリを確認し、ダウンロードが成功したかを確認してください
```bash
$ cd
$ ls
/Tello-Console <コレが表示されていたら成功
```
# 1.Try
　ダウンロードが完了したら、実際にドローンをPCに接続して、サンプルプログラムを実行してみましょう。
## 1.1 Tello EDU の WIFI に接続
1. Ubuntuのデスクトップ画面右上の WIFI マークをクリック
2. Select WI-FI もしくは WI-FI に接続…をクリック
3. TELLO- から始めるホスト名をクリック
4. Wi-Fi マークが？または接続マークが出たら成功
  
## 1.2 プログラムを実行
1. ターミナルでTello-Console ディレクトリに移動します。
```bash
$ cd Tello-Console
```
3. sample-Flight
