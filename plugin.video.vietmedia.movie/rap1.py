# -*- coding: utf-8 -*-
                                                      
import urllib,urllib2,re
import json
from BeautifulSoup import BeautifulSoup

fptplay = 'http://fptplay.net/'
moduleName = 'rap1'
defaultThumbnail = 'http://pasgo.vn/thumbs/thumb.php?id=thumbnail'

def make_request(url, params=None, headers=None):
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        		   'Content-type': 'application/x-www-form-urlencoded',
        		   'X-Requested-With': 'XMLHttpRequest',
                   'Referer' : 'http://fptplay.net'}
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
	movies.append({'title':'[COLOR ffff0000]Tìm kiếm[/COLOR]','url': moduleName + '.search(":query")', 'description':'','thumb': defaultThumbnail,'playable':False})

	movies.append({'title':'Tivi','url': moduleName + '.livetv("http://fptplay.net/livetv")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	name = 'Phim lẻ'
	url = 'danh-muc/5575429017dc1321ed858679/phim-le.html'
	movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	name = 'Phim bộ'
	url = 'danh-muc/55701c1517dc1321ee85857a/phim-bo.html'
	movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	name = 'TV Show'
	url = 'danh-muc/52847232169a585a2449c48c/tv-show.html'
	movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	name = 'Thiếu nhi'
	url = 'danh-muc/54fd271917dc136162a0cf2d/thieu-nhi.html'
	movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	name = 'Thể Thao'
	url = 'danh-muc/52842df7169a580a79169efd/the-thao.html'
	movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	name = 'Ca Nhạc'
	url = 'danh-muc/5283310e169a585a05b920de/ca-nhac.html'
	movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	name = 'Tổng Hợp'
	url = 'danh-muc/52842dd3169a580a79169efc/tong-hop.html'
	movies.append({'title':name,'url': moduleName + '.dirs("' + fptplay + url + '")', 'description':'','thumb': defaultThumbnail,'playable':False})
	
	
	return movies

def livetv(url):
	content=make_request(url)
	movies = []
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a',{'class' : 'tv_channel '})
	for item in items:
		lock = item.find('img',{'class':'lock'})
		if lock is None:
			title = item.find('img',{'class':'img-responsive'}).get('alt')
			url = item.get('data-href')
			thumb = item.find('img',{'class':'img-responsive'}).get('data-original')
			movies.append({'title':title,'url': moduleName + '.livetv_play("' + url + '")', 'description':'','thumb': thumb,'playable':True})
	
	return movies

def livetv_play(url):
	params = url.split('/')
	channel = params[len(params) - 1]
	getlinklivetv = 'http://fptplay.net/show/getlinklivetv'

	data = {
		'id':channel,
		'quality':'0',
		'mobile':'web'
	}

	content=make_request(getlinklivetv,data)

	jsonObject = json.loads(content)

	if jsonObject.get('msg_code') == 'success':
		return {'url': jsonObject['stream']}
	else:
		return {'error':'Không tìm thấy link, hãy thử lại.'}
	
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
	content=make_request(url)
	movies = []
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a',{'class' : 'pull-left btn_arrow_right'})
	for item in items:
		url = item.get('href')
		series = 1
		if '/nhac-' in url:
			series = 0
		arr = url.split('/')
		cate = arr[len(arr) - 2]
		name = item.get('title')
		movies.append({'title':name,'url': moduleName + '.plist("' + cate + '",page=1,series=' + str(series) + ')', 'description':'','thumb': defaultThumbnail,'playable':False})

	return movies

def plist(cate,page = 1, series = 1, typep='new', keyword=''):	
	movies = []
	url = 'http://fptplay.net/show/more'
	page_size = 4
	has_more_page = True
	for p in xrange(0,page_size):
		p_page = 1 + p + (page - 1)*page_size

		params = {
			'type' : typep,
			'stucture_id': cate,
			'page': p_page,
			'keyword': keyword
		}
		content=make_request(url,params)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.findAll('div',{'class' : 'atip'})
		info = []
		if len(items) == 0:
			has_more_page = False
			break

		for item in items:
			phim = item.get('id')
			title = item.find('h3').string
			description = item.find('span').string
			info.append({'phim':phim,'title':title,'description':description})

		items = soup.findAll('div',{'class' : 'small_item tip'})
		for item in items:
			phim = item.get('data-tooltip')
			thumbnail = item.find('img').get('src')
			link = item.find('a').get('href')
			title = ''
			description = ''
			for x in info:
				if x.get('phim') == phim:
					description = x.get('description')
					title = x.get('title')
			if series == 1:
				movies.append({'title':title,'url': moduleName + '.episodes("' + link + '")', 'description':description,'thumb': thumbnail,'playable':False})
			else:
				movies.append({'title':title,'url': moduleName + '.vlinks("' + link + '")', 'description':description,'thumb': thumbnail,'playable':True})
	if has_more_page:
		movies.append({'title':'[COLOR lime]Trang sau >> [/COLOR]','url': moduleName + '.plist("' + cate + '",page=' + str(page + 1) + ',series=' + str(series) + ',typep="' + typep + '",keyword="' + keyword + '")', 'description':'','thumb': '','playable':False})

	return movies

def episodes(url):

	ll = url.split('-')
	film_id = ll[len(ll)-1].replace('.html','')
	
	movies = []

	for p in xrange(1,20):
		
		params = {
			'page':p,
			'film_id': film_id
		}

		url = 'http://fptplay.net/show/episode'
		content=make_request(url,params)
		
		if content is None:
			break

		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.findAll('div',{'class' : 'small_item'})
		for item in items:
			href = item.find('a',{'class' : 'title'})
			link = href.get('href')
			title = item.find('img').get('alt')
			title = href.string + '-' + title
			thumbnail = item.find('img').get('src')
			movies.append({'title':title,'url': moduleName + '.vlinks("' + link + '")', 'description':'','thumb': thumbnail,'playable':True})
		
	if len(movies) == 0:
		title = soup.find('h3',{'class' : 'col-xs-8 col-sm-8 col-md-8'}).string.strip()
		movies.append({'title':title,'url': moduleName + '.vlinks("' + url + '")', 'description':'','thumb': defaultThumbnail ,'playable':True})
	return movies

def vlinks(url):
	params = url.split('#')
	p1 = params[0]
	p1_params = p1.split('-')
	movie_id = p1_params[len(p1_params)-1].replace('.html','')
	
	episode = 1
	if len(params) == 2:
		p2 = params[1]
		p2_params = p2.split('-')
		if len(p2_params) == 2 and p2_params[0] == 'tap':
			episode = int(p2_params[1])

	getlink = 'http://fptplay.net/show/getlink'
	data = {
		'id':movie_id,
		'episode':episode,
		'mobile':'web'
	}
	content=make_request(getlink,data)
	
	jsonObject = json.loads(content)
	if jsonObject.get('msg_code') == 'success':
		return {'url': jsonObject['stream']}
	else:
		return {'error':'Không tìm thấy link, hãy thử lại.'}

def search(query):
	query = query.replace('+',' ')
	return plist('key', 1, 1, 'search', query)
