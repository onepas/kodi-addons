# -*- coding: utf-8 -*-
import CommonFunctions as common
import urllib
import urllib2
import os
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import re, string, json

__settings__ = xbmcaddon.Addon(id='plugin.audio.vietmedia.music')
__language__ = __settings__.getLocalizedString
_home = __settings__.getAddonInfo('path')
_icon = xbmc.translatePath( os.path.join( _home, 'icon.png' ) )
_thumbnails = xbmc.translatePath( os.path.join( _home, 'thumbnails\\' ) )
_vol1_url = 'http://beta.nhacso.net'
_vol1_ajax_play_song_url = _vol1_url + '/songs/ajax-get-detail-song?dataId='
_vol1_ajax_playlist_url = _vol1_url + '/playlists/ajax-get-detail-playlist?dataId='
_vol1_playlist = _vol1_url + '/playlists-noi-bat.html?view_type=highlight&page='
_vol1_ajax_album_url = _vol1_url + '/albums/ajax-get-detail-album?dataId='

_vol1_regex_playlist_album = '<img style="background-image: url\((.*?)\);".*?data-url="([^"]*)" data-name="([^"]*)" data-artists="([^"]*)".*?<span class="pl"></span>'
_vol1_regex_video = '<div class="figure"><img style="background-image: url\((.*?)\);".*?data-url="([^"]*)" data-name="([^"]*)" data-artists="([^"]*)".*?<i class="fa fa-heart"></i></a>'
_vol1_regex_song = '<img style="background-image: url\((.*?)\);".*?class="song-thumb" alt="([^"]*)">\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*<a .*object-id="([^"]*)" object-type="song" data-url-song="([^"]*)" song-name=".*?" data-artist="([^"]*)"'

_vol1_regex_play_video = '<source src="([^"]*)" type=\'(.*?)\'>'
_vol1_regex_load_more = '<div class="load-more"><a class="load-more-link is-load-ajax is-load-more" data-id-content="([^"]*)" href="([^"]*)" page="([^"]*)">Xem thêm</a> </div>'

__thumbnails = []


def get_thumbnail_url():
  return _icon

def _makeCookieHeader(cookie):
  cookieHeader = ""
  for value in cookie.values():
      cookieHeader += "%s=%s; " % (value.key, value.value)
  return cookieHeader

def make_request(url, headers=None):
  if headers is None:
      headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                 'Referer' : 'http://www.google.com'}
  try:
      req = urllib2.Request(url,headers=headers)
      f = urllib2.urlopen(req)
      body=f.read()
      return body
  except urllib2.URLError, e:
      print 'We failed to open "%s".' % url
      if hasattr(e, 'reason'):
          print 'We failed to reach a server.'
          print 'Reason: ', e.reason
      if hasattr(e, 'code'):
          print 'We failed with error code - %s.' % e.code

def alert(message):
  xbmcgui.Dialog().ok("Oops!","",message)

def color_artist(title, artist):
  if title is not None:
    title = title.strip()
  if artist is not None:
    artist = artist.strip()
  if artist is not None and len(artist) > 0:
    return title + '[COLOR FF0084EA]-' + artist + '[/COLOR]'
  return title

def vol_categories():
  add_item('Music Vol1', '', "vol1", get_thumbnail_url())
  add_item('Music Vol2', '', "vol2", get_thumbnail_url())
  add_item('Music Vol3', '', "vol3", get_thumbnail_url())

def vol1_level1():
  add_item('Nổi bật', _vol1_url, "vol1_top",  get_thumbnail_url())
  add_item('Thể loại', _vol1_url, "vol1_category",  get_thumbnail_url())
  add_item('Bảng xếp hạng', _vol1_url, "vol1_ranking",  get_thumbnail_url())
  add_item('Tìm kiếm', _vol1_url, "vol1_search",  get_thumbnail_url())

def vol1_category_list():
  add_item('Việt Nam', _vol1_url +'/the-loai-album/viet-nam-12.html', "vol1_category_vietnam",  get_thumbnail_url())
  add_item('Âu Mỹ', _vol1_url + '/the-loai-album/au-my-21.html', "vol1_catetory_cacnuoc",  get_thumbnail_url())
  add_item('Hàn Quốc', _vol1_url + '/the-loai-album/han-quoc-16.html', "vol1_catetory_cacnuoc",  get_thumbnail_url())
  add_item('Nhạc Hoa', _vol1_url + '/the-loai-album/nhac-hoa-15.html', "vol1_catetory_cacnuoc",  get_thumbnail_url())
  add_item('Các nước khác', _vol1_url + '/the-loai-album/cac-nuoc-khac-18.html', "vol1_catetory_cacnuoc",  get_thumbnail_url())
  add_item('Nhạc chủ đề', _vol1_url +'/the-loai-album/nhac-chu-de-51.html', "vol1_category_vietnam",  get_thumbnail_url())

