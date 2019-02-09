import requests 
import json
import os
import re
from bs4 import BeautifulSoup as soup 
link = 'https://www.pornhub.com'
#获取某分类下任意页数的视频列表
def getVideoList(url):
    #url = link + '/video?c=111&page=1'
    result = {}
    rep = requests.get(url)
    videoList = soup(rep.content)
    videoList = videoList.find('ul',id = 'videoCategory').findAll('li')
    for i in videoList:
        title = i.a.get('title')
        result[title] = {
            'title':title,
            'preview' : i.img.get('data-mediabook'),
            'pic' : i.img.get('data-src'),
            'url' : i.a.get('href'),
            'time' : i.var.text
        }
    return result
#获取视频全部清晰度,地址,视频编号
def getVideoUrl(url):
    #url = link + '/view_video.php?viewkey=ph5c56aa1268005'
    rep = requests.get(url)
    videoList = json.loads('['+re.findall(r'"mediaDefinitions":\[(.+?)\]',rep.text)[0]+']')
    if videoList[0].get('videoUrl') == '':
        videoList = videoList[1:]
    ids = os.path.split(os.path.split(videoList[0].get('videoUrl'))[0])[1]
    return [videoList,ids]
    
#根据视频编号获取全部相似推荐
def getVideoSimilar(ids):
    urlList = list('%s/video/relateds?ajax=1&id=%s&page=%s&num_per_page=10'%(link,ids,i) for i in range(1,7))
    result={}
    for url in urlList:
        rep = requests.get(url)
        videoList = soup(rep.content)
        videoList = videoList.findAll('li')
        for i in videoList:
            title = i.a.get('title')
            result[title] = {
                'title':title,
                'preview' : i.img.get('data-mediabook'),
                'pic' : i.img.get('data-src'),
                'url' : i.a.get('href'),
                'time' : i.var.text
            }
    return result