import tkinter as tk #GUIライブラリ
import datetime
import configparser #confファイルを読む
import urllib.request
from bs4 import BeautifulSoup
import re

import tkinter.ttk as ttk #GUIライブラリのラジオボタン用

import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #カレントディレクトリをファイルのあるディレクトリに設定(画像ファイルをよむため)

ini = configparser.ConfigParser() #設定ファイルを読み込み
ini.read('setting.ini')

#対象のサイトURL
url = ini['setting']['url']

#URLリソースを開く
res = urllib.request.urlopen(url)

#インスタンスの作成
soup = BeautifulSoup(res, 'html.parser')

#メインウインドウ設定
root = tk.Tk()
root.title('ゴミ出しダッシュボード')
root.geometry("440x300")
root.configure(bg='#fff')

#フォント設定
mainfont = (ini['setting']['font'], '15', "bold")

#画像を読み込んでおく
trash = tk.PhotoImage(file="images/s-可燃ごみ.png")
noburn = tk.PhotoImage(file="images/s-不燃ごみ.png")
paper = tk.PhotoImage(file="images/s-紙類.png")
bottle = tk.PhotoImage(file="images/s-ビン類.png")
can = tk.PhotoImage(file="images/s-缶.png")
pet = tk.PhotoImage(file="images/s-ペットボトル.png")
tube = tk.PhotoImage(file="images/s-蛍光管.png")
title = tk.PhotoImage(file="images/title.png")
nothing = tk.PhotoImage(file="images/s-なし.png")

#タイトル画像設定
tcanvas = tk.Canvas(root, bg="#FFFFFF", width=300, height=43, highlightbackground="#fff")
tcanvas.place(x=5, y=5)
tcanvas.create_image(0, 0, image=title, anchor=tk.NW)

label1 = tk.Label(root, text = "きょう　　　     あす　     　　あさって", bg="#FFFFFF" ,font=mainfont)
label1.place(x=45,y=50)

todaycanvas = tk.Canvas(root, bg="#FFFFFF", width=130, height=200, highlightbackground="#fff")
todaycanvas.place(x=10, y=80)
todaycanvas.create_image(5, 5, image=nothing, anchor=tk.NW)

tomorrowcanvas = tk.Canvas(root, bg="#FFFFFF", width=130, height=200, highlightbackground="#fff")
tomorrowcanvas.place(x=150, y=80)
tomorrowcanvas.create_image(5, 5, image=nothing, anchor=tk.NW)

dftomorrowcanvas = tk.Canvas(root, bg="#FFFFFF", width=130, height=200, highlightbackground="#fff")
dftomorrowcanvas.place(x=290, y=80)
dftomorrowcanvas.create_image(5, 5, image=trash, anchor=tk.NW)

def changeimage(n,t):
  if t==0:
    if n==1: todaycanvas.create_image(5, 5, image=trash, anchor=tk.NW)
    if n==2: todaycanvas.create_image(5, 5, image=bottle, anchor=tk.NW)
    if n==3: todaycanvas.create_image(5, 5, image=paper, anchor=tk.NW)
    if n==4: todaycanvas.create_image(5, 5, image=can, anchor=tk.NW)
    if n==5: todaycanvas.create_image(5, 5, image=pet, anchor=tk.NW)
    if n==6: todaycanvas.create_image(5, 5, image=tube, anchor=tk.NW)
    if n==7: todaycanvas.create_image(5, 5, image=noburn, anchor=tk.NW)
    if n==8: todaycanvas.create_image(5, 5, image=nothing, anchor=tk.NW)
  if t==1:
    if n==1: tomorrowcanvas.create_image(5, 5, image=trash, anchor=tk.NW)
    if n==2: tomorrowcanvas.create_image(5, 5, image=bottle, anchor=tk.NW)
    if n==3: tomorrowcanvas.create_image(5, 5, image=paper, anchor=tk.NW)
    if n==4: tomorrowcanvas.create_image(5, 5, image=can, anchor=tk.NW)
    if n==5: tomorrowcanvas.create_image(5, 5, image=pet, anchor=tk.NW)
    if n==6: tomorrowcanvas.create_image(5, 5, image=tube, anchor=tk.NW)
    if n==7: tomorrowcanvas.create_image(5, 5, image=noburn, anchor=tk.NW)
    if n==8: tomorrowcanvas.create_image(5, 5, image=nothing, anchor=tk.NW)
  if t==2:
    if n==1: dftomorrowcanvas.create_image(5, 5, image=trash, anchor=tk.NW)
    if n==2: dftomorrowcanvas.create_image(5, 5, image=bottle, anchor=tk.NW)
    if n==3: dftomorrowcanvas.create_image(5, 5, image=paper, anchor=tk.NW)
    if n==4: dftomorrowcanvas.create_image(5, 5, image=can, anchor=tk.NW)
    if n==5: dftomorrowcanvas.create_image(5, 5, image=pet, anchor=tk.NW)
    if n==6: dftomorrowcanvas.create_image(5, 5, image=tube, anchor=tk.NW)
    if n==7: dftomorrowcanvas.create_image(5, 5, image=noburn, anchor=tk.NW)
    if n==8: dftomorrowcanvas.create_image(5, 5, image=nothing, anchor=tk.NW)


def check():
  mydict = {"燃えるごみ":1, 
  "びん類":2, 
  "紙類":3,
  "缶":4,
  "ペットボトル類・白トレイ":5,
  "蛍光管・スプレー類":6,
  "燃えないごみ":7,
  "桐生市清掃センター受入日":8 }
  today = datetime.datetime.today() +  datetime.timedelta(days=0)
  tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
  dftomorrow = datetime.datetime.today() + datetime.timedelta(days=2)
  root.after(60000, check)
  for i in range(2):
    text = soup.find_all('table', class_="gomi")[i]
    data = text.find_all('td')
    for j in range(len(text.find_all('td'))-1):
      if data[j].find('ul') is not None and data[j].find('ul').find('li') is not None:
        #print(re.search(r'\d+', data[j].find('strong').text).group() + "日: " + str(data[j].find('ul').find('li').text.replace( '\n' , '' )) + "\n")
        if re.search(r'\d+', data[j].find('strong').text).group() == str(today.day) and text.find('caption').find('span').text == str(today.month) + '月':
          changeimage(mydict[str(data[j].find('ul').find('li').text.replace( '\n' , '' ))],0)
        if re.search(r'\d+', data[j].find('strong').text).group() == str(tomorrow.day) and text.find('caption').find('span').text == str(tomorrow.month) + '月':
          changeimage(mydict[str(data[j].find('ul').find('li').text.replace( '\n' , '' ))],1)
        if re.search(r'\d+', data[j].find('strong').text).group() == str(dftomorrow.day) and text.find('caption').find('span').text == str(dftomorrow.month) + '月':
          changeimage(mydict[str(data[j].find('ul').find('li').text.replace( '\n' , '' ))],2)


#画像変更関数はここで呼び出し
check()

# メインループ
root.mainloop()

''' #ここから先参考コード
text = soup.find('table', class_="gomi")
print(text.find('caption').find('span').text + "のカレンダー\n");

data = text.find_all('td')
for i in range(len(text.find_all('td'))-1):
  if data[i].find('ul') is not None and data[i].find('ul').find('li') is not None:
    print(str(data[i].find('strong').text) + "日: " + str(data[i].find('ul').find('li').text.replace( '\n' , '' )) + "\n")
'''

