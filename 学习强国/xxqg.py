# -*- coding = utf -8 -*-
# @Time : 2021/5/24 19:40
# @Author : hair
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys  # 键盘对象
import time
import datetime

# 记录附加点击次数
add = 0
# 登陆
def login(bro, jifen):
	bro.find_element_by_class_name('login-icon').click()
	handles = bro.window_handles
	bro.close()
	bro.switch_to.window(handles[-1])
	flag = 1
	while 1:
		print('快扫码登录')
		time.sleep(4)
		while flag:
			try:
				bro.find_element_by_xpath('//a[@class="icon search-icon"]')
				flag = 0
			except:
				print('等待登陆')
				time.sleep(2)
		print('login successfully')
		jifen += 1
		print(f'目前积分:{jifen}')
		break
	return bro, jifen


def wenzhang(bro, jifen):
	print('\n' + '点击文章' * 10 + '\n')
	flag = 1
	while flag:
		try:
			print('等待加载')
			time.sleep(3)
			shiping = bro.find_element_by_id("f657")
			xinwen = bro.find_element_by_id("4d3a")
			zxb = bro.find_element_by_id("b0b8")
			
			find_bt0 = shiping.find_elements_by_class_name('grid-cell')
			find_bt1 = xinwen.find_elements_by_class_name('grid-cell')
			find_bt2 = zxb.find_elements_by_class_name('grid-cell')
			all_bt = [find_bt1, find_bt0, find_bt2]
			# 三个专题
			global add
			for index, bt in enumerate(all_bt):
				print('找专题中')
				# 每个专题下有8个标题
				for b in bt:
					num = len(b.find_elements_by_class_name('grid-cell'))
					if num == 8:
						biaoti = b.find_elements_by_class_name('grid-cell')
						print('已找到')
						break
					else:
						continue
					
				# 点击每个专题下的文章标题
				for n, i in enumerate(biaoti):
					i.click()
					time.sleep(2)
					handles = bro.window_handles
					bro.switch_to.window(handles[-1])
					
					nn = 0  # 尝试几次
					try:
						nn + 1
						# 文章的日期
						t = bro.find_element_by_class_name('render-detail-time').text
						# print(type(t),t)
						if today == t or index == 2:
							if jifen != 7 and index != 2:
								print(f'正在阅读第{n + 1}篇,一目1000行,马上好')
								# 滚动页面
								bro.execute_script("window.scrollTo(0,300)")
								time.sleep(2)
								bro.execute_script('window.scrollTo(0,300)')
								time.sleep(1)
								bro.close()
								handles = bro.window_handles
								bro.switch_to.window(handles[0])
								jifen += 1
								print(f'完成，目前积分:{jifen}')
								continue
							elif jifen == 7 or index == 2:
								if jifen < 7:
									add += 1
									print(f'点最后一个专题文章，无论时间，可能不会加分！')
									# 滚动页面
									bro.execute_script("window.scrollTo(0,300)")
									time.sleep(2)
									bro.execute_script('window.scrollTo(0,300)')
									time.sleep(1)
									bro.close()
									handles = bro.window_handles
									bro.switch_to.window(handles[0])
									jifen += 1
									continue
								jifen -= add
								print(f'减掉不确定积分，目前积分:{jifen}')
								print(f'阅读6分钟')
								# 滚动页面
								bro.execute_script('window.scrollTo(0,300)')
								time.sleep(2)
								bro.execute_script('window.scrollTo(0,300)')
								time.sleep(1)
								time.sleep(358)
								bro.close()
								handles = bro.window_handles
								bro.switch_to.window(handles[0])
								jifen += 6
								print(f'完成，目前积分:{jifen}')
							
						else:
							print('不是今天的，下个专题')
							bro.close()
							handles = bro.window_handles
							bro.switch_to.window(handles[0])
							break
					except Exception as e:
						if nn == 16:
							continue
						print(e)
				if jifen == 13 or index == 2:
					break
			break
		except Exception as e:
			print(e)
	return bro, jifen

