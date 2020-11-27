import itertools
import os
import sys
from urllib.parse import urlparse
import pandas as pd
import urllib3
import requests

'''
这是书中数据集的下载代码
作者提供的code是有问题的，于是我自己重写了这个代码
'''

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

classes = ["cat", "fish"]
set_types = ["train", "test", "val"]


def download_image(url, klass, data_type):
    filename = os.path.basename(urlparse(url).path)
    os.chdir("D:/PyCharm/pytorch_learning/src/download/{}/{}".format(data_type, klass))
    if not os.path.exists(filename):
        try:
            im = requests.get(url)
            if im.status_code == 200:
                open(filename, 'wb').write(im.content)
                print("Successfully download {}".format(url))
        except:
            print("Error downloading {}".format(url))


if __name__ == "__main__":
    if not os.path.exists("images.csv"):
        print("Error: can't find images.csv!")
        sys.exit(0)
    imagesDF = pd.read_csv("images.csv")
    for set_type, klass in list(itertools.product(set_types, classes)):
        path = "./{}/{}".format(set_type, klass)
        if not os.path.exists(path):
            print("Creating directory {}".format(path))
            os.makedirs(path)
    print("Downloading {} images".format(len(imagesDF)))
    result = [
        download_image(url, klass, data_type)
        for url, klass, data_type in zip(
            imagesDF["url"], imagesDF["class"], imagesDF["type"]
        )
    ]
    sys.exit(0)
