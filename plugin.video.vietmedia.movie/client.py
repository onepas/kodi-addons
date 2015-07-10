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

def client_id_1():
	
	content = make_request('http://hdonline.vn/phim-quy-ba-diep-vien-8170.html')

	vxml=re.compile(',"file":"(.+?)","').findall(content)[0]
	vxml = 'http://hdonline.vn' + vxml.replace('\/','/')
	
	content = make_request(vxml)
	
	client_id = re.compile('phimhd3s.com//?(................................)/').findall(content)

	if len(client_id) > 0:
		return client_id[0]

	return None


