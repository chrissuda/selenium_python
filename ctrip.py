#crawl air_ticket data from 携程. It runs three times a day, at 8:00, 14:00, 22:00.
#you can see the data in a .json file and a .svg chart file in the directory of this python file.
from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import schedule
import json
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
from twilio.rest import Client
import logging
# coding=UTF-8
logging.basicConfig(level=logging.INFO,
			filename='ctrip.log',
			filemode='a',
			format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
			datefmt='%a, %d %b %Y %H:%M:%S')

def crawl():
	option = ChromeOptions()
	option.add_argument('--user-data-dir=C:/Users/chris/AppData/Local/Google/Chrome/User Data') #based on location of you cookie
	option.add_experimental_option('excludeSwitches', ['enable-automation'])
	driver=webdriver.Chrome(options=option)

	d1=datetime.datetime.strptime('2019-08-24',"%Y-%m-%d")
	dnow=time.strftime("%Y-%m-%d", time.localtime())
	d2=datetime.datetime.strptime(dnow,"%Y-%m-%d")
	day=d2-d1
	d=day.days
	days1=str(16+d)
	days2=str(14+d)

	depature_city='nyc'
	arrival_city='can'
	depature_date1='2019-11-'+days1 #2019-12-02
	depature_date2='2019-12-'+days2 #2019-12-25
	file_name=depature_date1+'&'+depature_date2+'.svg'
	ticket_dicts,companys,prices=[],[],[]

	url='https://flights.ctrip.com/international/search/round-'+depature_city+'-'+arrival_city\
	+'?depdate='+depature_date1+'_'+depature_date2+'&cabin=y_s&adult=1&child=0&infant=0&directflight='

	try:
		driver.get(url)
		driver.implicitly_wait(10)
		driver.find_element_by_css_selector('.sort-box > span:nth-child(7)').click()
		time.sleep(8)
		for i in range(5):
			driver.execute_script("window.scrollBy(0,1000)")
			time.sleep(0.8)
		time.sleep(1)
		tickets=driver.find_elements_by_xpath("//div[@class='flight-item']")
	except:
		print('failed to crawl')
		print(time.strftime("%a %Y-%m-%d %H:%M", time.localtime()))
		account_sid='AC12d31096ff908c444a1e9baae82b9ee2'
		auth_token='eb33c5300e2b0965d4fda121d75b2b2c'
		client=Client(account_sid,auth_token)
		
		message=client.messages.create(
			from_='+16307964576',
			body='Something wrong with the ctrip crawler',
			to='+19292998697'
			)

	for ticket in tickets[:10]:
		a=ticket.text.split('\n')
		del a[-1]
		del a[-1]
		if '精选' in a[0]:
			del a[0]
		else:
			pass
		if '东方'in a[0]:
			pass
		else:
			if len(a)==9:
				ticket_dict={
								'Company:':a[0],
								'Price:':int(a[-1].rstrip('起').lstrip('¥')),
								'Date:':depature_date1,
								'Depature_time:':a[2],
								'Arrival_time:':a[4],
								'Hours:':a[-2].rstrip('航班详情'),
								'Type:':'Nonstop',
								'Transfer_city:':''						
							}
			else:
				ticket_dict={
								'Company:':a[0],
								'Price:':int(a[-1].rstrip('起').lstrip('¥')),
								'Date:':depature_date2,
								'Depature_time:':a[-9],
								'Arrival_time:':a[-5],
								'Hours:':a[-2].rstrip('航班详情'),
								'Type:':'1 stop',
								'Transfer_city:':a[-6].lstrip('转')														
							}
			ticket_dicts.append(ticket_dict)				
			companys.append(ticket_dict['Company:'])
			prices.append(ticket_dict['Price:'])
	driver.quit()
	
	my_style=LS('#333366',base_style=LCS)
	chart=pygal.Bar(style=my_style,x_label_rotation=45,show_legend=False)
	chart.title=time.strftime("%a %Y-%m-%d", time.localtime())+':Ticket_Price'
	chart.x_labels=companys
	chart.add('',prices)
	chart.render_to_file(file_name)
		
	f=open('tickets.json',mode='a',encoding='utf-8') #'a':追加模式 'w':覆盖模式
	f.write('\n')
	f.write('\n')
	f.write(time.strftime("%a %Y-%m-%d %H:%M", time.localtime()))
	f.write('\n')
	for line in ticket_dicts:
		for k, v in line.items():
			f.write(k+':')
			f.write(str(v))
			f.write(' ')
		f.write('\n')
		f.write('\n')
	print('Success...')
	print(time.strftime("%a %Y-%m-%d %H:%M", time.localtime()))
	
schedule.every().day.at('8:00').do(crawl)
schedule.every().day.at('14:00').do(crawl)
schedule.every().day.at('20:00').do(crawl)
while True:
	schedule.run_pending()
	time.sleep(5)
	logging.info('working ....')
