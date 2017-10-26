#encoding: utf-8
from pprint import pprint
from urllib2 import urlopen
import re
import json

vid='u_tORtmKIjE' # bards song (bez koment.)
vid='J56VVtlZCGE' # Fee Ra Huri

if 0:
	open('data.txt','w').write(urlopen('https://www.youtube.com/watch?v='+vid).read())
	exit()

data = open('data.txt','r').read()
config = re.findall('ytplayer.config = (.+?)</script>',data)
pairs = re.findall('"([^"]*)":"([^"]*)"',config[0])
pprint(sorted(pairs)) # keywords, ad_slots, ad_preroll, author, view_count, title, avg_rating, midroll_freqcap, midroll_prefetch_size, length_seconds

## from bs4 import BeautifulSoup
## soup = BeautifulSoup(data,'html.parser')
## print(soup.title.string)
## for x in soup.find_all('yt-view-count-renderer'):
	## print(x)



"""
      <meta itemprop="isFamilyFriendly" content="True">
      <meta itemprop="regionsAllowed" content="AD,AE,AF,AG,AI,AL,AM,AO,AQ,AR,AS,AT,AU,AW,AX,AZ,BA,BB,BD,BE,BF,BG,BH,BI,BJ,BL,BM,BN,BO,BQ,BR,BS,BT,BV,BW,BY,BZ,CA,CC,CD,CF,CG,CH,CI,CK,CL,CM,CN,CO,CR,CU,CV,CW,CX,CY,CZ,DE,DJ,DK,DM,DO,DZ,EC,EE,EG,EH,ER,ES,ET,FI,FJ,FK,FM,FO,FR,GA,GB,GD,GE,GF,GG,GH,GI,GL,GM,GN,GP,GQ,GR,GS,GT,GU,GW,GY,HK,HM,HN,HR,HT,HU,ID,IE,IL,IM,IN,IO,IQ,IR,IS,IT,JE,JM,JO,JP,KE,KG,KH,KI,KM,KN,KP,KR,KW,KY,KZ,LA,LB,LC,LI,LK,LR,LS,LT,LU,LV,LY,MA,MC,MD,ME,MF,MG,MH,MK,ML,MM,MN,MO,MP,MQ,MR,MS,MT,MU,MV,MW,MX,MY,MZ,NA,NC,NE,NF,NG,NI,NL,NO,NP,NR,NU,NZ,OM,PA,PE,PF,PG,PH,PK,PL,PM,PN,PR,PS,PT,PW,PY,QA,RE,RO,RS,RU,RW,SA,SB,SC,SD,SE,SG,SH,SI,SJ,SK,SL,SM,SN,SO,SR,SS,ST,SV,SX,SY,SZ,TC,TD,TF,TG,TH,TJ,TK,TL,TM,TN,TO,TR,TT,TV,TW,TZ,UA,UG,UM,US,UY,UZ,VA,VC,VE,VG,VI,VN,VU,WF,WS,YE,YT,ZA,ZM,ZW">
      <meta itemprop="interactionCount" content="15186135">
      <meta itemprop="datePublished" content="2006-06-30">
      <meta itemprop="genre" content="Music">
      

  <span class="like-button-renderer " data-button-toggle-group="optional" >
    <span class="yt-uix-clickcard">
      <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip" type="button" onclick=";return false;" aria-label="ten film podoba się mnie i jeszcze 101 047 innym osobom" title="To mi się podoba" data-force-position="true" data-position="bottomright" data-orientation="vertical"><span class="yt-uix-button-content">101 047</span></button>
          <div class="signin-clickcard yt-uix-clickcard-content">

 <span class="like-button-renderer " data-button-toggle-group="optional" >
    <span class="yt-uix-clickcard">
      <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip" type="button" onclick=";return false;" title="To mi siÄ podoba" aria-label="ten film podoba siÄ mnie i jeszcze 128Â 818 innym osobom" data-force-position="true" data-orientation="vertical" data-position="bottomright"><span class="yt-uix-button-content">128Â 818</span></button>
          <div class="signin-clickcard yt-uix-clickcard-content">

    <span class="yt-uix-clickcard">
      <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip" type="button" onclick=";return false;" title="To mi siÄ nie podoba" aria-label="ten film nie podoba siÄ mnie i jeszcze 1Â 792 innym osobom" data-force-position="true" data-orientation="vertical" data-position="bottomright"><span class="yt-uix-button-content">1Â 792</span></button>
          <div class="signin-clickcard yt-uix-clickcard-content">

class="yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count" title="3,4 tys." aria-label="3,4 tys." tabindex="0">3,4 tys.</span>  <span class="subscription-preferences-overlay-container">

"""