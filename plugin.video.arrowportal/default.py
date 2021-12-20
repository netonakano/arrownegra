#py3
#!/usr/bin/python
# -*- coding: utf-8 -*-
 # ############Imports#############

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import base64
import os
import re
import unicodedata
import requests
import time
import string
import sys
import urllib
import urllib.request
import json
import datetime
import zipfile
import shutil
from resources.modules import client, control, tools, shortlinks
from datetime import date
import xml.etree.ElementTree as ElementTree
import base64 as b


#################################

def addonInstalled(script_name):
    return xbmc.getCondVisibility('System.HasAddon(%s)' % script_name) \
        == 1


#############Defined Strings#############

addon_id = 'plugin.video.arrowportal'
selfAddon = xbmcaddon.Addon(id=addon_id)
icon = xbmc.translatePath(os.path.join('special://home/addons/'
                          + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/'
                            + addon_id, 'fanart.jpg'))

################Pic###############

livetv = \
    xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arrowportal/resources/pic/icon.png'
                       ))
filme = \
    xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arrowportal/resources/pic/icon.png'
                       ))
serie = \
    xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arrowportal/resources/pic/icon.png'
                       ))
suche = \
    xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arrowportal/resources/pic/icon.png'
                       ))



with urllib.request.urlopen("https://raw.githubusercontent.com/arrownegra/addon/main/addonk-pt/live.txt") as url:
    portal = url.read().decode('utf-8')

with urllib.request.urlopen("https://raw.githubusercontent.com/arrownegra/addon/main/addonk-pt/user.txt") as url2:
    username = url2.read().decode('utf-8')

with urllib.request.urlopen("https://raw.githubusercontent.com/arrownegra/addon/main/addonk-pt/pass.txt") as url3:
    password = url3.read().decode('utf-8')




live_url = \
    portal+'/enigma2.php?username='+username+'&password='+password+'&type=get_live_categories' \

vod_url = \
    portal+'/enigma2.php?username='+username+'&password='+password+'&type=get_vod_categories' \

panel_api = '%s/panel_api.php?username=%s&password=%s' % (portal,username,password)

play_url = '%s/live/%s/%s/' % (portal,username, password)

Series_url = \
    portal+'/enigma2.php?username='+username+'&password='+password+'&type=get_series_categories' \


Guide = \
    xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arrowportal/resources/catchup'
                       , 'guide.xml'))
GuideLoc = \
    xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arrowportal/resources/catchup'
                       , 'g'))

advanced_settings = xbmc.translatePath('special://home/addons/'
        + addon_id + '/resources/advanced_settings')
advanced_settings_target = \
    xbmc.translatePath(os.path.join('special://home/userdata',
                       'advancedsettings.xml'))


#########################################




def home():

    # tools.addDir('Account Information','url',6,icon,fanart,'')

    tools.addDir(
        '[B]ARROW.PORTAL TV[/B]',
        'live',
        1,
        livetv,
        fanart,
        '',
        )

    # tools.addDir('Catchup TV','url',12,icon,fanart,'')
    # if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
        # tools.addDir('TV Guide','pvr',7,icon,fanart,'')

    tools.addDir(
        '[B]ARROW.PORTAL FILMES[/B]',
        'vod',
        3,
        filme,
        fanart,
        '',
        )
    tools.addDir(
        '[B]ARROW.PORTAL SERIES[/B]',
        Series_url,
        24,
        serie,
        fanart,
        '',
        )
#    tools.addDir(
#        'ARROW.PORTAL SEARCH',
#        'url',
#        5,
#        suche,
#        fanart,
#        '',
#        )


    # tools.addDir('Settings','url',8,icon,fanart,'')
    # tools.addDir('Extras','url',16,icon,fanart,'')