def vol1_catetory_vietnam(url):
  content = make_request(url)
  regex = '[<a class="is|<a role="menuitem"].*data-id-content=".wrap-page" href="(/the-loai-album/[^"]*)" childId="[^"]*" >([^"]*)</a>'
  match=re.compile(regex).findall(content)
  for (link,title) in match:
    match_url=re.compile('-(\d+)/.*-(\d+).').findall(link)
    if len(match_url) > 0:
      category_id = match_url[0][0]
      category_children_id = match_url[0][1]
      ajax_link = _vol1_url + '/albums/ajax-list-album?category_id=' + category_id + '&category_children_id=' + category_children_id + '&view_type=latest'
      add_item(title, ajax_link, "vol1_category_album_list",  get_thumbnail_url(),page=1)

def vol1_catetory_cacnuoc(url):
  
  match_url=re.compile('-(\d+).').findall(url)
  if len(match_url) > 0:
    category_id = match_url[0]

    ajax_link = _vol1_url + '/albums/ajax-list-album?category_id=' + category_id + '&view_type=latest'
    vol_category_album_list(ajax_link,page=1)


def vol_category_album_list(url,page=1):
  url_page = url + '&page=' + str(page)
  content = make_request(url_page)
  regex = '<img style="background-image: url\(([^\)]*)\);".+?data-url-song="([^"]*)" object-id="([^"]*)".+?song-name="([^"]*)" data-artist="([^"]*)"'
  match=re.compile(regex,re.DOTALL).findall(content)
  for (thumb,link,objecid,title,artist) in match:
    add_item(color_artist(title.strip(),artist.strip()), link, "vol1_playlist", thumb)

  page = page + 1
  url_page_next = url + '&page=' + str(page)
  add_item('[COLOR green]Trang sau >>[/COLOR]', url_page_next, "vol1_category_album_list",  get_thumbnail_url(),page=page)

def vol1_top_categories():
  add_item('Playlist nổi bật', _vol1_url, "vol1_top_playlist",  get_thumbnail_url())
  add_item('Album nổi bật', _vol1_url, "vol1_top_album",  get_thumbnail_url())
  add_item('Video nổi bật', _vol1_url, "vol1_top_video",  get_thumbnail_url())
  add_item('Bài hát nổi bật', _vol1_url, "vol1_top_song",  get_thumbnail_url())

def vol1_level1_data_playlist(url):
  content = make_request(url)
  #playlist and album
  match=re.compile(_vol1_regex_playlist_album,re.DOTALL).findall(content)
  for (thumb,link,title,artist) in match:
    if 'nghe-playlist' in link:
      add_item(color_artist(title.strip(),artist.strip()), link, "vol1_playlist", thumb)

  more_playlist_url = _vol1_playlist + '2'
  add_item('[COLOR green]Các playlist khác[/COLOR]', more_playlist_url, "vol1_playlist_more",  get_thumbnail_url(),page=2)
  
def vol1_level1_data_album(url):
  content = make_request(url)
  #playlist and album
  match=re.compile(_vol1_regex_playlist_album,re.DOTALL).findall(content)
  for (thumb,link,title,artist) in match:
    if 'nghe-album' in link:
      add_item(color_artist(title.strip(),artist.strip()), link, "vol1_playlist", thumb)

def vol1_level1_data_video(url):
  content = make_request(url)
  #video
  match=re.compile(_vol1_regex_video,re.DOTALL).findall(content)
  for (thumb,link,title,artist) in match:
    if 'xem-video' in link:
      add_item(color_artist(title.strip(),artist.strip()), link, "vol1_playvideo", thumb, playable=True)
  
def vol1_level1_data_song(url):
  content = make_request(url)
  
  #song
  match=re.compile(_vol1_regex_song).findall(content)
  for (thumb,title,songid,link,artist) in match:
    data_url = _vol1_ajax_play_song_url + songid
    add_item(color_artist(title.strip(),artist.strip()), data_url, "vol1_playsong", thumb, playable=True)

def vol1_level1_data(url):
  content = make_request(url)
  #playlist and album
  match=re.compile(_vol1_regex_playlist_album,re.DOTALL).findall(content)
  begin_album = 0
  for (thumb,link,title,artist) in match:
    prefix_title = ''
    if 'nghe-playlist' in link:
      prefix_title = '[L].'
    elif 'nghe-album' in link:
      if begin_album == 0:
        begin_album = 1
      prefix_title = '[A].'
    if begin_album == 1:
      begin_album = 2
      more_playlist_url = _vol1_playlist + '2'
      add_item('[COLOR green]Các playlist khác[/COLOR]', more_playlist_url, "vol1_playlist_more",  get_thumbnail_url(),page=2)
    add_item(color_artist(prefix_title + title.strip(),artist.strip()), link, "vol1_playlist", thumb)

  #video
  match=re.compile(_vol1_regex_video,re.DOTALL).findall(content)
  for (thumb,link,title,artist) in match:
    if 'xem-video' in link:
      add_item(color_artist('[V]>' + title.strip(),artist.strip()), link, "vol1_playvideo", thumb, playable=True)
  
  #song
  match=re.compile(_vol1_regex_song).findall(content)
  for (thumb,title,songid,link,artist) in match:
    data_url = _vol1_ajax_play_song_url + songid
    add_item(color_artist('[S]>' + title.strip(),artist.strip()), data_url, "vol1_playsong", thumb, playable=True)
  

