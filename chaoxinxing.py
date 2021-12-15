# -*- coding = utf -8 -*-
# @Time : 2021/11/21 20:15
# @Author : hair
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import json
from selenium.webdriver.chrome.options import Options

def login(account,password):
	while 1:
		try:
			bro.find_element_by_class_name("ipt-tel").send_keys(account)
			bro.find_element_by_class_name("ipt-pwd").send_keys(password)
			bro.find_element_by_class_name("btn-big-blue").click()
			break
		except:
			pass

def jiandazuoye():
	WebDriverWait(bro, 10, 1).until(lambda bro: bro.find_element_by_class_name("zy"))
	bro.find_element_by_class_name("zy").click()
	while 1:
		try:
			WebDriverWait(bro,10,1).until(lambda bro:bro.find_element_by_id("frame_content-zy"))
			bro.switch_to.frame("frame_content-zy")
			elems = bro.find_elements_by_css_selector(".bottomList>ul>li[data]")
			links = [e.get_attribute("data") for e in elems[2:]]

			ti = {}

			n = 1
			for link in links:
				print(f"第{n}次爬取简答题")
				n += 1
				bro.get(link)
				es_ti = bro.find_elements_by_css_selector(".questionLi")

				for es in es_ti:
					timu = es.find_element_by_css_selector(".mark_name").text
					try:
						daan = es.find_element_by_css_selector(".colorGreen").text

						ti[timu] = daan
					except:
						ti[timu] = '无答案'

			with open('gaunlidt.text','w',encoding="utf-8") as f:
				# di_json = json.dumps(ti,indent=1,ensure_ascii=False).replace("\\n","\n")
				# di_json = json.dumps(ti, indent=1, ensure_ascii=False)
				# print(type(di_json))
				# print(di_json)
				for i,k in ti.items():
					f.write('******'+i[1:])
					f.write("\n")
					f.write(k)
					f.write("\n\n")

			break
		except	Exception as e:
			print(e)

def xuanze(url):
	bro.get(url)

	WebDriverWait(bro, 10, 0.5).until(lambda bro: bro.find_element_by_css_selector("#frame_content-zj"))
	bro.switch_to.frame("frame_content-zj")
	elems = bro.find_elements_by_css_selector(".chapter_item")

	xzlist = []
	for index,e in enumerate(elems):
		if e.get_attribute("title") == "测验":
			e.click()
			time.sleep(0.5)

	handles = bro.window_handles
	for ind,h in enumerate(handles):
		if ind != 0:
			print(f"第{ind}次爬取")
			bro.switch_to.window(handles[ind])
			bro.switch_to.frame(0)
			bro.switch_to.frame(0)
			bro.switch_to.frame(0)
			WebDriverWait(bro, 10, 0.5).until(lambda bro: bro.find_elements_by_css_selector(".TiMu"))

			elems1 = bro.find_elements_by_css_selector(".TiMu")

			for e in elems1:
				xzlist.append(e.text)

	with open('gaunlixz.txt', 'w', encoding="utf-8") as f:
		import re
		txt = ''.join(xzlist)
		txt = txt.replace("、\n", "、 ")
		txt = txt.replace("\n\n", "\n")
		txt = re.sub("[0-9]{1,3}\n", "_", txt)
		txt = re.sub("我的答案：[A-Z]{1,10}", "\n", txt)
		f.write(txt)

if __name__ == '__main__':

	options = Options()
	EDGE = {
		# headless
		"ms:edgeOptions": {
			'extensions': [],
			'args': [
				'--headless',
			]}
	}
	bro = webdriver.Edge(executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe",\
						 capabilities=EDGE)

	bro.get("https://mooc2-ans.chaoxing.com/mycourse/stu?courseid=219765415&clazzid=44508332&cpi=159676482&enc=7dd5c7d98849e9bbe19ab2ff75681b6a&t=1631326591322&pageHeader=1")

	import time
	login('your account','password')
	jiandazuoye()
	xuanze("https://mooc2-ans.chaoxing.com/mycourse/stu?courseid=219765415&clazzid=44508332&cpi=159676482&enc=7dd5c7d98849e9bbe19ab2ff75681b6a&t=1631326591322&pageHeader=1")

	bro.quit()