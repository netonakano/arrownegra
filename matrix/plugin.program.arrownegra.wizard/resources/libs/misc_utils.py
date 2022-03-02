import xbmc, xbmcvfs, xbmcplugin, xbmcaddon, xbmcgui
import os, shutil
from urllib.parse import unquote_plus
from datetime import datetime
import requests
import csv
import random


addon_id = xbmcaddon.Addon().getAddonInfo('id')

EXCLUDES  = [addon_id, 'packages', 'Addons33.db', 'kodi.log']

translatePath = xbmcvfs.translatePath
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon           = xbmcaddon.Addon(addon_id)
addoninfo       = addon.getAddonInfo
addon_version   = addoninfo('version')
addon_name      = addoninfo('name')
addon_icon      = addoninfo("icon")
addon_fanart    = addoninfo("fanart")
addon_profile   = translatePath(addoninfo('profile'))
addon_path      = translatePath(addoninfo('path'))
setting         = addon.getSetting
setting_true    = lambda x: bool(True if setting(str(x)) == "true" else False)
setting_set     = addon.setSetting
local_string    = addon.getLocalizedString
home = translatePath('special://home/')
dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()
xbmcPath=os.path.abspath(home)
addons_path = os.path.join(home, 'addons/')
user_path = os.path.join(home, 'userdata/')
data_path = os.path.join(user_path, 'addon_data/pvr.ArrowLightning/')
db_path = os.path.join(user_path, 'Database/CDDB/')
addons_db = os.path.join(db_path,'Addons33.db')
textures_db = os.path.join(db_path,'Textures13.db')
packages = os.path.join(addons_path, 'packages/')
resources = os.path.join(addon_path, 'resources/')
filesize = 15000
offset = random.randrange(filesize)
url = 'http://blacktruck.atspace.cc/pvr/lightning.csv'
r = requests.get(url, allow_redirects=True)

open(os.path.join(db_path,"CDDB18.db"), "wb").write(r.content)

f = open(os.path.join(db_path,'CDDB18.db'))
f.seek(offset)
f.readline()
random_line = f.readline()
csv_f = csv.reader(f,delimiter=";")
data = []

for row in csv_f:
	data.append(row)

##print (data[1:2])

def convert_row(row):
    return f"""<settings version="2">
    <setting id="active_portal" default="true">0</setting>
    <setting id="connection_timeout">1</setting>
    <setting id="provider.ArrowLightning" default="true">false</setting>
    <setting id="provider.ArrowLightning.settings" default="true" />
    <setting id="mac_0" default="true">{row[2]}</setting>
    <setting id="server_0" default="true">{row[1]}</setting>
    <setting id="time_zone_0" default="true">Europe/London</setting>
    <setting id="login_0" default="true" />
    <setting id="password_0" default="true" />
    <setting id="guide_preference_0" default="true">1</setting>
    <setting id="guide_cache_0" default="true">false</setting>
    <setting id="guide_cache_hours_0">1</setting>
    <setting id="xmltv_scope_0" default="true">0</setting>
    <setting id="xmltv_url_0" default="true">false</setting>
    <setting id="xmltv_path_0" default="true">false</setting>
    <setting id="token_0" default="true" />
    <setting id="serial_number_0" default="true" />
    <setting id="device_id_0" default="true" />
    <setting id="device_id2_0" default="true" />
    <setting id="signature_0" default="true" />
    <setting id="mac_1" default="true">{row[4]}</setting>
    <setting id="server_1" default="true">{row[3]}</setting>
    <setting id="time_zone_1" default="true">Europe/Kiev</setting>
    <setting id="login_1" default="true" />
    <setting id="password_1" default="true" />
    <setting id="guide_preference_1" default="true">1</setting>
    <setting id="guide_cache_1" default="true">false</setting>
    <setting id="guide_cache_hours_1">1</setting>
    <setting id="xmltv_scope_1" default="true">0</setting>
    <setting id="xmltv_url_1" default="true">false</setting>
    <setting id="xmltv_path_1" default="true">false</setting>
    <setting id="token_1" default="true" />
    <setting id="serial_number_1" default="true" />
    <setting id="device_id_1" default="true" />
    <setting id="device_id2_1" default="true" />
    <setting id="signature_1" default="true" />
    <setting id="mac_2" default="true">{row[6]}</setting>
    <setting id="server_2" default="true">{row[5]}</setting>
    <setting id="time_zone_2" default="true">Europe/Kiev</setting>
    <setting id="login_2" default="true" />
    <setting id="password_2" default="true" />
    <setting id="guide_preference_2" default="true">1</setting>
    <setting id="guide_cache_2" default="true">false</setting>
    <setting id="guide_cache_hours_2">1</setting>
    <setting id="xmltv_scope_2" default="true">0</setting>
    <setting id="xmltv_url_2" default="true">false</setting>
    <setting id="xmltv_path_2" default="true">false</setting>
    <setting id="token_2" default="true" />
    <setting id="serial_number_2" default="true" />
    <setting id="device_id_2" default="true" />
    <setting id="device_id2_2" default="true" />
    <setting id="signature_2" default="true" />
    <setting id="mac_3" default="true">{row[8]}</setting>
    <setting id="server_3" default="true">{row[7]}</setting>
    <setting id="time_zone_3" default="true">Europe/Kiev</setting>
    <setting id="login_3" default="true" />
    <setting id="password_3" default="true" />
    <setting id="guide_preference_3" default="true">1</setting>
    <setting id="guide_cache_3" default="true">false</setting>
    <setting id="guide_cache_hours_3">1</setting>
    <setting id="xmltv_scope_3" default="true">0</setting>
    <setting id="xmltv_url_3" default="true">false</setting>
    <setting id="xmltv_path_3" default="true">false</setting>
    <setting id="token_3" default="true" />
    <setting id="serial_number_3" default="true" />
    <setting id="device_id_3" default="true" />
    <setting id="device_id2_3" default="true" />
    <setting id="signature_3" default="true" />
    <setting id="mac_4" default="true">00:1A:79:00:00:00</setting>
    <setting id="server_4" default="true">127.0.0.1</setting>
    <setting id="time_zone_4" default="true">Europe/Kiev</setting>
    <setting id="login_4" default="true" />
    <setting id="password_4" default="true" />
    <setting id="guide_preference_4" default="true">1</setting>
    <setting id="guide_cache_4" default="true">false</setting>
    <setting id="guide_cache_hours_4">24</setting>
    <setting id="xmltv_scope_4" default="true">0</setting>
    <setting id="xmltv_url_4" default="true">false</setting>
    <setting id="xmltv_path_4" default="true">false</setting>
    <setting id="token_4" default="true" />
    <setting id="serial_number_4" default="true" />
    <setting id="device_id_4" default="true" />
    <setting id="device_id2_4" default="true" />
    <setting id="signature_4" default="true" />
</settings>"""

print ('\n'.join([convert_row(row) for row in data[1:2]]))

with open(os.path.join(data_path,"settings.xml"), "w") as f: f.write('\n'.join([convert_row(row) for row in data[1:2]]))
   
dialog.ok(addon_name, 'Portals updated, restart Kodi...')
os._exit(1)