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
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
thumbnails = xbmc.translatePath( os.path.join( home, 'thumbnails\\' ) )
vol1_url = 'http://beta.nhacso.net/'
vol1_ajax_play_song_url = 'http://beta.nhacso.net/songs/ajax-get-detail-song?dataId='
vol1_ajax_playlist_url = 'http://beta.nhacso.net/playlists/ajax-get-detail-playlist?dataId='
vol1_playlist = 'http://beta.nhacso.net/playlists-noi-bat.html?view_type=highlight&page='
vol1_ajax_album_url = 'http://beta.nhacso.net/albums/ajax-get-detail-album?dataId='

vol1_regex_playlist_album = '<img style="background-image: url\((.*?)\);".*?data-url="(.*?)" data-name="(.*?)" data-artists="(.*?)".*?<span class="pl"></span>'
vol1_regex_video = '<div class="figure"><img style="background-image: url\((.*?)\);".*?data-url="(.*?)" data-name="(.*?)" data-artists="(.*?)".*?<i class="fa fa-heart"></i></a>'
vol1_regex_song = '<img style="background-image: url\((.*?)\);".*?class="song-thumb" alt="(.*?)">\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*<a .*object-id="(.*?)" object-type="song" data-url-song="(.*?)" song-name=".*?" data-artist="(.*?)"'

vol1_regex_play_video = '<source src="(.*?)" type=\'(.*?)\'>'
vol1_regex_load_more = '<div class="load-more"><a class="load-more-link is-load-ajax is-load-more" data-id-content="(.*?)" href="(.*?)" page="(.*?)">Xem thêm</a> </div>'

__thumbnails = []


def get_thumbnail_url():
  return icon

def _makeCookieHeader(cookie):
  cookieHeader = ""
  for value in cookie.values():
      cookieHeader += "%s=%s; " % (value.key, value.value)
  return cookieHeader

def make_request(url, headers=None):
  if headers is None:
      headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
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
  add_item('Music Vol1', '', 1, get_thumbnail_url())

def vol1_level1():
  add_item('Nổi bật', vol1_url, 100,  get_thumbnail_url())
    
def vol1_level1_data(url):
  content = make_request(url)
  #playlist and album
  match=re.compile(vol1_regex_playlist_album,re.DOTALL).findall(content)
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
      more_playlist_url = vol1_playlist + '2'
      add_item('[COLOR green]Các playlist khác[/COLOR]', more_playlist_url, 102,  get_thumbnail_url(),page=2)
    add_item(color_artist(prefix_title + title.strip(),artist.strip()), link, 101, thumb)

  #video
  match=re.compile(vol1_regex_video,re.DOTALL).findall(content)
  for (thumb,link,title,artist) in match:
    if 'xem-video' in link:
      add_item(color_artist('[V]>' + title.strip(),artist.strip()), link, 121, thumb, playable=True)
  
  #song
  match=re.compile(vol1_regex_song).findall(content)
  for (thumb,title,songid,link,artist) in match:
    data_url = vol1_ajax_play_song_url + songid
    add_item(color_artist('[S]>' + title.strip(),artist.strip()), data_url, 120, thumb, playable=True)
  

def vol1_playlist_load_more(url,page):
  content = make_request(url)
  match=re.compile(vol1_regex_playlist_album,re.DOTALL).findall(content)
  for (thumb,link,title,artist) in match:
    add_item(color_artist('[L].' + title.strip(),artist.strip()), link, 101, thumb)
  
  match=re.compile(vol1_regex_load_more).findall(content)
  if len(match) > 0:
    page = page+1
    more_playlist_url = vol1_playlist + str(page)
    add_item('[COLOR green]Xem thêm[/COLOR]', more_playlist_url, 102,  get_thumbnail_url(),page=page)

def vol1_play_list(url):
  parts = url.split('.')
  url = vol1_ajax_playlist_url + parts[len(parts)-2]
  content = make_request(url)
  data = json.loads(content)
  if len(data['songs']) == 0:
    url = vol1_ajax_album_url + parts[len(parts)-2]
    content = make_request(url)
    data = json.loads(content)
    
  for song in data['songs']:
    thumb = song['link_image']
    title = song['name']
    songid = song['id']
    link = song['link_mp3']
    artist = song['singer'][0]['alias']
    data_url = vol1_ajax_play_song_url + songid
    add_item(color_artist(title.strip(),artist.strip()), data_url, 120, thumb, playable=True)

def vol1_play_song(url):
  content = make_request(url)
  data = json.loads(content)
  url_song = data['first_song']['link_mp3']
  listitem = xbmcgui.ListItem(path=url_song)
  xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def vol1_play_video(url):
  content = make_request(url)
  match=re.compile(vol1_regex_play_video).findall(content)
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
page=0

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
    mode=int(params["mode"])
except:
    pass


if mode==None:
  vol_categories()
elif mode==1:
  vol1_level1()
elif mode==100:
  vol1_level1_data(url)
elif mode==101:
  vol1_play_list(url)
elif mode==102:
  vol1_playlist_load_more(url,page)
elif mode==120:
  vol1_play_song(url)
elif mode==121:
  vol1_play_video(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))



