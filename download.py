# general modules
import os
import shutil
from urllib.parse import urlparse, parse_qs
import sys

# need to install
import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
import img2pdf # pip3 install img2pdf
from PIL import Image # img2pdfと一緒にインストールされたPillowを使います

def url_to_pagename(url):
    result = urlparse(url)
    result = str(result.path)
    result = result.replace(".", "_").replace("/","XX")
    return result



def download_img(page_url):
    img_dir = "img/"

    if os.path.isdir(img_dir):
        shutil.rmtree(img_dir)
    os.mkdir(img_dir)

    # agent偽装
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    header = {'User-Agent': user_agent}

    # get
    r = requests.get(page_url,headers=header)
    
    # 抽出
    soup = BeautifulSoup(r.text, 'html.parser')
    img_tags = soup.find_all("img")
    img_urls = []
    for img_tag in img_tags:
        # if not ("_thumb.jpg" in img_tag.get("src")):
            # continue
        url = img_tag.get("src")
        if (url != None):
            img_urls.append(url)
            # print(url)

    # print(img_urls)

    # download
    for i in range(len(img_urls)):
        p = requests.get(img_urls[i],headers=header)
        if p.status_code == 200:
            with open(img_dir+str(i).zfill(3)+".png", "wb") as f:
                f.write(p.content)
    
    # to pdf
    pdf_FileName = url_to_pagename(page_url)+".pdf" # 出力するPDFの名前
    png_Folder = "img\\" # 画像フォルダ
    extension  = ".png" # 拡張子がPNGのものを対象
    
    ext  = ".png"

    with open(pdf_FileName,"wb") as f:
        # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(png_Folder+j).filename for j in os.listdir(png_Folder)if j.endswith(extension)]))
    
    print("successfully downloaded!!")
    # imgフォルダ削除
    shutil.rmtree(img_dir)


if __name__ == "__main__":
    argc = sys.argv
    if(len(argc) != 2):
        print("Usage: python download.py [url]")
        sys.exit(1)
    download_img(argc[1])