def livecategory(url):

    open = tools.OPEN_URL(live_url)
    all_cats = tools.regex_get_all(open, '<channel>', '</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a, '<title>', '</title>')
        name = base64.b64decode(name).decode("utf-8")
        url1 = tools.regex_from_to(a, '<playlist_url>',
                                   '</playlist_url>'
                                   ).replace('<![CDATA[', ''
                ).replace(']]>', '')
        tools.addDir(
            name,
            url1,
            2,
            icon,
            fanart,
            '',
            )


def Livelist(url):
    open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open, '<channel>', '</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a, '<title>', '</title>')
        name = base64.b64decode(name).decode("utf-8")
        xbmc.log(str(name))
        try:
            name = re.sub('\[.*?min ', '-', name)
        except:
            pass
        thumb = tools.regex_from_to(a, '<desc_image>', '</desc_image>'
                                    ).replace('<![CDATA[', ''
                ).replace(']]>', '')
        url1 = tools.regex_from_to(a, '<stream_url>', '</stream_url>'
                                   ).replace('<![CDATA[', ''
                ).replace(']]>', '')
        desc = tools.regex_from_to(a, '<description>', '</description>')
        tools.addDir(
            name,
            url1,
            4,
            thumb,
            fanart,
            base64.b64decode(desc),
            )


def vod(url):
    if url == 'vod':
        open = tools.OPEN_URL(vod_url)
    else:
        open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open, '<channel>', '</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a, '<title>', '</title>')
            url1 = tools.regex_from_to(a, '<playlist_url>',
                    '</playlist_url>').replace('<![CDATA[', ''
                    ).replace(']]>', '')
            tools.addDir(
                str(base64.b64decode(name).decode("utf-8") ).replace('?', ''),
                url1,
                3,
                icon,
                fanart,
                '',
                )
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a, '<title>', '</title>')
                    name = base64.b64decode(name).decode("utf-8")
                    thumb = tools.regex_from_to(a, '<desc_image>',
                            '</desc_image>').replace('<![CDATA[', ''
                            ).replace(']]>', '')
                    url = tools.regex_from_to(a, '<stream_url>',
                            '</stream_url>').replace('<![CDATA[', ''
                            ).replace(']]>', '')
                    desc = tools.regex_from_to(a, '<description>',
                            '</description>')
                    desc = base64.b64decode(desc).decode("utf-8")
                    plot = tools.regex_from_to(desc, 'PLOT:', '\n')
                    cast = tools.regex_from_to(desc, 'CAST:', '\n')
                    ratin = tools.regex_from_to(desc, 'RATING:', '\n')
                    year = tools.regex_from_to(desc, 'RELEASEDATE:',
                            '\n').replace(' ', '-')
                    year = re.compile('-.*?-.*?-(.*?)-',
                            re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc, 'DURATION_SECS:',
                            '\n')
                    genre = tools.regex_from_to(desc, 'GENRE:', '\n')
                    tools.addDirMeta(
                        str(name).replace('[/COLOR].', '.[/COLOR]'),
                        url,
                        4,
                        thumb,
                        fanart,
                        plot,
                        str(year).replace("['", '').replace("']", ''),
                        str(cast).split(),
                        ratin,
                        runt,
                        genre,
                        )
                except:
                    pass
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            else:
                name = tools.regex_from_to(a, '<title>', '</title>')
                name = base64.b64decode(name).decode("utf-8")
                thumb = tools.regex_from_to(a, '<desc_image>',
                        '</desc_image>').replace('<![CDATA[', ''
                        ).replace(']]>', '')
                url = tools.regex_from_to(a, '<stream_url>',
                        '</stream_url>').replace('<![CDATA[', ''
                        ).replace(']]>', '')
                desc = tools.regex_from_to(a, '<description>',
                        '</description>')
                tools.addDir(
                    name,
                    url,
                    4,
                    thumb,
                    fanart,
                    base64.b64decode(desc).decode("utf-8") ,
                    )


#########################################

def Scat(url):
    open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open, '<channel>', '</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a, '<title>', '</title>')
            url1 = tools.regex_from_to(a, '<playlist_url>',
                    '</playlist_url>').replace('<![CDATA[', ''
                    ).replace(']]>', '')
            tools.addDir(
                str(base64.b64decode(name).decode("utf-8") ).replace('?', ''),
                url1,
                20,
                icon,
                fanart,
                '',
                )
        else:
            print('Test')


