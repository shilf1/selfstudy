#! python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#import action
import time

# PLEASE WRITE YOUR ACCOUNT INFO HERE to use this python script
# === USER INFO ===
USER_ID = ""
USER_PW = ""

# === TICKET INFO to reserve ===
TARGET_DATE = "2018/02/28(수)"
TARGET_TIME = "18:30"

DPT = "수서"
ARV = "대전"

NUM_ADT = "어른 1명"
NUM_CHD = "만 4~12세 0명"
# =================


driver = webdriver.Chrome('C:\\Users\shilf\AppData\Local\Programs\Python\Python36\Scripts\chromedriver.exe')

url_login = 'https://etk.srail.co.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000'
url_reserve = 'https://etk.srail.co.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000'

driver.implicitly_wait(3)

driver.get(url_login)

# 1. LOGIN : set id / pw to login --------------------------

driver.find_element_by_name("srchDvNm").send_keys(USER_ID)
driver.find_element_by_name("hmpgPwdCphd").send_keys(USER_PW)

form = driver.find_element_by_id('login-form')
form.submit()
#form.click()

driver.get(url_reserve)

# 2. search-form  -------------------------------------------

driver.find_element_by_name("dptRsStnCdNm").clear()
driver.find_element_by_name("dptRsStnCdNm").send_keys(DPT)
driver.find_element_by_name("arvRsStnCdNm").clear()
driver.find_element_by_name("arvRsStnCdNm").send_keys(ARV)
driver.find_element_by_xpath("//select[@name='dptDt']/option[text()='"+TARGET_DATE+"']").click() #date
driver.find_element_by_xpath("//select[@name='dptTm']/option[text()='16']").click()  #time
driver.find_element_by_xpath("//select[@name='psgInfoPerPrnb1']/option[text()='"+NUM_ADT+"']").click()  #adult
driver.find_element_by_xpath("//select[@name='psgInfoPerPrnb5']/option[text()='"+NUM_CHD+"']").click()  #child

form = driver.find_element_by_id('search-form')
form.submit()
#form.click()


# 3. search list (result) -----------------------------------

output = len(driver.find_elements_by_xpath("//*[@id='result-form']/fieldset/table/tbody/tr"))
print(output)

found = False # init
count = 0


print("\n\n## Try to find "+TARGET_DATE+" / "+TARGET_TIME+"\n")

while found == False:
	print("Try " +str(count) + " times")
	time.sleep(1)

	for i in range(1, output+1) :

		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="result-form"]/fieldset/table/tbody/tr['+str(i)+']/td[4]/em')))
		try:
			ex_time = driver.find_element_by_xpath("//*[@id='result-form']/fieldset/table/tbody/tr["+str(i)+"]/td[4]/em")
		except NoSuchElementException:
			print ('NoSuchElementException')
			break
		except StaleElementReferenceException:
			print ('StaleElementReferenceException')
			break

		print(ex_time)
		ex_time = ex_time.text
		text = driver.find_element_by_xpath("//*[@id='result-form']/fieldset/table/tbody/tr["+str(i)+"]/td[7]").text
		#print(str(i) + " " + ex_time + "/" + TARGET_TIME + " " + text)

		if (ex_time == TARGET_TIME):
			if ("예약하기" in text):
				print("we found it !!!") # we found it -----------------------------
				found = True;
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="result-form"]/fieldset/table/tbody/tr['+str(i)+']/td[7]/a[1]')))
				link = driver.find_element_by_xpath("//*[@id='result-form']/fieldset/table/tbody/tr["+str(i)+"]/td[7]/a[1]")
				link.click()
				break
	
	if found == True:
		print('\n\n> We Reserved ticket =====================\n')
		user_choice = input('Please click ENTER button to close application')
		if not user_choice:
			print('\n\n> EXIT =====================\n')
			quit()
	
	# there is no ticket, keep finding
	count+=1
	prev_search_form = driver.find_element_by_id('search-form')
	prev_search_form.submit()
	
