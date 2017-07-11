#Page Clean-up
from bs4 import BeautifulSoup

with open("test.html", "r", encoding="utf8") as f:
	soup = BeautifulSoup(f, "html.parser")
	pretext = soup.find("div", {"class":"cha-content"})
	[s.extract() for s in pretext('form')]
	[s.extract() for s in pretext('a')]
	[s.extract() for s in pretext('script')]
	pretext.find('div', id="cha-bts").decompose()
	pretext = str(pretext)
			
file = open("modified" + ".xhtml", "w", encoding = "utf8")

file.write('''
<html xmlns="http://www.w3.org/1999/xhtml"><head/><body>
''')
for line in pretext:
	if "href" not in line:
		file.write(line)	
file.write("</body>")
file.write("</html>")