#!/usr/bin/env python3
# coding=utf-8

from http.server import HTTPServer, BaseHTTPRequestHandler
import cv2, time, os

#コンフィグ
SLEEP = 0.3
SIZE = (600,400)
QUALITY = 30

camera = cv2.VideoCapture(0)

# Webサーバーのハンドラを定義 --- (*1)
class liveHTTPServer_Handler(BaseHTTPRequestHandler):
    # アクセスがあったとき
    def do_GET(self):
        time.sleep(SLEEP)

        print("path=",self.path)
        # 画像を送信する --- (*2)
        if self.path[0:7] == "/camera":
            # ヘッダ
            self.send_response(200)
            self.send_header('Cotent-Type', 'image/jpeg')
            self.end_headers()
            # フレームを送信
            _, frame = camera.read()
            img = cv2.resize(frame, SIZE)
            # JPEGにエンコード
            param = [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY]
            _, encimg = cv2.imencode('.jpg', img, param)
            self.wfile.write(encimg)
        # HTMLを送信する --- (*3)
        elif self.path == "/":
            # ヘッダ
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            # HTMLを出力
            try:
                #Daemonで動かすために絶対Path取得
                file = os.path.dirname(os.path.abspath(__file__)) + '/live.html'
                f = open(file, 'r', encoding='utf-8')
                s = f.read()
            except:
                s = "file not found"
            self.wfile.write(s.encode('utf-8'))
        else:
            self.send_response(404)
            self.wfile.write("file not found".encode('utf-8'))
try:
    # Webサーバーを開始 --- (*4)
    addr = ('', 8081)
    httpd = HTTPServer(addr, liveHTTPServer_Handler)
    print('サーバーを開始', addr)
    httpd.serve_forever()

except KeyboardInterrupt:
    httpd.socket.close()


