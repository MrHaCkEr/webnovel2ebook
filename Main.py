from selenium import webdriver
import getify
import time
import urllib.request

print("Select Category:")
print("")
print("1. Popular | Top 30")
print("2. Xianxia")
print("3. Xuanhuan")
print("4. Fantasy")
print("5. Sci-Fi")
print("6. Modern")
print("7. Other")
print("8. New Arrivals | Top 30")
print("9. More then 200 Chapters")

website = None
x = int(input("Select a category (Enter Number): "))
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

	
#Initializes webdriver
print("Getting Data...")
driver = webdriver.PhantomJS("phantomjs.exe")
driver.get(website)

# Collects Title and link of the Book
elem = driver.find_elements_by_css_selector(".c_strong")
result = [{"link": category.get_attribute("href"), "text": category.get_attribute("data-bid")}
for category in elem]
result = result[::3]
	
# Sorts and makes the data look kinda pretty
g = 1
for i in result:
	print(str(g) + ". ", end="")
	print(i["text"])
	g += 1
	
#Gets chapter Names and links
select = int(input("Which Novel do you want to read?: "))
website = result[select - 1]["link"]
print("Getting Chapter names ,links, cover and metadata...")
driver.get(website)
img = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/i/img')
src = img.get_attribute("src")
urllib.request.urlretrieve(src, "cover.jpg")

rawMeta = driver.find_elements_by_css_selector(".mb5.ell")
meta = [test.text for test in rawMeta]
for x, y in enumerate(meta):
	if y.startswith("Author: "):
		info = y[len("Author: "):] + ", "
	if y.startswith("Translator: "):
		info += y[len("Translator: "):]

popup = driver.find_element_by_css_selector("a[href='#contentsModal']")
popup.click()
time.sleep(1)
chlistRaw = driver.find_elements_by_css_selector(".g_mod_content .g_mod_bd.content-list a" )
chlist = [{"link": category.get_attribute("href"), "text": category.text}
for category in chlistRaw]
driver.quit()

print ("There are currently " + str(len(chlist)) + " available")
startingChapter = int(input("What's the starting Chapter?: "))
endingChapter = int(input("What's the ending Chapter?: "))

chlistSelection = chlist[startingChapter - 1 : endingChapter]

file_list = []
for q in range(len(chlistSelection)):
	getify.download(chlistSelection[q]["link"], str(q))
	getify.clean(str(q))
	file_list.append(str(q) + "m" + ".xhtml")
	getify.update_progress(q/len(chlistSelection))
	
getify.generate(file_list, result[select - 1]["text"], info, chlistSelection, str(startingChapter), str(endingChapter))