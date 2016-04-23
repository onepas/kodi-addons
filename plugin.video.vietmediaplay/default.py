# -*- coding: utf-8 -*-
#https://www.facebook.com/groups/vietkodi/

import xbmcplugin
import xbmcgui

name = "Go to VietmediaF"
liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="")
liz.setInfo( type="Video", infoLabels={ "Title": name } )
u = 'plugin://plugin.video.vietmediaF'  
xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