def Seasons(url):
    open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open, '<channel>', '</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a, '<category_id>', '</category_id>')
        url1 = tools.regex_from_to(a, '<playlist_url>',
                                   '</playlist_url>'
                                   ).replace('<![CDATA[', ''
                ).replace(']]>', '')
        tools.addDir(
            ('Season ' + name).replace('?', ''),
            url1,
            22,
            icon,
            fanart,
            '',
            )


##########################################

def eps(url):
    open = tools.OPEN_URL(url)

    # print open

    all_cats = tools.regex_get_all(open, '<channel>', '</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a, '<title>', '</title>')
        url1 = tools.regex_from_to(a, '<stream_url>', '</stream_url>'
                                   ).replace('<![CDATA[', ''
                ).replace(']]>', '')
        tools.addDir(
            str(base64.b64decode(name).decode("utf-8") ).replace('?', ''),
            url1,
            4,
            icon,
            fanart,
            '',
            )


##########################################

def Series(url):
    open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open, '<channel>', '</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a, '<title>', '</title>')
            url1 = tools.regex_from_to(a, '<playlist_url>',
                    '</playlist_url>').replace('<![CDATA[', ''
                    ).replace(']]>', '')
            tools.addDir(
                str(base64.b64decode(name).decode("utf-8") ).replace('?', ''),
                url1,
                21,
                icon,
                fanart,
                '',
                )
        else:
            pass


##########################################

def catchup():
    loginurl = \
        '%s/get.php?username=%s&password=%s&type=m3u_plus&output=ts' \
        % (live, username, password)
    try:
        connection = urllib.request.urlopen(loginurl)
        print(connection.getcode())
        connection.close()

        # playlist found, user active & login correct, proceed to addon

        pass
    except:
        xbmcgui.Dialog().ok('[COLOR white]Expired Account[/COLOR]',
                            '[COLOR white]You cannot use this service with an expired account[/COLOR]'
                            , ' ',
                            '[COLOR white]Please check your account information[/COLOR]'
                            )
        sys.exit(1)
        xbmc.executebuiltin('Dialog.Close(busydialog)')

    url = '%s/xmltv.php?username=%s&password=%s' % (live, username,
            password)
    DownloaderClass(url, GuideLoc + 'uide.xml')

    f = open(Guide, 'r+')
    input = open(Guide).read().decode('UTF-8')
    output = unicodedata.normalize('NFKD', input).encode('ASCII',
            'ignore')
    f.write(output)
    f.truncate()
    f.close()
    listcatchup()


def listcatchup():
    open = tools.OPEN_URL(panel_api)
    all = tools.regex_get_all(open, '{"num', 'direct')
    for a in all:
        if '"tv_archive":1' in a:
            name = tools.regex_from_to(a, '"epg_channel_id":"', '"')
            thumb = tools.regex_from_to(a, '"stream_icon":"', '"'
                    ).replace('\/', '/')
            id = tools.regex_from_to(a, 'stream_id":"', '"')
            tools.addDir(
                name.replace('ENT:', '[COLOR blue]ENT:[/COLOR]'
                             ).replace('DOC:',
                        '[COLOR blue]DOC:[/COLOR]').replace('MOV:',
                        '[COLOR blue]MOV:[/COLOR]').replace('SSS:',
                        '[COLOR blue]SSS[/COLOR]').replace('BTS:',
                        '[COLOR blue]BTS:[/COLOR]').replace('TEST',
                        '[COLOR blue]TEST[/COLOR]').replace('Install',
                        '[COLOR blue]Install[/COLOR]').replace('24/7',
                        '[COLOR blue]24/7[/COLOR]').replace('INT:',
                        '[COLOR blue]INT:[/COLOR]').replace('DE:',
                        '[COLOR blue]DE:[/COLOR]').replace('FR:',
                        '[COLOR blue]FR:[/COLOR]').replace('PL:',
                        '[COLOR blue]PL:[/COLOR]').replace('AR:',
                        '[COLOR blue]AR:[/COLOR]').replace('LIVE:',
                        '[COLOR blue]LIVE:[/COLOR]').replace('ES:',
                        '[COLOR blue]ES:[/COLOR]').replace('IN:',
                        '[COLOR blue]IN:[/COLOR]').replace('PK:',
                        '[COLOR blue]PK:[/COLOR]'),
                'url',
                13,
                thumb,
                fanart,
                id,
                )


def tvarchive(name, description):
    name = str(name.replace('[COLOR blue]ENT:[/COLOR]', 'ENT:'
               ).replace('[COLOR blue]DOC:[/COLOR]', 'DOC:'
               ).replace('[COLOR blue]MOV:[/COLOR]', 'MOV'
               ).replace('[COLOR blue]SSSS[/COLOR]', 'SSS:'
               ).replace('[COLOR blue]BTS:[/COLOR]', 'BTS:'
               ).replace('[COLOR blue]INT:[/COLOR]', 'INT:'
               ).replace('[COLOR blue]DE:[/COLOR]', 'DE:'
               ).replace('[COLOR blue]FR:[/COLOR]', 'FR:'
               ).replace('[COLOR blue]PL:[/COLOR]', 'PL:'
               ).replace('[COLOR blue]AR:[/COLOR]', 'AR:'
               ).replace('[COLOR blue]LIVE:[/COLOR]', 'LIVE:'
               ).replace('[COLOR blue]ES:[/COLOR]', 'ES:'
               ).replace('[COLOR blue]IN:[/COLOR]', 'IN:'
               ).replace('[COLOR blue]PK:[/COLOR]', 'PK'))
    filename = open(Guide)
    tree = ElementTree.parse(filename)
    pony = 'apples'
    import datetime as dt
    from datetime import time
    date3 = datetime.datetime.now() - datetime.timedelta(days=5)
    date = str(date3)
    now = str(datetime.datetime.now()).replace('-', '').replace(':', ''
            ).replace(' ', '')
    programmes = tree.findall('programme')
    for programme in programmes:
        if name in programme.attrib.get('channel'):
            showtime = programme.attrib.get('start')
            (head, sep, tail) = showtime.partition(' +')
            date = str(date).replace('-', '').replace(':', ''
                    ).replace(' ', '')
            (year, month, day) = showtime.partition('2017')
            kanalinimi = programme.find('title').text + showtime
            day = day[:-6]
            if head > date:
                if head < now:
                    head2 = head
                    head2 = head2[:4] + '/' + head2[4:]
                    head = head[:4] + '-' + head[4:]
                    head2 = head2[:7] + '/' + head2[7:]
                    head = head[:7] + '-' + head[7:]
                    head2 = head2[:10] + ' - ' + head2[10:]
                    head = head[:10] + ':' + head[10:]
                    head2 = head2[:15] + ':' + head2[15:]
                    head = head[:13] + '-' + head[13:]
                    head2 = head2[:-2]
                    head = head[:-2]
                    poo1 = \
                        '%s:%s/streaming/timeshift.php?username=%s&password=%s&stream=%s&start=' \
                        % (host, port, username, password, description)
                    pony = poo1 + str(head) + '&duration=240'
                    head2 = '[COLOR white]%s - [/COLOR]' % head2
                    kanalinimi = str(head2) + programme.find('title'
                            ).text
                    desc = programme.find('desc').text
                    tools.addDir(
                        kanalinimi,
                        pony,
                        4,
                        icon,
                        fanart,
                        desc,
                        )
                    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')


def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up', 'Fetching latest Catch Up...'
              , ' ', ' ')
    dp.update(0)
    start_time = time.time()
    urllib.request.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs,
                       fs, dp, start_time))


