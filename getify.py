from bs4 import BeautifulSoup
import urllib.request
import shutil
import os.path
import sys
import zipfile
import time

#Downloads Chapters
def download(link, file_name):
	url = urllib.request.Request(
		link,
		data=None, 
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)

	with urllib.request.urlopen(url) as response, open(file_name + ".xhtml", 'wb') as out_file:
		shutil.copyfileobj(response, out_file)

#Page Clean-up
def clean(filename):
	with open(filename + ".xhtml", "r", encoding="utf8") as f:
		soup = BeautifulSoup(f, "html.parser")
		pretext = soup.find("div", {"class":"cha-content"})
		[s.extract() for s in pretext('form')]
		[s.extract() for s in pretext('a')]
		[s.extract() for s in pretext('script')]
		for div in pretext("div", {"class":"g_ad_ph"}):
			div.decompose()
		for div in pretext("div", {"class":"cha-bts"}):
			div.decompose()
		pretext = str(pretext)
				
	file = open(filename + "m" + ".xhtml", "w", encoding = "utf8")

	file.write('''
	<html xmlns="http://www.w3.org/1999/xhtml"><head/><body>
	''')
	for line in pretext:
		if "href" not in line:
			file.write(line)	
	file.write("</body>")
	file.write("</html>")
	os.remove(filename + ".xhtml")
	
#Displays and updates the download progress bar
def update_progress(progress):
    barLength = 25 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rDownload Progress: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
	
def generate(html_files, novelname, author, chaptername, chapter_s, chapter_e):
	epub = zipfile.ZipFile(novelname + "_" + chapter_s + "-" + chapter_e + ".epub", "w")

	# The first file must be named "mimetype"
	epub.writestr("mimetype", "application/epub+zip")

	# The filenames of the HTML are listed in html_files
	# We need an index file, that lists all other HTML files
	# This index file itself is referenced in the META_INF/container.xml
	# file
	epub.writestr("META-INF/container.xml", '''<container version="1.0"
			   xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
	  <rootfiles>
		<rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
	  </rootfiles>
	</container>''');

	# The index file is another XML file, living per convention
	# in OEBPS/Content.xml
	index_tpl = '''<package version="3.1"
	xmlns="http://www.idpf.org/2007/opf">
		<metadata>
			%(metadata)s
		</metadata>
		<manifest>
			%(manifest)s
		</manifest>
		<spine>
			<itemref idref="toc" linear="yes"/>
			%(spine)s
		</spine>
	</package>'''

	manifest = ""
	spine = ""
	metadata = '''<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">%(novelname)s</dc:title>
    <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns0="http://www.idpf.org/2007/opf" ns0:role="aut" ns0:file-as="Unbekannt">%(author)s</dc:creator>
	<meta xmlns:dc="http://purl.org/dc/elements/1.1/" name="calibre:series" content="%(series)s"/>''' % {
	"novelname": novelname + ": " + chapter_s + "-" + chapter_e, "author": author, "series": novelname}
	toc_manifest = '<item href="toc.xhtml" id="toc" properties="nav" media-type="application/xhtml+xml"/>'
	
	# Write each HTML file to the ebook, collect information for the index
	for i, html in enumerate(html_files):
		basename = os.path.basename(html)
		manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
					  i+1, basename)
		spine += '<itemref idref="file_%s" />' % (i+1)
		epub.write(html, "OEBPS/"+basename)

	# Finally, write the index
	epub.writestr("OEBPS/Content.opf", index_tpl % {
	"metadata": metadata,
	"manifest": manifest + toc_manifest,
	"spine": spine,
	})
	
	 #Generates a Table of Contents + lost strings
	toc_start = '''<?xml version='1.0' encoding='utf-8'?>
	<!DOCTYPE html>
	<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
	<head>
		<title>%(novelname)s</title>
	</head>
	<body>
		<section class="frontmatter TableOfContents">
			<header>
				<h1>Contents</h1>
			</header>
			<nav id="toc" role="doc-toc" epub:type="toc">
				<ol>
				%(toc_mid)s
		%(toc_end)s'''
	toc_mid = ""
	toc_end = '''</ol></nav></section></body></html>''' 
		
	for i, y in enumerate(html_files):
		ident = 0
		chapter = chaptername[i]["text"]
		toc_mid += '''<li class="toc-Chapter-rw" id="num_%s">
		<a href="%s">%s</a>
		</li>''' % (i, html_files[i], chapter)
		
	epub.writestr("OEBPS/toc.xhtml", toc_start % {"novelname": novelname, "toc_mid": toc_mid, "toc_end": toc_end})
	
	#removes all the temporary files
	for x in html_files:
		os.remove(x)