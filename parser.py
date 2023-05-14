from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import requests
import random
import time 
import os

def wait_by_name(driver, element_name):
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, element_name)))

def wait_by_id(driver, element_id):
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, element_id)))

def wait_by_tag(driver, element_tag_name):
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, element_tag_name)))

def wait_by_class(driver, element_class_name):
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, element_class_name)))

def wait_by_title(driver, title):
	WebDriverWait(driver, 5).until(EC.title_is(title))

class Parser:
	def __init__(self, web_source, username, password):
		self.url = web_source
		self.driver = webdriver.Chrome("./config/chromedriver.exe")
		self.username = username
		self.password = password
	
	def ping(self):
		self.driver.get("https://www.google.com")
		try:
			wait_by_title(self.driver, "Google")
			print("Online")
		except:
			print("Offline")
		
	def login(self):
		self.driver.get(self.url)
		
		try:
			wait_by_name(self.driver, "username")
		except:
			print("Cannot Access The Web Resource")
			return False
		else:
			username = self.driver.find_element(By.XPATH, "//input[@name='username']") 
			username.send_keys(self.username)
			password = self.driver.find_element(By.XPATH, "//input[@name='password']") 
			password.send_keys(self.password)
			password.submit()

			print("Loggin In...")
			try:
				wait_by_title(self.driver, "Instagram")
			except:
				print("There Is An Error While Logging In")
				return False
			else:
				time.sleep(5)
				print("Logged In")
				return True
	
	def reload(self):
		self.driver.quit()
		self.driver = webdriver.Chrome("./config/chromedriver.exe")
		print("Driver Reloaded")
	
	def parse_followers(self, target, file_name, depth = 1):
		self.driver.get(self.url + "/" + target + "/followers")
		try:
			wait_by_class(self.driver, "_aano")
		except:
			print("Followers Module Not Loaded")
			return
			
		try:
			followers_window = self.driver.find_element(By.XPATH, '//div[@class="_aano"]')
		except:
			print("Cannot Access Followers Module")
			return

		with open(file_name, "w") as file:
			cnt = 1
			break_point = 0
			while break_point < 10 and depth > 0:
				try:
					el = self.driver.find_element(By.XPATH, f'//div[@class="_aano"]/div[1]/div/div[{cnt}]/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a')
					profile_link = el.get_attribute("href")
					file.write(profile_link + "\n")
					cnt += 1
					break_point = 0
					print("Got", profile_link)
				except:
					break_point += 1
					depth -= 1
					self.driver.execute_script('document.getElementsByClassName("_aano")[0].scrollBy(0, 1000)')
					time.sleep(2)
		print("Parsing Stopped")
	
	def parse_account(self, target, analyzer, alternative_analyzer):
		self.driver.get(target)
		ret_age = -1
		ret_gender = "N"
		try:
			wait_by_tag(self.driver, "header")
		except:
			print("Not Accessed " + target)
		else:
			print("Accessed " + target)
			page = BS(self.driver.page_source, features="html.parser")
			url = page.find("header").find("img")["src"]
			resp = requests.get(url)
			print("Image Being Accessed")
			if resp.status_code == 200:
				letters = [chr(i) for i in range(65, 91)]
				file_name = "./temp/" + "".join([random.choice(letters) for i in range(20)]) + ".jpg"
				with open(file_name, "wb") as f:
					f.write(resp.content)
				print("Image Fetched")
				try:
					ret_age, ret_gender = analyzer(file_name)
					if os.path.exists(file_name):
						os.remove(file_name)
				except:
					print("Error While Processing Image")
			else:
				print("Image Not Fetched")
		if ret_gender == "N" or random.random() < 0.3:
			try:
				print("Name Being Accessed")
				name = page.find("div", {"class": "_aa_c"}).span.string
				name.replace("_", " ")
				name.replace("-", " ")
				name.replace(",", " ")
				name.replace(":", " ")
				name = min(name.split(), key=lambda x: len(x))
				if (gender := alternative_analyzer(name)) != "N":
					ret_gender = gender
				print("Name Fetched")
			except:
				print("Name Not Fetched")
		return ret_age, ret_gender
	
	def parse_accounts(self, file_in, file_out, analyzer, alternative_analyzer):
		with open(file_in, "r") as data:
			with open(file_out, "w", encoding="utf-8") as out:
				for target in data:
					out.write(target[:-1] + " | " + " ".join(list(map(str, self.parse_account(target[:-1], analyzer, alternative_analyzer)))) + "\n")
					#time.sleep(2)
		print("Fetching Stopped")
	
	def shut_down(self, sec):
		print(f"Shut Down In {sec} Seconds")
		time.sleep(sec)
		self.driver.quit()
		print("Parser Shut Down")