def _pbhook(
    numblocks,
    blocksize,
    filesize,
    dp,
    start_time,
    ):
    try:
        percent = min(numblocks * blocksize * 100 / filesize, 100)
        currently_downloaded = float(numblocks) * blocksize / (1024
                * 1024)
        kbps_speed = numblocks * blocksize / (time.time() - start_time)
        if kbps_speed > 0:
            eta = (filesize - numblocks * blocksize) / kbps_speed
        else:
            eta = 0
        kbps_speed = kbps_speed / 1024
        mbps_speed = kbps_speed / 1024
        total = float(filesize) / (1024 * 1024)
        mbs = '[COLOR white]%.02f MB of less than 5MB[/COLOR]' \
            % currently_downloaded
        e = '[COLOR white]Speed:  %.02f Mb/s ' % mbps_speed + '[/COLOR]'
        dp.update(percent, mbs, e)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        dialog = xbmcgui.Dialog()
        dialog.ok('Error', 'The download was cancelled.')

        sys.exit()
        dp.close()


#####################################################################
#py3
# def tvguide():
    # if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
        # dialog = xbmcgui.Dialog().select('Select a TV Guide', ['PVR TV Guide','iVue TV Guide'])
        # if dialog==0:
            # xbmc.executebuiltin('ActivateWindow(TVGuide)')
        # elif dialog==1:
            # xbmc.executebuiltin('RunAddon(script.ivueguide)')
    # elif not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
        # xbmc.executebuiltin('RunAddon(script.ivueguide)')
    # elif xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and not xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
        # xbmc.executebuiltin('ActivateWindow(TVGuide)')

