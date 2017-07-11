from selenium import webdriver
import time

print("Select Category:")
print("")
print("1. Popular")
print("2. Xianxia")
print("3. Xuanhuan")
print("4. Fantasy")
print("5. Sci-Fi")
print("6. Modern")
print("7. Other")

website = None
x = int(input("Input"))
if x == 1:
	website = "https://www.webnovel.com/popular"
elif x == 2:
	website = "https://www.webnovel.com/popular/xianxia"
elif x == 3:
	website = "https://www.webnovel.com/popular/xuanhuan"
elif x == 4:
	website = "https://www.webnovel.com/popular/fantasy"
elif x == 5:
	website = "https://www.webnovel.com/popular/sci-fi"
elif x == 6:
	website = "https://www.webnovel.com/popular/modern"
elif x == 7:
	website = "https://www.webnovel.com/popular/other"
	
print("Getting Data...")
driver = webdriver.PhantomJS()
driver.get(website)

print("Getting Data...")

elem = driver.find_elements_by_css_selector(".c_strong")
result = [{"link": category.get_attribute("href"), "text": category.get_attribute("data-bid")}
for category in elem]
result = result[::3]
	
x = 1
for i in result:
	print(str(x) + ". ", end="")
	print(i["text"])
	x += 1
	
select = int(input("Which Novel do you want to read?"))

website = result[select - 1]["link"]
driver.get(website)
popup = driver.find_element_by_css_selector("a[href='#contentsModal']")
popup.click()
time.sleep(0.5)
chlist_raw = driver.find_elements_by_css_selector(".g_mod_content .g_mod_bd.content-list a" )
chlist = [{"link": category.get_attribute("href"), "text": category.text}
for category in chlist_raw]

amountChapters = len(chlist)

print ("There are currently " + str(amountChapters) + " available")

driver.save_screenshot('screenie.png')