def search_sth(bro, jifen):
	print('\n' + '找视频点' + '\n')
	js = "window.open('https://static.xuexi.cn/search/online/index.html?t=1622020818706')"
	bro.execute_script(js)
	bro.close()
	handles = bro.window_handles
	bro.switch_to.window(handles[0])
	bro.find_element_by_xpath('//*[@class = "search"]/input').send_keys('每日')
	bro.find_element_by_xpath('//*[@type = "submit"]').click()
	while 1:
		try:
			art = bro.find_elements_by_xpath('//*[@class = "list"]/div[@class = "c-card"]')
			if len(art) == 14:
				print('加载成功')
				break
			else:
				print('等待加载')
				time.sleep(2)
		except Exception as e:
			print(e)
	
	# 每日视频
	li_v = ['影视经典', '每日一曲']
	for n, i in enumerate(art):
		for v in li_v:
			if v in i.find_element_by_class_name('title').text:
				i.click()
				time.sleep(2)
				handles = bro.window_handles
				bro.switch_to.window(handles[-1])
				while 1:
					try:
						bro.find_element_by_class_name('search-icon')
						# 滚动页面
						bro.execute_script('window.scrollTo(0,300)')
						time.sleep(2)
						bro.execute_script('window.scrollTo(0,300)')
						break
					except:
						pass
				bro.close()
				handles = bro.window_handles
				bro.switch_to.window(handles[0])
				jifen += 1
				print(f'目前积分:{jifen}')
				break
	
	print('\n' + '找俩视频点' + '\n')
	js = "window.open('https://static.xuexi.cn/search/online/index.html?t=1622020818706')"
	bro.execute_script(js)
	bro.close()
	handles = bro.window_handles
	bro.switch_to.window(handles[0])
	bro.find_element_by_xpath('//*[@class = "search"]/input').send_keys('视频')
	bro.find_element_by_xpath('//*[@type = "submit"]').click()
	time.sleep(2)
	while 1:
		try:
			art = bro.find_elements_by_xpath('//*[@class = "list"]/div[@class = "c-card"]')
			if len(art) == 15:
				print('加载成功')
				for n, i in enumerate(art[:2]):
					i.click()
					time.sleep(2)
					handles = bro.window_handles
					bro.switch_to.window(handles[-1])
					while 1:
						try:
							time.sleep(2)
							# 滚动页面
							bro.execute_script('window.scrollTo(0,500)')
							time.sleep(2)
							bro.find_element_by_class_name('video-article-time')
							jifen += 1
							print(f'目前积分:{jifen}')
							bro.close()
							handles = bro.window_handles
							bro.switch_to.window(handles[0])
							break
						except:
							bro.close()
							handles = bro.window_handles
							bro.switch_to.window(handles[0])
							print('不是视频不加分')
							break
				
				break
			else:
				print('等待加载')
				time.sleep(2)
		except Exception as e:
			print(e)
	return bro, jifen


def dubao(bro, jifen):
	print('听每日读报6分钟')
	js = "window.open('https://www.xuexi.cn/')"
	bro.execute_script(js)
	bro.close()
	handles = bro.window_handles
	bro.switch_to.window(handles[0])
	try:
		time.sleep(1)
		dubao = bro.find_element_by_id('83d3')
		dubao_tu = dubao.find_element_by_class_name('lazyload-wrapper')
		dubao_tu.click()
		time.sleep(2)
		handles = bro.window_handles
		bro.switch_to.window(handles[-1])
		bro.execute_script('window.scrollTo(0,600)')
		time.sleep(361)
		jifen += 6
		print(f'已拿{jifen}分')
		bro.close()
		handles = bro.window_handles
		bro.switch_to.window(handles[0])
		print('*' * 100 + '\n')
	except:
		time.sleep(2)
	return bro, jifen

def bufen(bro, jifen):
	print('\n' + '找点文章补分' + '\n')
	js = "window.open('https://static.xuexi.cn/search/online/index.html?t=1622020818706')"
	bro.execute_script(js)
	bro.close()
	handles = bro.window_handles
	bro.switch_to.window(handles[0])
	# 取月份
	mon = time.localtime().tm_mon
	day = time.localtime().tm_mday
	md = ''
	for dex, i in enumerate(map(str, [mon, day])):
		md += i
		if dex == 0: md += '-'
	bro.find_element_by_xpath('//*[@class = "search"]/input').send_keys(f'{md}')
	bro.find_element_by_xpath('//*[@type = "submit"]').click()
	while 1:
		try:
			art = bro.find_elements_by_xpath('//*[@class = "list"]/div[@class = "c-card"]')
			if len(art) == 14:
				print('加载成功')
				break
			else:
				print('等待加载')
				time.sleep(2)
		except Exception as e:
			print(e)
	
	for n, i in enumerate(art[:4]):
		i.click()
		time.sleep(2)
		handles = bro.window_handles
		bro.switch_to.window(handles[-1])
		while 1:
			try:
				bro.find_element_by_class_name('search-icon')
				# 滚动页面
				bro.execute_script('window.scrollTo(0,300)')
				time.sleep(2)
				bro.execute_script('window.scrollTo(0,300)')
				break
			except:
				pass
		bro.close()
		handles = bro.window_handles
		bro.switch_to.window(handles[0])
		jifen += 1
		print(f'目前积分:{jifen}')
	return bro,jifen
	
if __name__ == '__main__':
	jifen = 0
	today = datetime.date.today()
	today = str(today)
	
	start = time.time()
	try:
		bro = webdriver.Chrome(executable_path='./chromedriver')
		url = f'https://www.xuexi.cn/'
		bro.get(url)
		# bro.maximize_window()
		while 1:
			try:
				time.sleep(2)
				bro.find_element_by_xpath('//a[@class="icon login-icon"]')
				break
			except:
				pass
		
		bro, jifen = login(bro, jifen)
		bro, jifen = wenzhang(bro, jifen)
		bro, jifen = search_sth(bro, jifen)
		bro, jifen = dubao(bro, jifen)
		print(f'拿到{jifen}分')
		if jifen < 20:
			print('新文章不够,启动补分')
			bro, jifen = bufen(bro, jifen)
			print('再不够用手点几下吧')
		else:
			print('分够啦')
	except Exception as e:
		print(e)
	
	finally:
		bro.quit()
	

	end = time.time()
	print(f'用时{end - start}秒')
