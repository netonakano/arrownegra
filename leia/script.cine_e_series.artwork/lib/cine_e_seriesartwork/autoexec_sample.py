# -*- coding: UTF-8 -*-
#######################################################################

# Addon Name: AutoExec for cine_e_series
# Addon id: script.cine_e_series.artwork
# Addon Provider: ArrowNegra

import xbmcvfs,xbmcgui
from placentaartwork import theme_setter

def main():
    try:
        theme_setter.Apply_Theme('Collusion')
        xbmcvfs.delete('special://userdata/autoexec.py')
    except Exception, e:
        xbmcvfs.delete('special://userdata/autoexec.py')

if __name__ == '__main__':
    main()