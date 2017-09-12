# coding: utf-8
import requests
import urllib
import sys
import os
import time
import requests 
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import random
from multiprocessing.pool import ThreadPool 
import json
from urllib import quote
from urllib import unquote


agent_pool = [
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'},
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)'},
    {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)'},
    {'User-Agent':'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0'},
    {'User-Agent':'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5'},
    {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'},
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'}
]


def download_pic(infor_dict): 
	img_name=infor_dict['name']
	try:
		status_code=requests.get(infor_dict["url"],headers=agent_pool[0],timeout=20).status_code
		if status_code==200:

			pic = requests.get(infor_dict["url"],headers=agent_pool[0],timeout=20)  
			fp = open(img_name,'wb')
			print img_name
			fp.write(pic.content)
			fp.close()
		else:
			print err
			fp_tmp = open(img_name,'w')
			fp_tmp.close()
			return 
	except Exception as err:
		print "<<",img_name,"----->","err",">>" 
		fp_tmp2 = open(img_name,'w')
		fp_tmp2.close()
		return 




def start_download(star_name):
	encode_name=quote(star_name)

	if not os.path.exists(star_name):
		os.mkdir(star_name)

	all_url_list=[]
	start_urls=["https://m.baidu.com/sf/vsearch/image/search/wisejsonala?tn=wisejsonala&ie=utf8&cur=result&fromsf=1&word=%s&pn=%d&rn=50&gsm="%(encode_name,50*i) for i in range(100) ]

	#print start_urls
	for x,url in enumerate( start_urls ):
		result= requests.get(url,headers=agent_pool[0],timeout=20).text
		images=json.loads(result)['data']

		if( len(images) ==0 ):

			break

		for y,img in enumerate(images):
			if(img['thumbnail_url']==None):
				continue

			real_img_url=img['thumbnail_url']

			print real_img_url
			if( real_img_url.find("png")>0 ):
				all_url_list.append( {"name":os.path.join(star_name,"%d_%d.png"%(x,y) ),"url":img['thumbnail_url'] } )
			elif( real_img_url.find("jpg")>0 ):
				all_url_list.append( {"name":os.path.join(star_name,"%d_%d.jpg"%(x,y) ),"url":img['thumbnail_url'] } )
			elif( real_img_url.find("jpeg")>0 ):
				all_url_list.append( {"name":os.path.join(star_name,"%d_%d.jpeg"%(x,y) ),"url":img['thumbnail_url'] } )
			elif( real_img_url.find("bmp")>0 ):
				all_url_list.append( {"name":os.path.join(star_name,"%d_%d.bmp"%(x,y) ),"url":img['thumbnail_url'] } )
			else:
				all_url_list.append( {"name":os.path.join(star_name,"%d_%d"%(x,y) ),"url":img['thumbnail_url'] } )

		print "collect url %d sucessful"%len(all_url_list)	
		time.sleep(0.2)

	pool=ThreadPool(200)
	pool.map( download_pic,all_url_list)
	pool.close()
	pool.join()



#start_download("迪丽热巴")
