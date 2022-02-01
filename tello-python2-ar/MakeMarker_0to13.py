#!/usr/bin/env python
# -*- coding: utf-8 -*-

#ARマーカーを生成するプログラム

import cv2 #画像処理用のライブラリであるOpenCVを導入
aruco = cv2.aruco #OpenCV2の中にあるARマーカーのライブラリarucoを呼び出し、変数arucoに格納。

#あらかじめ定義されている辞書を使ってdictionaryオブジェクトを作成。マーカーのサイズが6X6,マーカーのビット数が50。
dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)

def main():
    for i in range(14):
        # 第一引数は上記で定義したdictionary。第二引数はID名。第三引数は縦横のサイズ。
        ar_image = aruco.drawMarker(dictionary,i,150) 

        fileName = "ar" + str(i).zfill(2) + ".png" #zfill(2)はカウンタ変数iが2桁未満なら数字をゼロ埋めする。
        cv2.imwrite(fileName, ar_image) #マーカー画像を保存する

# "python MakeMarker_0to11.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":
    main()