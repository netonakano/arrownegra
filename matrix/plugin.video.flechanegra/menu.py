  

 <item>
 <item>
<title>[COLOR red][COLOR yellow] [/COLOR]</title>
<link>$doregex[makelist]</link>
<regex>
<name>makelist</name>
<listrepeat><![CDATA[
<fanart></fanart>
<title>[makelist.param1]</title>
<link>plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name=[makelist.param1]&amp;url=$doregex[encodedurl]</link>
<thumbnail></thumbnail>
]]></listrepeat>
<expres>#EXTINF:.*,(.*?)\n.*(http.*m3u8)</expres>
<page>http://br13.xyz:80/get.php?username=alan123&amp;password=alan123&type&amp;type=m3u_plus&amp;output=m3u8</page>
<referer>http://dns.ulttv.xyz</referer>
<x-forward></x-forward>
<buffermode>50</buffermode>
<readfactor>50</readfactor>
<agent>VLC/3.0.0</agent>
</regex>
<regex>
<name>encodedurl</name>
<expres>$pyFunction:urllib.quote_plus('[makelist.param2]')<expres>
<page></page>
</regex>
</item>
  
  
  
  
 <item>
 <item>
<title>[COLOR red][COLOR yellow] [/COLOR]</title>
<link>$doregex[makelist]</link>
<regex>
<name>makelist</name>
<listrepeat><![CDATA[
<fanart></fanart>
<title>[makelist.param1]</title>
<link>plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name=[makelist.param1]&amp;url=$doregex[encodedurl]</link>
<thumbnail></thumbnail>
]]></listrepeat>
<expres>#EXTINF:.*,(.*?)\n.*(http.*ts)</expres>
<page>http://br13.xyz:80/get.php?username=alan123&amp;password=alan123&type&amp;type=m3u_plus&amp;output=m3u8</page>
<referer>http://dns.ulttv.xyz</referer>
<x-forward></x-forward>
<buffermode>50</buffermode>
<readfactor>50</readfactor>
<agent>VLC/3.0.0</agent>
</regex>
<regex>
<name>encodedurl</name>
<expres>$pyFunction:urllib.quote_plus('[makelist.param2]')<expres>
<page></page>
</regex>
</item>
  
    
  <item>
<title>[COLOR red][COLOR yellow] [/COLOR]</title>
<link>$doregex[makelist]</link>
<regex>
<name>makelist</name>
<listrepeat><![CDATA[
<fanart></fanart>
<title>[makelist.param1]</title>
<link>plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=[makelist.param1]&amp;url=$doregex[encodedurl]</link>
<thumbnail></thumbnail>
]]></listrepeat>
<expres>#EXTINF:.*,(.*?)\n.*(http.*ts)</expres>
<page>http://</page>
<referer>https://google.com</referer>
<x-forward></x-forward>
<buffermode>50</buffermode>
<readfactor>50</readfactor>
<agent>VLC/3.0.0</agent>
<agent>Kodi/18.0</agent>
</regex>
<regex>
<name>encodedurl</name>
<expres>$pyFunction:urllib.quote_plus('[makelist.param2]')<expres>
<page></page>
</regex>
</item>

  
    
  <item>
<title>[COLOR red][COLOR yellow] [/COLOR]</title>
<link>$doregex[makelist]</link>
<regex>
<name>makelist</name>
<listrepeat><![CDATA[
<fanart></fanart>
<title>[makelist.param1]</title>
<link>plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=[makelist.param1]&amp;url=$doregex[encodedurl]</link>
<thumbnail></thumbnail>
]]></listrepeat>
<expres>#EXTINF:.*,(.*?)\n.*(http.*m3u8)</expres>
<page>http://</page>
<referer>https://google.com</referer>
<x-forward></x-forward>
<buffermode>50</buffermode>
<readfactor>50</readfactor>
<agent>VLC/3.0.0</agent>
<agent>Kodi/18.0</agent>
</regex>
<regex>
<name>encodedurl</name>
<expres>$pyFunction:urllib.quote_plus('[makelist.param2]')<expres>
<page></page>
</regex>
</item>

  
 