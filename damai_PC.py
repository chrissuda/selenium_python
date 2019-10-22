# cop a concert from 大麦.com at a specific time.
# You need to configure cookie_location (option.add_argument), time, damai_url...
from selenium import webdriver
import time
import schedule
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
option = ChromeOptions()

option.add_argument('--user-data-dir=C:/Users/chris/AppData/Local/Google/Chrome/User Data') #based on your cookie location(Chrome)
# paste your concert url above
damai_url='https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.436a5389MtFkee&id=598066779141&clicktitle=%E6%B1%AA%E8%8B%8F%E6%B3%B72019%E2%80%9C%E9%93%B6%E6%B2%B3%E6%BC%AB%E6%B8%B8%E2%80%9D%E5%B7%A1%E5%9B%9E%E6%BC%94%E5%94%B1%E4%BC%9A%E4%B8%8A%E6%B5%B7%E7%AB%99-%E7%94%9F%E6%97%A5%E7%89%B9%E5%88%AB%E5%9C%BA'
target_time="23:18:59 " #"23:18:59"

option.add_experimental_option('excludeSwitches', ['enable-automation'])
desired_capabilities = DesiredCapabilities.CHROME  
desired_capabilities["pageLoadStrategy"] = "none" #eager
prefs = {"profile.managed_default_content_settings.images": 2} # 1:loading picture 2: forbidden loading message 
option.add_experimental_option("prefs", prefs)
driver=webdriver.Chrome(options=option)

book='div[class=buybtn]' #/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[3]/div[10]/div 
people='span.next-checkbox' #span.next-checkbox  span.next-checkbox > input:nth-child(2)
submit='.submit-wrapper > button:nth-child(1)' #//button[@type="button"][contains(.,"同意以上协议并提交订单")] 
	
def login():
	driver.get(damai_url)
	while driver.current_url!=damai_url:
		time.sleep(0.1)

	while driver.current_url==damai_url:
		print("please_click_login")
		driver.find_element_by_xpath('//span[@data-spm="dlogin"]').click()
		time.sleep(2)

	while driver.current_url!=damai_url:
		print("please login")
		time.sleep(2)

def ticket(book,people,submit):
	driver.refresh()
	start=time.time() # starting timing (only for testing purpose)
	print('Ready')

	element = WebDriverWait(driver, 600,0.01).until(
	EC.element_to_be_clickable((By.CSS_SELECTOR,book)))
	driver.find_element_by_css_selector(book).click()

	element = WebDriverWait(driver, 600,0.01).until(
	EC.element_to_be_clickable((By.CSS_SELECTOR,people)))
	try:
		elementsss = WebDriverWait(driver, 600,0.01).until_not(
		EC.visibility_of_element_located((By.CLASS_NAME,'loading-mask')))
		driver.find_element_by_css_selector(people).click()
	except:
		pass

	elementsss = WebDriverWait(driver, 600,0.01).until_not(
	EC.visibility_of_element_located((By.CLASS_NAME,'loading-mask')))
	#elements = WebDriverWait(driver, 10,0.01).until(
	#EC.element_to_be_clickable((By.XPATH,submit)))
	last=driver.find_element_by_css_selector(submit)
	try:
		last.click()
		print('first_attempt:success')
	except:
		last.click()
		print('second_attempt:success')
	end=time.time()
	print('time:'+str(end-start))
	print('Success')


login()
schedule.every().day.at(target_time).do(ticket,book,people,submit) 
while True:
	schedule.run_pending()
	time.sleep(0.01)