class Player(xbmc.Player):
    pass



def stream_video(url):
    progress = xbmcgui.DialogProgress()
    progress.create('ARROW.PORTAL', u'Starting the stream...')
    progress.update(15)
    url = str(url).replace('USERNAME', username).replace('PASSWORD',
            password)
    liz = xbmcgui.ListItem('')
    liz.setArt({'icon': 'DefaultVideo.png', 'thumb': icon})
    liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
    liz.setProperty('IsPlayable', 'true')
    liz.setPath(str(url))
    progress.update(30)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    progress.update(45)
    abortReason = ''
    step = 1
    t = time.time()
    player = Player()
    try:
        while not abortReason:
            if progress.iscanceled():
                abortReason = 'cancelled'
            elif time.time() - t > 30:
                abortReason = 'timeout'
            elif step == 1:
                if player.isPlaying():
                    progress.update(60)
                    step = 2
            if step == 2:
                if xbmc.getInfoLabel('VideoPlayer.VideoResolution'):
                    progress.update(75)
                    step = 3
            if step == 3:
                if player.getTime() > 0.01:
                    progress.update(100)

                    break
            if not abortReason:
                xbmc.sleep(15)

        if abortReason:
            player.stop()
            xbmcgui.Dialog().ok('The channel is not available', 'Please try again.')
            #raise RuntimeError('Stream died! reason=%s' % abortReason)
    finally:
        del player


def searchdialog():
    search = control.inputDialog(heading='ARROW.PORTAL Search:')
    if search == '':
        return
    else:
        return search


def search():
    if mode == 3:
        return False
    text = searchdialog()
    if not text:
        xbmc.executebuiltin('XBMC.Notification([COLOR red][B]Search is Empty[/B][/COLOR],Aborting search,4000,'
                             + icon + ')')
        return
    xbmc.log(str(text))
    open = tools.OPEN_URL(panel_api)
    all_chans = tools.regex_get_all(open, '{"num":', 'epg')
    for a in all_chans:
        name = tools.regex_from_to(a, 'name":"', '"').replace('\/', '/')
        url = tools.regex_from_to(a, '"stream_id":"', '"')
        thumb = tools.regex_from_to(a, 'stream_icon":"', '"'
                                    ).replace('\/', '/')
        if text in name.lower():
            tools.addDir(
                name,
                play_url + url + '.ts',
                4,
                thumb,
                fanart,
                '',
                )
        elif text not in name.lower() and text in name:
            tools.addDir(
                name,
                play_url + url + '.ts',
                4,
                thumb,
                fanart,
                '',
                )


def settingsmenu():
    tools.addDir(
        'Edit Advanced Settings',
        'ADS',
        10,
        icon,
        fanart,
        '',
        )
    tools.addDir(
        'Log Out',
        'LO',
        10,
        icon,
        fanart,
        '',
        )


