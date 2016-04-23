# -*- coding: utf-8 -*-
#https://www.facebook.com/groups/vietkodi/

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.vietmedia.movie')
__language__ = __settings__.getLocalizedString
__profile__ = xbmc.translatePath( __settings__.getAddonInfo('profile') ).decode("utf-8")

name = "Go to VietmediaF"
liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="")
liz.setInfo( type="Video", infoLabels={ "Title": name } )
u = 'plugin://plugin.video.vietmediaF'  
xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
