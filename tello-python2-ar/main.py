#!/usr/bin/env python
# -*- coding: utf-8 -*-

#ARマーカーを認識してTelloを動かすプログラム
#Python2の環境がないと動かない

import tello  #tello.pyをインポートする
import time   #time.sleepを使用する為にインポート
import cv2    #OpenCVを使うためにインポート

def main():
    aruco = cv2.aruco
    #画像生成側と画像読み込み側で同じ辞書を使う必要がある。
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_50) #有効なIDを50個生成
    #tello.pyのTelloクラスを呼び出し、インスタンスを生成。
    drone = tello.Tello('', 8889, command_timeout=.01)
    #現在のエポック秒を取得し、current_timeに代入
    current_time = time.time()
    #5秒ごとのコマンド送信をする為に使う
    pre_time  = current_time

    time.sleep(0.5) #0.5秒間処理を停止する。

    pre_idno = None #前回のIDを記憶する変数。
    count = 0 #同じID番号が見えた回数を記憶する変数。

    #Ctrl+cが押されるまでループ

    try: #Pythonの例外処理をキャッチする文（try,except）
        while True: #例外処理が発生するまでループを繰り返す
            #(A)画像取得する
            frame = drone.read() #映像を1フレーム取得
            if frame is None or frame.size == 0:    # 中身がおかしかったら無視。（映像フレームが取得できなかった or 映像フレームのサイズが0だった場合）
                continue 

            # (B)ここから画像処理
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)      # 取得した映像フレームをOpenCV用のカラー並びに変換する
            small_image = cv2.resize(image, dsize=(480,360) )   # 画像サイズを指定したサイズに変更

            # ARマーカーの検出と，枠線の描画

            #cornersはマーカーの四隅の点, idsは取得したID番号, rejectedImgPointsは解析できないポイント
            #aruco.detectMarkers(リサイズした画像, 冒頭で作成したdictionary)は引数を基にマーカーを検出する
            corners, ids, rejectedImgPoints = aruco.detectMarkers(small_image, dictionary)

            aruco.drawDetectedMarkers(small_image, corners, ids, (0,255,0)) #検出したマーカ情報を元に，元の画像に描画する


            # 30回同じマーカーが見えたらコマンド送信する処理

            try:
                if ids != None: # idsが空(マーカーが１枚も認識されなかった)じゃなければ処理
                    idno = ids[0,0] # idsには複数のマーカーが入っているので，0番目のマーカーを取り出す

                    if idno == pre_idno:    # 今回認識したidnoが前回のpre_idnoと同じ時には処理
                        count+=1            # 同じマーカーが見えてる限りはカウンタを増やす

                        if count > 20:      # 同じマーカーが20回超えたら，コマンドを確定する
                            #変数の文字列が整数ならば符号付き10進数で出力する
                            print("ID:%d"%(idno)) #%記法を使って出力（C言語などでよく使われる）

                            if idno == 0:
                                drone.takeoff()             # 離陸
                            elif idno == 1:
                                drone.land()                # 着陸
                                time.sleep(3)
                            elif idno == 2:
                                drone.move_up(0.3)          # 上昇
                            elif idno == 3:
                                drone.move_down(0.3)        # 下降
                            elif idno == 4:
                                drone.rotate_ccw(20)        # 左旋回
                            elif idno == 5:
                                drone.rotate_cw(20)         # 右旋回
                            elif idno == 6:
                                drone.move_forward(0.3)     # 前進
                            elif idno == 7:
                                drone.move_backward(0.3)    # 後進
                            elif idno == 8:
                                drone.move_left(0.3)        # 左移動
                            elif idno == 9:
                                drone.move_right(0.3)       # 右移動
                            elif idno == 10:
                                drone.flip('f')             #前回転
                            elif idno == 11:
                                drone.flip('r')             #右回転
                            elif idno == 12:
                                drone.flip('b')             #後回転
                            elif idno == 13:
                                drone.flip('l')             #左回転

                            count = 0   # コマンド送信したらカウント値をリセット
                    else:
                        count = 0

                    pre_idno = idno # 前回のpre_idnoを更新する
                else:
                    count = 0   # 何も見えなくなったらカウント値をリセット

            except ValueError as e:   # if ids != None の処理で時々エラーが出るので，try exceptで捕まえて無視させる
                print("ValueError")


            # (X)ウィンドウに表示
            cv2.imshow('OpenCV Window', small_image)    # ウィンドウに表示するイメージを変えれば色々表示できる

            # (Y)OpenCVウィンドウでキー入力を1m秒待つ
            key = cv2.waitKey(1)
            if key == 27:
                break

            # (Z)5秒おきに'command'を送る
            current_time = time.time()  # 現在時刻を取得
            if current_time - pre_time > 5.0 :  # 前回時刻から5秒以上経過しているか判断
                drone.send_command('command')   # 'command'送信
                pre_time = current_time         # 前回時刻を更新

    except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
    #上記の例外キャッチ処理のインデント間違えると処理を止めることができなくなる恐れがある
        print( "プログラムの実行を終了します" )

    # telloクラスを削除
    #次回以降プログラムを実行した時droneが不可解な動作をしないように
    del drone


# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":      # importされると"__main__"は入らないので，実行かimportかを判断できる．
    main()    # メイン関数を実行
    
