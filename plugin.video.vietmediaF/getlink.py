# -*- coding: utf-8 -*-
#https://www.facebook.com/groups/vietkodi/

import re
import urlfetch
import os
from time import sleep
from addon import notify, alert, ADDON
import simplejson as json
import random

def fetch_data(url, headers=None, data=None):
  	if headers is None:

  		headers = { 
    				'User-agent'		: 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
                	'Referer'			: 'http://www.google.com'
            }
  	try:

  		if data:
  			response = urlfetch.post(url, headers=headers, data=data)
  		else:
			response = urlfetch.get(url, headers=headers)

		return response

	except Exception as e:
  		print e
  		pass


def get(url):
	if 'fptplay.net' in url:
		return get_fptplay(url)
	if 'fshare.vn' in url:
		return get_fshare(url)
	if 'hdonline.vn' in url:
		return get_hdonline(url)
	else:
		return url

def get_fptplay(url):
	headers = { 
				'Referer'			: 'https://fptplay.net',
    			'X-Requested-With'	: 'XMLHttpRequest'
            }
	match = re.search(r'\-([\w]+)\.html', url)
	if not match:
		return

	movie_id = match.group(1)
	match = re.search(r'#tap-([\d]+)$', url)
	
	if match:
		episode_id = match.group(1)
	else:
		episode_id = 1

	data = {
  		'id' 	   : movie_id,
  		'type'     : 'newchannel',
  		'quality'  : 3,
  		'episode'  : episode_id,
  		'mobile'   : 'web',
    }

	response = fetch_data('https://fptplay.net/show/getlink', headers, data)
	
	if response:
		json_data = json.loads(response.body)
		return json_data['stream']
	pass

def get_hdonline(url):
	response = fetch_data(url)
	if not response:
		return ''

	match = re.search(r'\-(\d+)\.?\d*?\.html$', url)
	if not match:
		return
	fid = match.group(1)

	match = re.search(r'\-tap-(\d+)-[\d.]+?\.html$', url)
	if not match:
		ep = 1
	else:
		ep = match.group(1)
	
	_x = random.random()
	url_play = ('http://hdonline.vn/frontend/episode/xmlplay?ep=%s&fid=%s&format=json&_x=%s' % (ep, fid, _x))

	headers = { 
				'User-Agent' 	: 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
				'Referer'		: url,
				'Cookie'		: response.cookiestring
			}
	response = fetch_data(url_play, headers)

	json_data = json.loads(response.body)
	video_url = json_data['file']
	if json_data.get('level') and len(json_data['level']) > 0:
		video_url = json_data['level'][len(json_data['level']) - 1]['file']

	subtitle_url = ''
	if json_data.get('subtitle') and len(json_data['subtitle']) > 0:
		for subtitle in json_data['subtitle']:
			subtitle_url = subtitle['file']
			if subtitle['code'] == 'vi':
				subtitle_url = subtitle['file']
				break
	if len(subtitle_url) > 0:		
		subtitle_url = ('http://data.hdonline.vn/api/vsub.php?url=%s' % subtitle_url)
		return video_url + "[]" + subtitle_url
	else:
		return video_url

def get_fshare(url):
	login_url = 'https://www.fshare.vn/login'
	logout_url = 'https://www.fshare.vn/logout'
	download_url = 'https://www.fshare.vn/download/get'

	username = ADDON.getSetting('fshare_username')
	password = ADDON.getSetting('fshare_password')

	if len(username) == 0  or len(password) == 0:
		alert(u'Bạn chưa nhập tài khoản fshare'.encode("utf-8"))
		return
	
	response = fetch_data(login_url)
	if not response:
		return

	csrf_pattern = '\svalue="(.+?)".*name="fs_csrf"'

	csrf=re.search(csrf_pattern, response.body)
	fs_csrf = csrf.group(1)

	headers = { 
				'User-Agent' 	: 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
				'Cookie'		: response.cookiestring
            }
	
	data = {
			"LoginForm[email]"		: username,
			"LoginForm[password]"	: password,
			"fs_csrf"				: fs_csrf
		}

	response = fetch_data(login_url, headers, data)
	headers['Cookie'] = response.cookiestring
	headers['Referer'] = url
	direct_url = ''
	attempt = 1
	MAX_ATTEMPTS = 8
	file_id = os.path.basename(url)
	if response and response.status == 302:
		notify (u'Đăng nhập fshare thành công'.encode("utf-8"))
		while attempt < MAX_ATTEMPTS:
			if attempt > 1: sleep(2)
			notify (u'Lấy link lần thứ #%s'.encode("utf-8") % attempt)
			attempt += 1

			response = fetch_data(url, headers, data)

			if response.status == 200:
				csrf=re.search(csrf_pattern, response.body)
				fs_csrf = csrf.group(1)
				data = {
						'fs_csrf'					: fs_csrf,
						'ajax'						: 'download-form',
						'DownloadForm[linkcode]'	: file_id
					}
				
				response=fetch_data(download_url, headers, data);
				
				json_data = json.loads(response.body)
				
				if json_data.get('url'):
					direct_url = json_data['url']
					break
				elif json_data.get('msg'):
					notify(json_data['msg'].encode("utf-8"))
			elif response.status == 302:
				direct_url = response.headers['location']
				break
			else:
				notify (u'Lỗi khi lấy link, mã lỗi #%s. Đang thử lại...'.encode("utf-8") % response.status) 

		response = fetch_data(logout_url, headers)
		if response.status == 302:
			notify (u'Đăng xuất fshare thành công'.encode("utf-8"))
	else:
		notify (u'Đăng nhập không thành công, kiểm tra lại tài khoản'.encode("utf-8"))
	if len(direct_url) > 0:
		notify (u'Đã lấy được link'.encode("utf-8"))
	else:
		notify (u'Không được link, bạn vui lòng kiểm tra lại tài khoản'.encode("utf-8"))

	return direct_url
