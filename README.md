# 0. Introduction
このライブラリは DJI tello-SDK を参考にカスタマイズされた tello EDU 向け SDK である。Tello-Console（以下本ライブラリ）は tello-sdk より簡易的にプログラムを記述でき、各問題のソリューションをターミナル上でフィードバクできる機能を持っている。加えて、tello-sdk で必要だった H264 コーデックを不要とし、環境構築も簡単に済ませることができる。<br>
このプログラムは高頻度でアップデートされる要諦なので、定期的にアップデート確認を行なってください。詳しくは本人に連絡してください
# 1.Download
本ライブラリは以下の環境をサポートしています。
- ubuntu
- macOS

windows での動作はサポートしていません。
<br>
次に、本ライブラリを動作させるのに必要なツールを紹介します。前提条件として、
- LINUX コマンドを理解している
- python3 がインストールされている
- openCV がインストールされている
- Numpy がインストールされている

python3 がインストールされているかどうかは、以下のコマンドで確認できます。
```bash
$ python3 -V
```
このうち、openCV, Numpy がインストールされていない場合は、[こちら][1]を参照してインストールしてください。
<br>
そしたら、以下のコマンドで本ライブラリをインストールしましょう！
<br>**このコマンドを実行すると、既存のカレントディレクトリにデータが上書きされます。もし以前にこのコマンドを実行し、Tello-Console ディレクトリ内に何かプログラムを作っているなら、他のディレクトリにバックアップを作成することを強く勧めます！！！**<br>本ライブラリは常に更新されます。詳しくは**リリースノート**を参照してください。
```bash
$ cd ~
$ git clone https://github.com/GAI-313/Tello-console.git
```
これでダウンロードは完了です！試しに Tello を飛ばしてみましょう！
# 2.Flight
## 2-1.Connection
本ライブラリで正常に tello が飛行できるかどうか確かめるのに最適な方法は、sample_flight を実行することです。その前に tello を PC に説お↑雨する方法を説明をしましょう。以下の手順で Tello に接続します。<br>
1. Tello 右側にある電源ボタンを一回押す
2. Tello 前方カメラ横の LED が黄色に点滅していることを確認する
3. PC の Wifi 設定を開いて TELLO- から始まるアドレスに接続する。
## 2-2.Execute
PC が Tello と Wifi で接続できたら、ターミナルを開いて以下のコマンドを実行してください。
```bash
$ cd Tello-Console #ディレクトリに移動
$ python3 sample_flight.py #実行プログラム
```
これでドローンが飛行したら成功です！
## 2-3.issues & solves
以下のエラーが出た場合は、ドローンとの接続が確立されていません。Wifi で Tello が接続されているか確認してください。もしくは再度実行してみてください。
```bash
send command >>> command: response >>> None response
警告：レスポンスエラー。タスクが正常に機能しませんでした。
接続エラー：ドローンに接続されていません。
ヒント：Wi-Fiでドローンに接続してください。
```
以下のエラーが出た場合は、tello のバッテリー残量が 10% 以下の時に発生します。 tello のバッテリーを充電してください。
```bash
```
以下のエラーが出た場合は、tello 内で重大なエラーが発生した際に起こります。tello を再起動して再実行してください。
```bash
```
以下のエラーが出た場合は、本ライブラリを動かすのに必要なモジュールが足りません。**1.Downliad** セクションに戻ってライブラリの確認を行なってください
```bash
importError: ~~~
```
## 2-4.Commentary
プログラムを実行すると、ターミナル内に分裂がわちゃわちゃ出てくるかと思います。これは本ライブラリと tello とのやりとりをログとして表示しているのです。そして何か問題が発生したらどんな問題が起きたのか、その解決方法は何かを示してくれる重要な要素です。ドローンとのやり取りは以下のように記述されます。
```bash
send command >>> tello に送信した命令: response >>> その命令を送った際の tello からの応答
```
プログラム実行中に表示されるのは、他に警告、エラー文があります。以下のように重要度が区別されます。
```bash
警告：黄色で表示される。プログラムは継続して実行されるが、シークエンスに問題がある可能性がある。もしくは引数の許容値を超えてしまった場合。
エラー：赤色で表示される。一部は継続してプログラムが継続されるが、tello または実行プログラムに何か問題がある。重大なエラーが発生したら強制的にプログラムが停止し、飛行中の tello は自動着陸する。
解決可能なエラーの場合はヒントが表示される。
```
ターミナル内に表示されるログはドローンの動きをその場で認知できるため、プログラム実行時には tello とこのログを確認してプログラムの進捗を見守るのが良いでしょう。

[1]:https://avinton.com/academy/opencv4-5-1-python3-8-ubuntu20-04-install/