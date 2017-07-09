from selenium import webdriver

#Get's all available chapters
print("Getting Chapters...")
driver = webdriver.PhantomJS()
driver.get("https://www.webnovel.com/book/7834185605001405")
elem = driver.find_element_by_css_selector("a[href='#contentsModal']")
elem.click()
elem = driver.find_elements_by_css_selector(".g_mod_content .g_mod_bd.content-list a" )
result = [{"link": category.get_attribute("href"), "text": category.text}
for category in elem]

amountChapters = len(result) - 1

print ("There are currently " + str(amountChapters) + " available")
x = input("What Chapter do you want to read?")
container = result[int(x) - 1]
print (container["text"])
