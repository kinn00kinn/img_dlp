# general modules
import os
import shutil
from urllib.parse import urlparse, parse_qs
import sys
import uuid
import re

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

def is_ok_url(url):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"

    if re.match(pattern, url):
        return True
    else:  
        return False



def download_img(page_url):
    img_dir = str(uuid.uuid4())+"img/"
    if os.path.isdir(img_dir):
        os.chmod(img_dir,0o777)
        shutil.rmtree(img_dir)
    os.mkdir(img_dir)
    os.chmod(img_dir,0o777)

    # agent偽装    
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    # get
    r = requests.get(page_url,headers=header)
    
    # 抽出
    soup = BeautifulSoup(r.text, 'html.parser')
    img_tags = soup.find_all("img")
    img_urls = []
    for img_tag in img_tags:
        url = img_tag.get("src")
        # print(url)
        if (url != None) and (is_ok_url(url)): # is_ok_url(url)
            img_urls.append(url)
            print(url)

    # print(img_urls)

    # download
    for i in range(len(img_urls)):
        p = requests.get(img_urls[i],headers=header)
        if p.status_code == 200:
            with open(img_dir+str(i).zfill(3)+".png", "wb") as f:
                f.write(p.content)
    
    # to pdf
    # pdf_FileName = url_to_pagename(page_url)+".pdf" # 出力するPDFの名前
    pdf_FileName = str(uuid.uuid4())+".pdf" # 出力するPDFの名前
    print(pdf_FileName)
    extension  = ".png" # 拡張子がPNGのものを対象
    
    ext  = ".png"

    with open(pdf_FileName,"wb") as f:
        # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(img_dir+j).filename for j in os.listdir(img_dir)if j.endswith(extension)]))
    
    # print("successfully downloaded!!")
    # imgフォルダ削除
    os.chmod(img_dir,0o777)
    shutil.rmtree(img_dir)