def addonsettings(url, description):
    if url == 'CC':
        tools.clear_cache()
    elif url == 'AS':
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % addon_id)
    elif url == 'ADS':
        dialog = xbmcgui.Dialog().select('Edit Advanced Settings', [
            'Enable Fire TV Stick AS',
            'Enable Fire TV AS',
            'Enable 1GB Ram or Lower AS',
            'Enable 2GB Ram or Higher AS',
            'Enable Nvidia Shield AS',
            'Disable AS',
            ])
        if dialog == 0:
            advancedsettings('stick')
            xbmcgui.Dialog().ok('ARROW.PORTAL', 'Set Advanced Settings')
        elif dialog == 1:
            advancedsettings('firetv')
            xbmcgui.Dialog().ok('ARROW.PORTAL', 'Set Advanced Settings')
        elif dialog == 2:
            advancedsettings('lessthan')
            xbmcgui.Dialog().ok('ARROW.PORTAL', 'Set Advanced Settings')
        elif dialog == 3:
            advancedsettings('morethan')
            xbmcgui.Dialog().ok('ARROW.PORTAL', 'Set Advanced Settings')
        elif dialog == 4:
            advancedsettings('shield')
            xbmcgui.Dialog().ok('ARROW.PORTAL', 'Set Advanced Settings')
        elif dialog == 5:
            advancedsettings('remove')
            xbmcgui.Dialog().ok('IPIV is Easy',
                                'Advanced Settings Removed')
    elif url == 'ADS2':
        dialog = \
            xbmcgui.Dialog().select('Select Your Device Or Closest To',
                                    ['Fire TV Stick ', 'Fire TV',
                                    '1GB Ram or Lower',
                                    '2GB Ram or Higher', 'Nvidia Shield'
                                    ])
        if dialog == 0:
            advancedsettings('stick')
            xbmcgui.Dialog().ok('IPIV is Easy', 'Set Advanced Settings')
        elif dialog == 1:
            advancedsettings('firetv')
            xbmcgui.Dialog().ok('IPIV is Easy', 'Set Advanced Settings')
        elif dialog == 2:
            advancedsettings('lessthan')
            xbmcgui.Dialog().ok('IPIV is Easy', 'Set Advanced Settings')
        elif dialog == 3:
            advancedsettings('morethan')
            xbmcgui.Dialog().ok('IPIV is Easy', 'Set Advanced Settings')
        elif dialog == 4:
            advancedsettings('shield')
            xbmcgui.Dialog().ok('IPIV is Easy', 'Set Advanced Settings')
    elif url == 'tv':
        dialog = xbmcgui.Dialog().select('Select a TV Guide to Setup',
                ['iVue TV Guide', 'PVR TV Guide', 'Both'])
        if dialog == 0:
            ivueint()
            xbmcgui.Dialog().ok('IPIV is Easy',
                                'iVue Integration Complete')
        elif dialog == 1:
            pvrsetup()
            xbmcgui.Dialog().ok('IPIV is Easy',
                                'PVR Integration Complete')
        elif dialog == 2:
            pvrsetup()
            ivueint()
            xbmcgui.Dialog().ok('IPIV is Easy',
                                'PVR & iVue Integration Complete')
    elif url == 'ST':
        xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.arrowportal/resources/modules/speedtest.py")'
                            )
    elif url == 'META':
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('meta', 'false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('meta', 'true')
            xbmc.executebuiltin('Container.Refresh')
    elif url == 'LO':
        xbmcaddon.Addon().setSetting('Username', '')
        xbmcaddon.Addon().setSetting('Password', '')
        xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)'
                            )
        xbmc.executebuiltin('Container.Refresh')
    elif url == 'UPDATE':
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('update', 'false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('update', 'true')
            xbmc.executebuiltin('Container.Refresh')


def advancedsettings(device):
    if device == 'stick':
        file = open(os.path.join(advanced_settings, 'stick.xml'))
    elif device == 'firetv':
        file = open(os.path.join(advanced_settings, 'firetv.xml'))
    elif device == 'lessthan':
        file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
    elif device == 'morethan':
        file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
    elif device == 'shield':
        file = open(os.path.join(advanced_settings, 'shield.xml'))
    elif device == 'remove':
        os.remove(advanced_settings_target)

    try:
        read = file.read()
        f = open(advanced_settings_target, mode='w+')
        f.write(read)
        f.close()
    except:
        pass


def pvrsetup():
    correctPVR()
    return


def asettings():
    choice = xbmcgui.Dialog().yesno('IPIV is Easy',
                                    'Please Select The RAM Size of Your Device'
                                    , yeslabel='Less than 1GB RAM',
                                    nolabel='More than 1GB RAM')
    if choice:
        lessthan()
    else:
        morethan()


def morethan():
    file = open(os.path.join(advanced_settings, 'morethan.xml'))
    a = file.read()
    f = open(advanced_settings_target, mode='w+')
    f.write(a)
    f.close()


def lessthan():
    file = open(os.path.join(advanced_settings, 'lessthan.xml'))
    a = file.read()
    f = open(advanced_settings_target, mode='w+')
    f.write(a)
    f.close()


def userpopup():
    kb = xbmc.Keyboard('', 'heading', True)
    kb.setHeading('Enter Username')
    kb.setHiddenInput(False)
    kb.doModal()
    if kb.isConfirmed():
        text = kb.getText()
        return text
    else:
        return False


def passpopup():
    kb = xbmc.Keyboard('', 'heading', True)
    kb.setHeading('Enter Password')
    kb.setHiddenInput(False)
    kb.doModal()
    if kb.isConfirmed():
        text = kb.getText()
        return text
    else:
        return False


def accountinfo():
    open = tools.OPEN_URL(panel_api)
    try:
        username = tools.regex_from_to(open, '"username":"', '"')
        password = tools.regex_from_to(open, '"password":"', '"')
        status = tools.regex_from_to(open, '"status":"', '"')
        connects = tools.regex_from_to(open, '"max_connections":"', '"')
        active = tools.regex_from_to(open, '"active_cons":"', '"')
        expiry = tools.regex_from_to(open, '"exp_date":"', '"')
        expiry = \
            datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M'
                )
        expreg = re.compile('^(.*?)/(.*?)/(.*?)$',
                            re.DOTALL).findall(expiry)
        for (day, month, year) in expreg:
            month = tools.MonthNumToName(month)
            year = re.sub(' -.*?$', '', year)
            expiry = month + ' ' + day + ' - ' + year
            ip = tools.getlocalip()
            extip = tools.getexternalip()
            tools.addDir(
                '[COLOR blue]Username :[/COLOR] ' + username,
                '',
                '',
                icon,
                fanart,
                '',
                )
            tools.addDir(
                '[COLOR blue]Password :[/COLOR] ' + password,
                '',
                '',
                icon,
                fanart,
                '',
                )
            tools.addDir(
                '[COLOR blue]Expiry Date:[/COLOR] ' + expiry,
                '',
                '',
                icon,
                fanart,
                '',
                )
            tools.addDir(
                '[COLOR blue]Account Status :[/COLOR] %s' % status,
                '',
                '',
                icon,
                fanart,
                '',
                )
            tools.addDir(
                '[COLOR blue]Current Connections:[/COLOR] ' + active,
                '',
                '',
                icon,
                fanart,
                '',
                )
            tools.addDir(
                '[COLOR blue]Allowed Connections:[/COLOR] ' + connects,
                '',
                '',
                icon,
                fanart,
                '',
                )
            tools.addDir(
                '[COLOR blue]Local IP Address:[/COLOR] ' + ip,
                '',
                '',
                icon,
                fanart,
                '',
                )
            tools.addDir(
                '[COLOR blue]External IP Address:[/COLOR] ' + extip,
                '',
                '',
                icon,
                fanart,
                '',
                )
    except:
        pass


