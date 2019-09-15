import requests 
import json
import os
import re
from bs4 import BeautifulSoup as soup 
link = 'https://www.pornhub.com'
#获取某分类下任意页数的视频列表
def getVideoList(types,page='1',search = False):
    #url = link + '/video?c=111&page=1'
    result = []
    url = link+types+str(page)
    rep = requests.get(url)
    videoList = soup(rep.content)
    if search:
        videoList = videoList.find('ul',id = 'videoSearchResult').findAll('li')
    else:
        videoList = videoList.find('ul',id = 'videoCategory').findAll('li')
    for i in videoList:
        try:
            title = i.a.get('title')
            result.append({
            'title':title,
            'preview' : i.img.get('data-mediabook'),
            'pic' : i.img.get('data-src'),
            'url' : i.a.get('href'),
            'time' : i.var.text
            }) 
        except:
            continue
            
    return result
#获取视频全部清晰度,地址,视频编号
def getVideoUrl(viewkey):
    url = link + '/view_video.php?viewkey='+viewkey
    rep = requests.get(url)
    t = re.findall(r'"mediaDefinitions":\[(.+?)\]',rep.text)[0]
    try:
        videoList = json.loads('['+t+']')
    except:
        videoList = json.loads('['+t+']}]')
    videoURL = []
    t=0
    for i in videoList:
        if (i["format"].upper() != 'MP4') or i['videoUrl'] == "":
            continue
        try:
            if int(i["quality"])>t:
                t=int(i["quality"])
                videoURL = [i,]
        except Exception as e:
            print(e)
            continue
    ids = os.path.split(os.path.split(videoURL[0].get('videoUrl'))[0])[1]
    return [videoURL,ids]
    
#根据视频编号获取全部相似推荐
def getVideoSimilar(ids,page=1):
    url = '%s/video/relateds?ajax=1&id=%s&page=%s&num_per_page=10'%(link,ids,page)
    result=[]
    rep = requests.get(url)
    videoList = soup(rep.content)
    videoList = videoList.findAll('li')
    for i in videoList:
        result.append({
            'title':i.a.get('title'),
            'preview' : i.img.get('data-mediabook'),
            'pic' : i.img.get('src'),
            'url' : i.a.get('href'),
            'time' : i.var.text
        })
    #return resultStr
    return result
