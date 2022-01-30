import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json

AddonID = 'plugin.video.arrownegra.play.tv'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')
fanart = Addon.getAddonInfo('fanart')
addonDir = Addon.getAddonInfo('path').decode("utf-8")
libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)

import common

addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)
	
mainURL = "https://raw.githubusercontent.com/arrownegra/addon/main/addonk-pt/arrownegraplay.xml"
tmpPlayList = os.path.join(addon_data_dir, 'tmpPlay')
tmpListFile = os.path.join(addon_data_dir, 'tmpList')
tmpM3U = os.path.join(addon_data_dir, 'tmpM3U')
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')
	
def isM3UDir(url):
	urllib.urlretrieve(url, tmpM3U)
	ss = open(tmpM3U).readline()
	if ss.strip()=="#EXTM3UDIR":
		return True
	return False
	
def Categories(url):
	i = 0
	urllib.urlretrieve(url, tmpPlayList)
	list = common.ReadList(tmpPlayList)
	for item in list:
		mode = 1 if item["url"].find(".plx") > 0 else 2
		name = common.GetEncodeString(item["name"])
		image = item.get('image', '')
		fanart= item.get('fanart')
		if mode == 1:
			logos = ''
		else:
			logos = item.get('logos', '')
		AddDir("[COLOR gold][{0}][/COLOR]".format(name) ,item["url"].encode("utf-8"), mode, image.encode("utf-8"), logos.encode("utf-8"), index=i)
		i += 1

	AddDir("Reset Cache", "".format(sys.argv[0]), 4, image, isFolder=True)
			
def PlxCategory(url):
	tmpList = []
	list = common.plx2list(url)
	background = list[0]["fanart"]
	for channel in list[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("[COLOR gold][{0}][/COLOR]".format(name) ,channel["url"].encode("utf-8"), 1, iconimage, background=fanart.encode("utf-8"))
		else:
			AddDir(name, channel["url"].encode("utf-8"), 3, iconimage, isFolder=False, background=fanart)
			tmpList.append({"url": channel["url"], "image": iconimage.decode("utf-8"), "name": name.decode("utf-8"), "fanart": fanart.decode("utf-8")})
			
	common.SaveList(tmpListFile, tmpList)

def m3uDir(url, logos):

	tmpList = []
	list = common.m3u2list(url)

	for dirchannel in list:
		name = common.GetEncodeString(dirchannel["display_name"])
		image = dirchannel.get("tvg_logo", "")
		if image == "":
			image = dirchannel.get("logo", "")
		if logos is not None and logos != '' and image is not None and image != '' and not image.startswith('http'):
			image = logos + image
		url = common.GetEncodeString(dirchannel["url"])
		AddDir(name ,url, 2, image, isFolder=True)
		tmpList.append({"url": url.decode("utf-8"), "image": image.decode("utf-8"), "name": name.decode("utf-8")})
		
	common.SaveList(tmpListFile, tmpList)
	
def m3uCategory(url, logos):
	if isM3UDir(url):
		m3uDir(url, logos)
		return

	tmpList = []
	list = common.m3u2list(url)

	for channel in list:
		name = common.GetEncodeString(channel["display_name"])
		image = channel.get("tvg_logo", "")
		if image == "":
			image = channel.get("logo", "")
		if logos is not None and logos != '' and image is not None and image != '' and not image.startswith('http'):
			image = logos + image
		url = common.GetEncodeString(channel["url"])
		AddDir(name ,url, 3, image, isFolder=False)
		tmpList.append({"url": url.decode("utf-8"), "image": image.decode("utf-8"), "name": name.decode("utf-8")})

	common.SaveList(tmpListFile, tmpList)
		
def PlayUrl(name, url, iconimage=None):
	print '--- Playing "{0}". {1}'.format(name, url)
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage, logos="", index=-1, move=0, isFolder=True, background=fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&logos="+urllib.quote_plus(logos)+"&index="+str(index)+"&move="+str(move)

	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "Title": name})
	listMode = 21 # Lists
	if background != None:
		liz.setProperty('fanart_image', background)
	if mode == 1 or mode == 2:
		items = [(getLocaleString(10008), 'XBMC.RunPlugin({0}?index={1}&mode=22)'.format(sys.argv[0], index)),
		(getLocaleString(10026), 'XBMC.RunPlugin({0}?index={1}&mode=23)'.format(sys.argv[0], index)),
		(getLocaleString(10027), 'XBMC.RunPlugin({0}?index={1}&mode=24)'.format(sys.argv[0], index)),
		(getLocaleString(10028), 'XBMC.RunPlugin({0}?index={1}&mode=25)'.format(sys.argv[0], index))]
		if mode == 2:
			items.append((getLocaleString(10029), 'XBMC.RunPlugin({0}?index={1}&mode=26)'.format(sys.argv[0], index)))
	elif mode == 3:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(getLocaleString(10009)), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
	elif mode == 32:
		liz.setProperty('IsPlayable', 'true')
		items = [(getLocaleString(10010), 'XBMC.RunPlugin({0}?index={1}&mode=33)'.format(sys.argv[0], index)),
		(getLocaleString(10026), 'XBMC.RunPlugin({0}?index={1}&mode=35)'.format(sys.argv[0], index)),
		(getLocaleString(10027), 'XBMC.RunPlugin({0}?index={1}&mode=36)'.format(sys.argv[0], index)),
		(getLocaleString(10028), 'XBMC.RunPlugin({0}?index={1}&mode=37)'.format(sys.argv[0], index))]
		listMode = 38 # Favourits
	if mode == 1 or mode == 2 or mode == 32:
		items += [(getLocaleString(10030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, listMode)),
		(getLocaleString(10031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, listMode)),
		(getLocaleString(10032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, listMode))]
		liz.addContextMenuItems(items)
		
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?','')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0].lower()] = splitparams[1]
	return param

	
params=get_params()
url=None
logos=None
name=None
mode=None
iconimage=None
description=None
command=None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	logos = urllib.unquote_plus(params.get("logos", ''))
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:        
	mode = int(params["mode"])
except:
	pass
try:        
	index = int(params["index"])
except:
	pass
try:        
	move = int(params["move"])
except:
	pass
	
	
if mode == None:
	Categories(mainURL)
elif mode == 1:
	PlxCategory(url)
elif mode == 2:
	m3uCategory(url, logos)
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage)
elif mode == 4:
	if os.path.exists(tmpPlayList):
		os.remove(tmpPlayList)
	if os.path.exists(tmpListFile):
		os.remove(tmpListFile)
	sys.exit()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
