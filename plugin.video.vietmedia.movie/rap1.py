# -*- coding: utf-8 -*-
                                                      
import urllib,urllib2,re
import json
from BeautifulSoup import BeautifulSoup

fptplay = 'http://fptplay.net/'
moduleName = 'rap1'
defaultThumbnail = 'http://pasgo.vn/thumbs/thumb.php?id=thumbnail'

def make_request(url, headers=None):
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                   'Referer' : 'http://www.google.com'}
    try:
        req = urllib2.Request(url,headers=headers)
        f = urllib2.urlopen(req)
        body=f.read()
        return body
    except:
    	pass

def menu():

	link=make_request(fptplay)
	
	movies = []
	movies.append({'title':'[COLOR ffff0000]Tìm kiếm[/COLOR]','url': moduleName + '.search(":query")', 'description':'','thumb': defaultThumbnail,'playable':False})

	movies.append({'title':'Live TV (cần mồi)','url': moduleName + '.livetv("http://fptplay.net/livetv/")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	match=re.compile('<ul class="top_menu reponsive">(.+?)</ul>',re.DOTALL).findall(link)
	if len(match) > 0:
		link = match[0]
		match=re.compile("<a href=\"(.+?)\"\s*class=\".+?\">(.+?)<\/a>").findall(link)
		for url,name in match:
			movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
			
	movies.append({'title':'Thuý Nga - Tổng hợp','url': moduleName + '.thuynga("http://ott.thuynga.com/vi/genre/index/22/3")', 'description':'','thumb': defaultThumbnail,'playable':False})
	movies.append({'title':'Thuý Nga - Hài kịch','url': moduleName + '.thuynga("http://ott.thuynga.com/vi/genre/index/26/3")', 'description':'','thumb': defaultThumbnail,'playable':False})
	movies.append({'title':'Thuý Nga - Hậu trường','url': moduleName + '.thuynga("http://ott.thuynga.com/vi/genre/index/64/3")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	return movies

def livetv(url):
	content=make_request(url)
	movies = []
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('div',{'class' : 'col-sm-16'})
	for item in items:
		lock = item.find('img',{'class':'lock'})
		if lock is None:
			href = item.find('a',{'class':'channel_slug '})
			title = href.get('channel')
			url = fptplay + href.get('data')
			thumb = item.find('img',{'class':'img-responsive'}).get('src')
			movies.append({'title':title,'url': moduleName + '.livetv_play("' + url + '")', 'description':'','thumb': thumb,'playable':True})
	
	return movies

def livetv_play(url):
	content=make_request(url)

	jsonObject = json.loads(content)

	if jsonObject.get('hls_stream_2500'):
		return {'url': jsonObject['hls_stream_2500']}
	elif jsonObject.get('hls_stream_1000'):
		return {'url': jsonObject['hls_stream_1000']}
	elif jsonObject.get('hls_stream_500'):
		return {'url': jsonObject['hls_stream_500']}
	elif jsonObject.get('hls_stream'):
		return {'url': jsonObject['hls_stream']}
	else:
		return {'error':'Không tìm thấy kênh'}
	
def thuynga(url):
	content=make_request(url)
	movies = []
	thuyngaUrl = 'http://ott.thuynga.com/'

	match=re.compile('<div class="image-wrapper">.*?<a href="(.*?)" style="background-image: url\(\'(.*?)\'\)".*?<h3>.*?<a href=".*?">(.*?)</a>.*?</h3>.*?<div class="content">.*?<p>(.*?)</p>.*?</div>.*?<div style="clear:both;"></div>',re.DOTALL).findall(content)
	for url,thumbnail,title,summary in match:	
		movies.append({'title':title,'url': moduleName + '.thuynga_play("' + thuyngaUrl + url + '")', 'description':summary,'thumb': thumbnail + '?f.png','playable':True})

	match=re.compile('<ul>(.*?)<div class="next button">.*?</ul>').findall(content)
	if len(match) > 0:
		content = match[0]
		match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(content)
		for url,name in match:	
			movies.append({'title':'[COLOR lime]Trang ' + name + '[/COLOR]','url': moduleName + '.thuynga("' + url + '")', 'description':summary,'thumb': defaultThumbnail,'playable':False})
	
	return movies

def thuynga_play(url):
	content=make_request(url)
	
	match=re.compile('var iosUrl = \'(.*?)\';').findall(content)
	if len(match) > 0:
		link = match[0]
		return {'url':link}

def dirs(url):
	link=make_request(url)
	movies = []
	match=re.compile('<a class="col-xs-12 link_title_header" href="/the-loai-more/(.+?)/1">\s*<span class="pull-left" >(.+?)</span >').findall(link)
	
	for url,name in match:	
		movies.append({'title':name,'url': moduleName + '.plist("' + fptplay + 'get_all_vod_structure/news/' + url + '",page=1)', 'description':'','thumb': defaultThumbnail,'playable':False})
		
	return movies

def plist(url,page = 0):	
	movies = []
	for page in range(1,20):
		url_with_page = url + '/' + str(page)
		json_data=make_request(url_with_page)
		match=json.loads(json_data)
		if len(match['videos_list']) == 0:
			break
		for video in match['videos_list']:
			title = video['title']
			thumbnail = video['thumb']
			description = video['description']
			link_video = video['link_video']
			episode_type = video['episode_type']
			playable = False
			if 'Single' in episode_type:
				playable = True
			movies.append({'title':title,'url': moduleName + '.episodes("' + fptplay + link_video + '")', 'description':description,'thumb': thumbnail,'playable':playable})
		
	return movies

def episodes(url):

	link=make_request(url)
	
	movies = []

	title=re.compile('<title >([^\']+)</title >').findall(link)	
	title = title[-1].replace('&#39;',"'")
	match=re.compile('<div class="eps_vod caption">\s*<a data="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(link)
	if len(match) > 0:
		for url,name in match:
			movies.append({'title':('%s - %s' % (name,title)),'url': moduleName + '.vlinks("' + ('%s%s' % (fptplay, url)) + '")', 'description':'','thumb': defaultThumbnail,'playable':True})
		return movies
	else:
		match=re.compile("CallGetVOD\('(.+?)', '(.+?)', currentChapter\);").findall(link)
		if len(match) > 0:
			url = fptplay + 'getvod/' + match[0][0] + '/' + match[0][1] + '/1'
			return vlinks(url)	

def vlinks(url):
	link=make_request(url)
	return {'url':link}

def search(query):
	
	url = fptplay + '/search/' + urllib.quote_plus(query)
	movies = []
	link=make_request(url)
	match=re.compile('<a href="(.+?)" title="(.+?)" class="item_image">\s*<img src="(.+?)".+?').findall(link)

	for url,name, thumbnail in match:
		title = name.replace('&#39;',"'")
		movies.append({'title':title,'url': moduleName + '.episodes("' + fptplay + url + '")', 'description':'','thumb': thumbnail,'playable':True})
		
	return movies
