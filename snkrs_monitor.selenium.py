# crawl "snkrs pass" data from nike. It will notify you by message as long as it detects "snkrs pass" from nike.com
#But there is a delay between "pass" and message. Range:[0,50s]

from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#import schedule
from twilio.rest import Client
import logging
snkrs=[]
phone_receiver='+19292998697'
phone_sender='+16307964576'
frequency=50  #how often does the program run 

logging.basicConfig(level=logging.INFO,
			filename='snkr.log',
			filemode='w',
			format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
			datefmt='%a, %d %b %Y %H:%M:%S')

def monitor():
	option = ChromeOptions()
	option.add_argument('--user-data-dir=C:/Users/chris/AppData/Local/Google/Chrome/User Data') #based on location of you cookie
	#option.add_argument('--headless')

	option.add_experimental_option('excludeSwitches', ['enable-automation'])
	browser=webdriver.Chrome(options=option)
	browser.get('https://www.nike.com/launch/')
	browser.implicitly_wait(5)
	browser.find_element_by_css_selector("li.nav-items:nth-child(2) > a:nth-child(1)").click()
	browser.implicitly_wait(5)
	time.sleep(1)
	browser.find_element_by_css_selector("li.nav-items:nth-child(3) > a:nth-child(1)").click()
	browser.implicitly_wait(5)
	time.sleep(1)
	browser.find_element_by_css_selector("li.nav-items:nth-child(1) > a:nth-child(1)").click()
	browser.implicitly_wait(5)
	
	global snkrs
	for i in range(2):
		time.sleep(2)
		try:
			shoes=browser.find_elements_by_xpath("//a[contains(@aria-label,'Pass')]")
			print(2)
			snkrs=list(set(snkrs))
			print(3)
			for shoe in shoes:
				Pass=shoe.get_attribute('aria-label')
				print(Pass)
				print(4)
				if Pass in snkrs:
					print('have already detected')
					pass
				else:
					print(Pass)
					account_sid='AC12d31096ff908c444a1e9baae82b9ee2'
					auth_token='eb33c5300e2b0965d4fda121d75b2b2c'
					client=Client(account_sid,auth_token)
					
					message=client.messages.create(
						from_=phone_sender,
						body=Pass,
						to=phone_receiver
						)

					snkrs.append(Pass)					
		except:
			print("can't find the Snkrs Pass")
		browser.refresh()
	browser.quit()
	print(time.strftime("%m.%d-%H:%M:%S", time.localtime()))
	

while True:
	monitor()
	logging.info('working')
	time.sleep(frequency)