def vol1_playlist_load_more(url,page):
  content = make_request(url)
  match=re.compile(_vol1_regex_playlist_album,re.DOTALL).findall(content)
  for (thumb,link,title,artist) in match:
    add_item(color_artist('[L].' + title.strip(),artist.strip()), link, "vol1_playlist", thumb)
  
  match=re.compile(_vol1_regex_load_more).findall(content)
  if len(match) > 0:
    page = page+1
    more_playlist_url = _vol1_playlist + str(page)
    add_item('[COLOR green]Xem thêm[/COLOR]', more_playlist_url, "vol1_playlist_more",  get_thumbnail_url(),page=page)

def vol1_play_list(url):
  parts = url.split('.')
  url = _vol1_ajax_playlist_url + parts[len(parts)-2]
  content = make_request(url)
  data = json.loads(content)
  if len(data['songs']) == 0:
    url = _vol1_ajax_album_url + parts[len(parts)-2]
    content = make_request(url)
    data = json.loads(content)
    
  for song in data['songs']:
    thumb = song['link_image']
    title = song['name']
    songid = song['id']
    link = song['link_mp3']
    artist = song['singer'][0]['alias']
    data_url = _vol1_ajax_play_song_url + songid
    add_item(color_artist(title.strip(),artist.strip()), data_url, "vol1_playsong", thumb, playable=True)

def vol1_play_song(url):
  content = make_request(url)
  data = json.loads(content)
  url_song = data['first_song']['link_mp3']
  listitem = xbmcgui.ListItem(path=url_song)
  xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def vol1_play_video(url):
  content = make_request(url)
  match=re.compile(_vol1_regex_play_video).findall(content)
  if len(match) > 0:
    for (link,content_type) in match:
      listitem = xbmcgui.ListItem(path=link)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
      break

def add_item(name,url,mode,iconimage,query='',type='f',page=0,playable=False):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  if playable:
    liz.setProperty('IsPlayable', 'true')
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=(not playable))
  return ok


def get_params():
  param=[]
  paramstring=sys.argv[2]
  if len(paramstring)>=2:
      params=sys.argv[2]
      cleanedparams=params.replace('?','')
      if (params[len(params)-1]=='/'):
          params=params[0:len(params)-2]
      pairsofparams=cleanedparams.split('&')
      param={}
      for i in range(len(pairsofparams)):
          splitparams={}
          splitparams=pairsofparams[i].split('=')
          if (len(splitparams))==2:
              param[splitparams[0]]=splitparams[1]

  return param

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()

url=''
name=None
mode=None
query=''
type='f'
page=1

try:
    type=urllib.unquote_plus(params["type"])
except:
    pass
try:
    page=int(urllib.unquote_plus(params["page"]))
except:
    pass
try:
    query=urllib.unquote_plus(params["query"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=urllib.unquote_plus(params["mode"])
except:
    pass


if mode==None:
  vol_categories()
elif mode=="vol1":
  vol1_level1()
elif mode=="vol2":
  alert('Sắp phát hành Vol2')
elif mode=="vol3":
  alert('Sắp phát hành Vol3')
elif mode=="vol1_category":
  vol1_category_list()
elif mode=="vol1_top":
  vol1_top_categories()
elif mode=="vol1_category_vietnam":
  vol1_catetory_vietnam(url)
elif mode=="vol1_category_album_list":
  vol_category_album_list(url,page)
elif mode=="vol1_catetory_cacnuoc":
  vol1_catetory_cacnuoc(url)

elif mode=="vol1_top_playlist":
  vol1_level1_data_playlist(url)
elif mode=="vol1_top_album":
  vol1_level1_data_album(url)
elif mode=="vol1_top_video":
  vol1_level1_data_video(url)
elif mode=="vol1_top_song":
  vol1_level1_data_song(url)
elif mode=="vol1_playlist":
  vol1_play_list(url)
elif mode=="vol1_playlist_more":
  vol1_playlist_load_more(url,page)
elif mode=="vol1_playsong":
  vol1_play_song(url)
elif mode=="vol1_playvideo":
  vol1_play_video(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))