def correctPVR():

    addon = xbmcaddon.Addon('plugin.video.arrowportaltPVRtv')
    username_text = addon.getSetting(id='Username')
    password_text = addon.getSetting(id='Password')
    jsonSetPVR = \
        '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
    IPTVon = \
        '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
    nulldemo = \
        '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
    loginurl = \
        '%s/get.php?username=%s&password=%s&type=m3u_plus&output=ts' \
        % (live, username, password)
    EPGurl = \
        '%s/xmltv.php?username=%s&password=%s&type=m3u_plus&output=ts' \
        % (live, username, password)

    xbmc.executeJSONRPC(jsonSetPVR)
    xbmc.executeJSONRPC(IPTVon)
    xbmc.executeJSONRPC(nulldemo)

    moist = xbmcaddon.Addon('pvr.iptvsimple')
    moist.setSetting(id='m3uUrl', value=loginurl)
    moist.setSetting(id='epgUrl', value=EPGurl)
    moist.setSetting(id='m3uCache', value='false')
    moist.setSetting(id='epgCache', value='false')
    xbmc.executebuiltin('Container.Refresh')


def ivueint():
    ivuesetup.iVueInt()


def tvguidesetup():
    dialog = xbmcgui.Dialog().yesno('ARROW.PORTAL',
                                    'Would You like us to Setup the TV Guide for You?'
                                    )
    if dialog:
        dialog = xbmcgui.Dialog().select('Select a TV Guide to Setup',
                ['iVue TV Guide', 'PVR TV Guide', 'Both'])
        if dialog == 0:
            ivueint()
            xbmcgui.Dialog().ok('ARROW.PORTAL', 'iVue Integration Complete'
                                )
        elif dialog == 1:
            pvrsetup()
            xbmcgui.Dialog().ok('ARROW.PORTAL', 'PVR Integration Complete')
        elif dialog == 2:
            pvrsetup()
            ivueint()
            xbmcgui.Dialog().ok('ARROW.PORTAL',
                                'PVR & iVue Integration Complete')


