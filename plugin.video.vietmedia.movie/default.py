# -*- coding: utf-8 -*-
#https://www.facebook.com/groups/vietkodi/

import CommonFunctions as common
import urllib
import urllib2
import os
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import re, string, json
import base64,uuid


reload(sys);
sys.setdefaultencoding("utf8")

__settings__ = xbmcaddon.Addon(id='plugin.video.vietmedia.movie')
__language__ = __settings__.getLocalizedString
__profile__ = xbmc.translatePath( __settings__.getAddonInfo('profile') ).decode("utf-8")

_home = __settings__.getAddonInfo('path')
_icon = xbmc.translatePath( os.path.join( _home, 'icon.png' ))

_homeUrl = 'maSklWtfX5ualaSQoJSZU6SVopuWmKSZoV6TlJ5qY1VhYF-Imp6VkpJfplY='
_version = '1.0.3'
_user = 'vietmedia'

def make_cookie_header(cookie):
  cookieHeader = ""
  for value in cookie.values():
      cookieHeader += "%s=%s; " % (value.key, value.value)
  return cookieHeader

def fetch_data(url, headers=None):
  visitor = get_visitor()
  if headers is None:
    headers = { 'User-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
                'Referers':'http://www..google.com',
                'X-Visitor':visitor,
                'X-Version':_version,
                'X-User':_user
              }
  try:
    req = urllib2.Request(url,headers=headers)
    f = urllib2.urlopen(req)
    body=f.read()
    return body
  except:
    pass
    
def alert(message):
  xbmcgui.Dialog().ok("Oops!","",message)

def notification(message, timeout=7000):
  xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s)' % ('VietMedia', message, timeout)).encode("utf-8"))

def extract(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def add_item(name,url,mode,iconimage,query='',type='f',plot='',page=0,playable=False):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  if playable:
    liz.setProperty('IsPlayable', 'true')
  liz.setInfo( type="Video", infoLabels={ "Title": name, "plot":plot } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=(not playable))
  return ok

def buildCinemaMenu(url):
  if (url is None):
    url = extract('100%',_homeUrl)

  if ':query' in url:
    keyboardHandle = xbmc.Keyboard('','Enter search text')
    keyboardHandle.doModal()
    if (keyboardHandle.isConfirmed()):
      queryText = keyboardHandle.getText()
      if len(queryText) == 0:
        return
      queryText = urllib.quote_plus(queryText)
      url = url.replace(':query',queryText)
    else:
      return

  content = fetch_data(url)
  jsonObject = json.loads(content)
  if isinstance(jsonObject,list):
    for item in jsonObject:
      title = item['title']
      thumb = item['thumb']
      url = item['url']
      description = item['description']
      playable = item['playable']

      add_item(title,url,"default",thumb,plot=description,playable=playable)
  elif jsonObject.get('url'):
    link = jsonObject['url']
    if jsonObject.get('regex'):
      try:
        regex = jsonObject['regex']
        content = fetch_data(link)
        link=re.compile(regex).findall(content)[0]  
      except:
        pass
    subtitle = ''
    if jsonObject.get('subtitle'):
      subtitle = jsonObject['subtitle']

    listitem = xbmcgui.ListItem(path=link)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    if len(subtitle) > 0:
      subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
      subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
      urllib.urlretrieve (subtitle,subfile )
      xbmc.sleep(2000)
      xbmc.Player().setSubtitles(subfile)
    elif jsonObject.get('subtitle'):
      notification('Video này không có phụ đề rời.');

  elif jsonObject.get('error') is not None:
    alert(jsonObject['error'])

def get_visitor():
  filename = os.path.join( __profile__, 'visitor.dat' )
  visitor = ''

  if os.path.exists(filename):
    with open(filename, "r") as f:
      visitor = f.readline()
  else:
    try:
      visitor = str(uuid.uuid1())
    except:
      visitor = str(uuid.uuid4())
    
    if not os.path.exists(__profile__):
      os.makedirs(__profile__)
    with open(filename, "w") as f:
      f.write(visitor)

  return visitor

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

url=None
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


buildCinemaMenu(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))



