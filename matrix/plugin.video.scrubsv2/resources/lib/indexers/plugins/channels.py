# -*- coding: utf-8 -*-

import re
import sys

from six.moves.urllib_parse import quote_plus

from resources.lib.indexers import movies

from resources.lib.modules import client
from resources.lib.modules import workers
from resources.lib.modules import log_utils


class channels:
    def __init__(self):
        self.list = []
        self.items = []
        self.sky_now_link = 'http://epgservices.sky.com/5.1.1/api/2.0/channel/json/%s/now/nn/3'


    def sky_list(self, channel, id):
        try:
            url = self.sky_now_link % id
            results = client.scrapePage(url).json()
            results = results['listings'][id]
            for result in results:
                title = result['t']
                title = client.replaceHTMLCodes(title)
                if not title in str(self.items):
                    year = result['d']
                    year = re.findall('[(](\d{4})[)]', year)[0].strip()
                    self.items.append((title, year, channel))
        except:
            #log_utils.log('sky_list', 1)
            pass


    def items_list(self, i):
        try:
            query = '%s&year=%s' % (quote_plus(i[0]), i[1])
            url = movies.movies().tmdb_search_link % query
            item = movies.movies().get(url, create_directory=False)[0]
            item.update({'channel': i[2]})
            self.list.append(item)
        except:
            #log_utils.log('items_list', 1)
            pass


# BBC1_NE = "2155";
# BBC1_HD = "2076";
# BBC2 = "2006";
# BBC3 = "2061";
# BBC4 = "2018";
# ITV1 = "6390";
# ITV1_HD = "6505";
# ITV2_HD = "6452";
# ITV3_HD = "6533";
# ITV4_HD = "6534";
# CHANNEL4 = "1624";
# CHANNEL4_HD = "4075";
# CHANNEL5 = "1829";
# CHANNEL5_HD = "4058";
# SKY1_HD = "4061";
# SKY_ATLANTIC_HD = "4053";
# FX_HD = "4023";


    def get(self):
        try:
            channels_list = [
                ('ActionWomen', '1811'), ('ActionWomen HD', '4020'),
                ('Christmas 24', '4420'), ('Christmas 24+', '4421'),
                ('Film4', '1627'), ('Film4 HD', '4044'), ('Film4+', '1629'),
                ('Horror Channel', '3605'), ('Horror Channel+', '4502'),
                ('ROK', '3542'),
                ('Sky Action', '1001'), ('Sky Action HD', '4014'),
                ('Sky Christmas', '1816'), ('Sky Christmas HD', '4016'),
                ('Sky Comedy', '1002'), ('Sky Comedy HD', '4019'),
                ('Sky Family', '1808'), ('Sky Family HD', '4018'),
                ('Sky Greats', '1815'), ('Sky Greats HD', '4015'),
                ('Sky Hits', '1814'), ('Sky Hits HD', '4033'),
                ('Sky Premiere', '1409'), ('Sky Premiere HD', '4021'), ('Sky Premiere+', '1823'),
                ('Sky ScFi/Horror', '1807'), ('Sky ScFi/Horror HD', '4017'),
                ('Sky Thriller', '1818'), ('Sky Thriller HD', '4062'),
                ('Sony Action', '3708'), ('Sony Action+', '3721'),
                ('Sony Christmas', '3643'), ('Sony Christmas+', '3751'),
                ('Sony Movies', '3709'), ('Sony Movies+', '3771'),
                ('TalkingPictures', '5252'),
                ('TCM Movies', '5605'), ('TCM Movies+', '5275')
            ]
            threads = []
            for i in channels_list:
                threads.append(workers.Thread(self.sky_list, i[0], i[1]))
            [i.start() for i in threads]
            [i.join() for i in threads]
            threads = []
            for i in range(0, len(self.items)):
                threads.append(workers.Thread(self.items_list, self.items[i]))
            [i.start() for i in threads]
            [i.join() for i in threads]
            self.list = sorted(self.list, key=lambda k: k['channel'])
            movies.movies().movieDirectory(self.list)
            return self.list
        except:
            #log_utils.log('get', 1)
            return self.list


