# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a facility script file for you to download and rename the paper with 
the paper title.

Author: wfeng6@gmail.com
"""

import requests
import uuid
import pdftitle
import os
import time
import argparse

def formatFloat(num):
    return '{:.2f}'.format(num)

def downloadFile(url, name):
    print("downloadFile: url: {} name: {}".format(url, name))
    headers = {'Proxy-Connection':'keep-alive'}
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])

    print('Total download size: {:.2f} MB'.format(length/1024/1024))
    count = 0
    count_tmp = 0
    time1 = time.time()
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 512):
            if chunk:
                f.write(chunk)
                count += len(chunk)
                if time.time() - time1 > 2:
                    p = count / length * 100
                    speed = (count - count_tmp) / 1024 / 1024 / 2
                    count_tmp = count
                    print(name + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'MB/S')
                    time1 = time.time()

def changePdfName(filename):
    print('changePdfName: original filename {}'.format(filename))
    title = pdftitle.get_title_from_file(filename)
    print('original title: ', title)

    forbidChars = ['/', ':']
    for ch in forbidChars:
        newTitle = title.replace(ch,"")
        title = newTitle

    newTitle = newTitle+'.pdf'
    print('new title: ', newTitle)

    os.rename(filename, newTitle)

def getPaper(link):
    filename = str(uuid.uuid4()) + '.pdf'
    downloadFile(link, filename)
    changePdfName(filename)


if __name__ == '__main__':
#    filename = 'd25c283e-c071-4230-979c-23b9315ff9ac.pdf'
#    changePdfName(filename)
#    link = 'https://nips2017creativity.github.io/doc/ObamaNet.pdf'
#    getPaper(link)
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("-l", "--link", type=str, required=True, help="the download link")
    args = parser.parse_args()
    print(args.link)
    getPaper(args.link)