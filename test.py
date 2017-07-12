from selenium import webdriver
import urllib.request

driver = webdriver.PhantomJS()
driver.get("https://www.webnovel.com/book/7834185605001405")
elem = driver.find_elements_by_css_selector(".mb5.ell")
meta = [test.text for test in elem]
info = ""
for y in enumerate(meta):
	if y.startswith("Author: "):
		info = y[len("Author: "):] + ", "
	if y.startswith("Translator: "):
		info += y[len("Translator: "):]
print(info)
driver.close()