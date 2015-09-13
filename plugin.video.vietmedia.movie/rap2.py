# -*- coding: utf-8 -*-
                                                      
import urllib,urllib2,re
import json
from BeautifulSoup import BeautifulSoup
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.vietmedia.movie')
moduleName = 'rap2'


def login_xmio():
    url = 'http://125.212.195.249:8088/login_action.php'
    headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
		   		'Content-type': 'application/x-www-form-urlencoded',
           		'Referer' : 'http://125.212.195.249'}

    user_xmio = __settings__.getSetting('user_xmio')
    pass_xmio = __settings__.getSetting('pass_xmio')
    try:
    	params = {
			'email' : user_xmio,
		  	'password' : pass_xmio
		}

        req = urllib2.Request(url,urllib.urlencode(params),headers)
        f = urllib2.urlopen(req)
        body=f.read()
        if 'index.php' in body:
        	return f.info()['Set-Cookie']

    except:
    	pass

def make_request(url, cookie=None, params=None, headers=None):
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        		   'Content-type': 'application/x-www-form-urlencoded',
           			'Referer' : 'http://125.212.195.249'}
    if cookie is not None:
    	headers['Cookie'] = cookie
    try:
    	if params is not None:
    		params = urllib.urlencode(params)
        req = urllib2.Request(url,params,headers)
        f = urllib2.urlopen(req)
        body=f.read()
        return body
    except:
    	pass

def menu():
	movies = []
	cookie = login_xmio()
	if cookie is None:
		return {'error': u'Tên đăng nhập hoặc mật khẩu không đúng, hãy kiểm tra lại trên website xmio'}

	content = make_request('http://125.212.195.249:8088/truyen-hinh',cookie)
	items = re.compile('<li><a href="truyen-hinh(.*?)".*src="(.*?)".*alt="(.*?)"').findall(content)

	for item in items:
		if item[1] == '':
			break
		name = item[2]
		url = 'http://125.212.195.249:8088/truyen-hinh' + item[0]
		thumb = item[1]
		movies.append({'title':name,'url': moduleName + '.play("' + url + '")', 'description':'','thumb': thumb,'playable':True})
		if '?id=28' == item[0]:
			name = 'StarMovie'
			url = 'http://125.212.195.249:8088/truyen-hinh?id=24'
			thumb = 'http://i.imgur.com/CQBtPMD.png'
			movies.append({'title':name,'url': moduleName + '.play("' + url + '")', 'description':'','thumb': thumb,'playable':True})
			name = 'StarWorld'
			url = 'http://125.212.195.249:8088/truyen-hinh?id=1084'
			thumb = 'http://www.medigit.in/wp-content/uploads/2013/07/star-world1-150x150.jpg'
			movies.append({'title':name,'url': moduleName + '.play("' + url + '")', 'description':'','thumb': thumb,'playable':True})

	return movies

def play(url):
	cookie = login_xmio()
	content = make_request(url,cookie)
	result = re.compile('banner_slide_tv.php(.*?)\'').findall(content)[0]
	headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        		'Content-type': 'application/x-www-form-urlencoded',
           	'Referer' : url}
	url = 'http://125.212.195.249:8088/banner_slide_tv.php' + result
	content = make_request(url,cookie,headers=headers)

	match = re.compile("'(.*?)'").findall(content)

	if len(match) > 0:
		link = match[0]
		return {'url':link + '|User-Agent=AppleCoreMedia/1.0.0.11D201%20(iPad;%20U;%20CPU%20OS%207_1_1%20like%20Mac%20OS%20X;%20fi_fi)&seekable=0'}
	else:
		return {'error': u'Không tìm thấy link, hãy thử lại.'}
