import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib.request as urllib2,urllib.parse,urllib.error,tarfile,os,sys,re,gzip
from io import StringIO

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'

class download_tools():
	def Downloader(self,url,dest,description,heading):
		dp = xbmcgui.DialogProgress()
		dp.create(heading,description,'')
		dp.update(0)
		urllib2.urlretrieve(url,dest,lambda nb, bs, fs, url=url: self._pbhook(nb,bs,fs,dp))
		
	def _pbhook(self,numblocks, blocksize, filesize,dp=None):
		try:
			percent = (int(numblocks)*int(blocksize)*100)/int(filesize))
			dp.update(percent)
		except:
			percent = 100
			dp.update(percent)
		if dp.iscanceled(): 
			dp.close()
	
	def extract(self,file_tar,destination):
		dp = xbmcgui.DialogProgress()
		dp.create(translate(30000),translate(30023))
		tar = tarfile.open(file_tar)
		tar.extractall(destination)
		dp.update(100)
		tar.close()
		dp.close()
		
	def remove(self,file_):
		dp = xbmcgui.DialogProgress()
		dp.create(translate(30000),translate(30024))
		os.remove(file_)
		dp.update(100)
		dp.close()

def get_page_source(url):
	req = urllib2.urlopen(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	# if response.info().get('Content-Encoding') == 'gzip':
	if req.info().get('Content-Encoding') == 'gzip':
		# buf = StringIO(response.read())
		buf = StringIO(req.read())
		f = gzip.GzipFile(fileobj=buf)
		link = f.read()
	else:
		link = response.read()
		# link = req.read()
	response.close()
	# req.close()
	return link
	
def makeRequest(url, headers=None):
	try:
		if not headers:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
		req = urllib2.Request(url,None,headers)
		# req = urllib2.openurl(url,None,headers)
		response = urllib2.urlopen(req)
		data = response.read()
		# data = req.read()
		response.close()
		# req.close()
		return data
	except:
		sys.exit(0)
		
def url_isup(url, headers=None):
	try:
		if not headers:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
		req = urllib2.Request(url,None,headers)
		# req = urllib2.urlopen(url,None,headers)
		response = urllib2.urlopen(req)
		data = response.read()
		# data = req.read()
		response.close()
		# req.close()
		return True
	except: return False
		
def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'�','&170;':'�','&#233;':'�','&#231;':'�','&#243;':'�','&#226;':'�','&ntilde;':'�','&#225;':'�','&#237;':'�','&#245;':'�','&#201;':'�','&#250;':'�','&amp;':'&','&#193;':'�','&#195;':'�','&#202;':'�','&#199;':'�','&#211;':'�','&#213;':'�','&#212;':'�','&#218;':'�'}
      regex = re.compile("|".join(map(re.escape, list(command.keys()))))
      return regex.sub(lambda mo: command[mo.group(0)], text)