def num2day(num):
    if num == '0':
        day = 'monday'
    elif num == '1':
        day = 'tuesday'
    elif num == '2':
        day = 'wednesday'
    elif num == '3':
        day = 'thursday'
    elif num == '4':
        day = 'friday'
    elif num == '5':
        day = 'saturday'
    elif num == '6':
        day = 'sunday'
    return day


def extras():
    tools.addDir(
        'Create a Short M3U & EPG URL',
        'url',
        17,
        icon,
        fanart,
        '',
        )
    tools.addDir(
        'Integrate With TV Guide',
        'tv',
        10,
        icon,
        fanart,
        '',
        )
    tools.addDir(
        'Run a Speed Test',
        'ST',
        10,
        icon,
        fanart,
        '',
        )
    tools.addDir(
        'Clear Cache',
        'CC',
        10,
        icon,
        fanart,
        '',
        )


params = tools.get_params()
url = None
name = None
mode = None
iconimage = None
description = None
query = None
type = None

try:
    url = urllib.parse.unquote_plus(params['url'])
except:
    pass
try:
    name = urllib.parse.unquote_plus(params['name'])
except:
    pass
try:
    iconimage = urllib.parse.unquote_plus(params['iconimage'])
except:
    pass
try:
    mode = int(params['mode'])
except:
    pass
try:
    description = urllib.parse.unquote_plus(params['description'])
except:
    pass
try:
    query = urllib.parse.unquote_plus(params['query'])
except:
    pass
try:
    type = urllib.parse.unquote_plus(params['type'])
except:
    pass

if mode == None or url == None or len(url) < 1:
    home()
elif mode == 1:

    livecategory(url)
elif mode == 2:

    Livelist(url)
elif mode == 3:

    vod(url)
elif mode == 4:

    stream_video(url)
elif mode == 5:

    search()
elif mode == 6:

    accountinfo()
elif mode == 7:

    tvguide()
elif mode == 8:

    settingsmenu()
elif mode == 9:

    xbmc.executebuiltin('ActivateWindow(busydialog)')
    tools.Trailer().play(url)
    xbmc.executebuiltin('Dialog.Close(busydialog)')
elif mode == 10:

    addonsettings(url, description)
elif mode == 11:

    pvrsetup()
elif mode == 12:

    catchup()
elif mode == 13:

    tvarchive(name, description)
elif mode == 14:

    listcatchup2()
elif mode == 15:

    ivueint()
elif mode == 16:

    extras()
elif mode == 17:

    shortlinks.Get()
elif mode == 18:

    footballguidesearch(description)
elif mode == 19:

    get()
elif mode == 20:

    Series(url)
elif mode == 21:

    Seasons(url)
elif mode == 22:

    eps(url)
elif mode == 24:

    Scat(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
##py3
