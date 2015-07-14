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
import re, string
import base64,uuid
import client

try:
  import simplejson as json
except ImportError:
  import json

from config import VIETMEDIA_HOST
from addon import ADDON, ADDON_ID, ADDON_NAME, ADDON_PROFILE
from platform import PLATFORM

reload(sys);
sys.setdefaultencoding("utf8")

HANDLE = int(sys.argv[1])

CURRENT_PATH = ADDON.getAddonInfo("path")
PROFILE_PATH = xbmc.translatePath(ADDON_PROFILE).decode("utf-8")

VERSION = ADDON.getAddonInfo("version")
USER = ADDON.getSetting('user_id')

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
                'X-Version':VERSION,
                'X-User':USER,
                'X-Platform':PLATFORM,
              }
  try:
    req = urllib2.Request(url,headers=headers)
    f = urllib2.urlopen(req)
    body=f.read()

    return json.loads(body)
  except:
    pass

def get_visitor():
  
  filename = os.path.join(PROFILE_PATH, 'visitor.dat' )
  visitor = ''

  if os.path.exists(filename):
    with open(filename, "r") as f:
      visitor = f.readline()
  else:
    try:
      visitor = str(uuid.uuid1())
    except:
      visitor = str(uuid.uuid4())
    
    if not os.path.exists(PROFILE_PATH):
      os.makedirs(PROFILE_PATH)
    with open(filename, "w") as f:
      f.write(visitor)

  return visitor

def alert(message,title="VietMedia"):
  xbmcgui.Dialog().ok(title,"",message)

def notify(message='', header=None, time=5000, image=''):
  if header is None:
      header = ADDON_NAME
  xbmc.executebuiltin('Notification("%s", "%s", "%d", "%s")' %
                      (header, message, time, image))

def extract(key, enc):
  dec = []
  enc = base64.urlsafe_b64decode(enc)
  for i in range(len(enc)):
      key_c = key[i % len(key)]
      dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
      dec.append(dec_c)
  return "".join(dec)

def choose_server(data):
  servers = []
  servers_items = []
  for i, item in enumerate(data["items"]):
    servers_items.append(item["title"])
    servers.append(item)
  dialog = xbmcgui.Dialog()
  selected_server_index = dialog.select('Choose a server', servers_items)
  if selected_server_index >=0:
    server_url = servers[selected_server_index]["url"].replace("plugin://%s" % ADDON_ID, VIETMEDIA_HOST ) + sys.argv[2]
    server_json = fetch_data(server_url)
    if not server_json:
      return
    
    if server_json.get('content_type'): #episodes
      return server_json

    if server_json.get('error'):
      alert(server_json['error'])
      return
    if server_json.get("url"):
      play(server_json)

def play(data):
  link = data["url"]
  if 'phimhd3s.com' in link:
    client_id = client.client_id_1()
    if client_id is not None:
      link = link.replace('dc469e7a3c7f76e5bfcc0e104526fb85',client_id)

  item = xbmcgui.ListItem(path=link, thumbnailImage=xbmc.getInfoLabel("ListItem.Art(thumb)"))
  xbmcplugin.setResolvedUrl(HANDLE, True, item)

  if data.get('subtitle'):
    subtitle = data.get('subtitle')
    subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
    subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
    try:
      if os.path.exists(subfile):
        os.remove(subfile)
      f = urllib2.urlopen(subtitle)
      with open(subfile, "wb") as code:
        code.write(f.read())
      xbmc.sleep(3000)
      xbmc.Player().setSubtitles(subfile)
    except:
      notify('Không tải được phụ đề phim.')

def go():
  url = sys.argv[0].replace("plugin://%s" % ADDON_ID, VIETMEDIA_HOST ) + sys.argv[2]
  if url == VIETMEDIA_HOST + '/':
    url += 'play/v1'
  
  #Settings
  if ':settings' in url:
    ADDON.openSettings()
    return
  #Search
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
  data = fetch_data(url)
  if not data:
      return
  if data.get('error'):
    alert(data['error'])
    return

  if data.get("url"):
    play(data)
    return

  if data["content_type"] and data["content_type"] == "servers":
    data = choose_server(data)
    if not data:
      return

  if data["content_type"]:
      xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
      xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
      xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATE)
      xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_GENRE)
      xbmcplugin.setContent(HANDLE, data["content_type"])

  listitems = range(len(data["items"]))
  for i, item in enumerate(data["items"]):
      listItem = xbmcgui.ListItem(label=item["label"], label2=item["label2"], iconImage=item["icon"], thumbnailImage=item["thumbnail"])
      if item.get("info"):
          listItem.setInfo("video", item["info"])
      if item.get("stream_info"):
          for type_, values in item["stream_info"].items():
              listItem.addStreamInfo(type_, values)
      if item.get("art"):
          listItem.setArt(item["art"])
      if item.get("context_menu"):
          listItem.addContextMenuItems(item["context_menu"])
      listItem.setProperty("isPlayable", item["is_playable"] and "true" or "false")
      if item.get("properties"):
          for k, v in item["properties"].items():
              listItem.setProperty(k, v)
      listitems[i] = (item["path"], listItem, not item["is_playable"])

  xbmcplugin.addDirectoryItems(HANDLE, listitems, totalItems=len(listitems))
  xbmcplugin.endOfDirectory(HANDLE, succeeded=True, updateListing=False, cacheToDisc=True)

go()
