import urllib.request
import os
import re

def url_open(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
	response = urllib.request.urlopen(req)
	return response.read() 
#寻找页面地址
def get_page(url):
	html = url_open(url).decode('utf-8')
	# print(html)
	pattern = r'<span class="current-comment-page">\[(\d{4})\]</span>' #正则表达式获取按钮地址
	page = int(re.findall(pattern,html)[0])
	return page
#获取照片的地址

def find_imgs(page_url):
	pattern = r'<img src="(.*?\.jpg)"'
	html = url_open(page_url).decode('utf-8')
	img_addrs = re.findall(pattern,html)
	return img_addrs
#获取图片的名字并创建指定文件夹并保存
def save_imgs(img_addrs,page_num,folder):
    os.mkdir(str(page_num))
    os.chdir(str(page_num))
    for i in img_addrs:
	    pattern = r'sinaimg.cn/mw600/(.*?).jpg'
	    filename = i.split('/')[-1]
	    image = url_open(i)
	    with open(filename,'wb') as f:
	    	f.write(image)
	    	f.close()
	    fp = open('../index.html', 'a')
	    fp.write('<img src="./'+ str(page_num)+'/'+filename+'">')
	    fp.close()

def download(folder='JianDan',pages=10):
	# os.mkdir(folder)
	os.chdir(folder)
	folder_top = os.getcwd()
	url = 'http://jandan.net/ooxx/'
	page_num = get_page(url)
	# print(page_num)
	for i in range(pages):
		page_num -= i
		page_url = url + 'page-' + str(page_num) + '#comments'
		print(page_url)
		img_addrs = find_imgs(page_url)
		save_imgs(img_addrs,page_num,folder)
		os.chdir(folder_top)

if __name__ == '__main__':
	folder = './'
	pages = 1
	download(str(folder),int(pages))

