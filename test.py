from selenium import webdriver

driver = webdriver.PhantomJS()
# print("Select Category:")
# print("")
# print("1. Popular")
# print("2. Xianxia")
# print("3. Xuanhuan")
# print("4. Fantasy")
# print("5. Sci-Fi")
# print("6. Modern")
# print("7. Other")


# x = input("Input")
# if x == 1:
driver.get("https://www.webnovel.com/popular")
# if x == 2:
	# driver.get("https://www.webnovel.com/popular/xianxia")
# if x == 3:
	# driver.get("https://www.webnovel.com/popular/xuanhuan")
# if x == 4:
	# driver.get("https://www.webnovel.com/popular/fantasy")
# if x == 5:
	# driver.get("https://www.webnovel.com/popular/sci-fi")
# if x == 6:
	# driver.get("https://www.webnovel.com/popular/modern")
# if x == 7:
	# driver.get("https://www.webnovel.com/popular/other")
	
elem = driver.find_elements_by_css_selector(".c_strong")
result = [{"link": category.get_attribute("href"), "text": category.get_attribute("data-bid")}
for category in elem]

result = result[::3]
	
print(new_result)

for i in new_result:
	print(i["text"])