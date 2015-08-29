import urllib,urllib2,re
import StringIO,gzip

def make_request(url):
    strresult=""
    try:
		opener = urllib2.build_opener()
		opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
							 ('Accept-Encoding','gzip, deflate'),
							 ('Referer', "http://hdonline.vn/player/vplayer.swf"),
							 ('Content-Type', 'application/x-www-form-urlencoded'),
							 ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
							 ('Connection','keep-alive'),
							 ('Accept-Language','en-us,en;q=0.5'),
							 ('Pragma','no-cache'),
							 ('Host','hdonline.vn')]
		usock=opener.open(url)
		if usock.info().get('Content-Encoding') == 'gzip':
			buf = StringIO.StringIO(usock.read())
			f = gzip.GzipFile(fileobj=buf)
			strresult = f.read()
		else:
			strresult = usock.read()
		usock.close()
    except Exception, e:
       print str(e)+" |" + url
    return strresult

def extract_data(encoded):
    import math
    _local_2 = "";
    _local_3 = list("1234567890qwertyuiopasdfghjklzxcvbnm")
    _local_4= len(_local_3)
    strlen=len(encoded)
    _local_5= list("f909e34e4b4a76f4a8b1eac696bd63c4")
    _local_6 = list(encoded[((_local_4 * 2) + 32):strlen])
    _local_7= list(encoded[0:(_local_4 * 2)])
    _local_8= []
    _local_9= encoded[((_local_4 * 2) + 32):strlen]
    _local_10 = 0
    while (_local_10 < (_local_4 * 2)):
        _local_11 = (_local_3.index(_local_7[_local_10]) * _local_4)
        _local_11 = (_local_11 + _local_3.index(_local_7[(_local_10 + 1)]))
        idx= int(math.floor((_local_10 / 2)) % len(_local_5))
        str(_local_5[idx])[0]
        _local_11 = (_local_11 - ord(str(_local_5[idx])[0]))
        _local_8.append(chr(_local_11))
        _local_10 = (_local_10 + 2)
		
    _local_10 = 0
    while (_local_10 < len(_local_6)):
        _local_11 = (_local_3.index(_local_6[_local_10]) * _local_4)
        _local_11 = (_local_11 + _local_3.index(_local_6[(_local_10 + 1)]))
        idx= int((math.floor((_local_10 / 2)) % _local_4))
        _local_11 = (_local_11 - ord(str(_local_8[idx])[0]))
        _local_2 = (_local_2 + chr(_local_11))
        _local_10 = (_local_10 + 2)

    return _local_2

def client_id_1():
	
	try:
		content = make_request('http://hdonline.vn/phim-quy-ba-diep-vien-8170.html')
		
		vxml=re.compile(',"file":"(.+?)","').findall(content)[0]
		vxml = 'http://hdonline.vn' + vxml.replace('\/','/')

		content = make_request(vxml)
		
		url_encoded = re.compile('<jwplayer:file>(.*?)</jwplayer:file>').findall(content)[0]
		url_decoded = extract_data(url_encoded)
		
		content = make_request(url_decoded)

		url_encoded = re.compile('<jwplayer:file>(.*?)</jwplayer:file>').findall(content)[0]
		
		url_decoded = extract_data(url_encoded)
		
		#client_id = re.compile('phimhd3s.com/.*?/?(................................)/').findall(url_decoded)
		client_id = re.compile('/?(................................)/').findall(url_decoded)
		
		if len(client_id) > 0:
			return client_id[0]

		return None
	except:
		pass

def client_id_2():
	
	try:
		content = make_request('http://hdonline.vn/frontend/episode/loadxmlconfigorder?ep=1&fid=7876')

		url_decoded = re.compile('<jwplayer:file>(.*?)</jwplayer:file>').findall(content)[0]
		
		#client_id = re.compile('phimhd3s.com/.*?/?(................................)/').findall(url_decoded)
		client_id = re.compile('/?(................................)/').findall(url_decoded)
		
		if len(client_id) > 0:
			return client_id[0]

		return None
	except:
		pass
