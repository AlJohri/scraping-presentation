# requres python 2.7
# pip install requests lxml cssselect

import requests, lxml.html

for i in range(0, 700+100, 100):
	response = requests.get("http://newjersey.craigslist.org/mis/index%d.html" % i)
	doc = lxml.html.fromstring(response.content)
	for row in doc.cssselect('.row'):
		pid = row.get('data-pid')
		date = row.cssselect('.date')[0].text_content()
		text = row.cssselect('.pl a')[0].text_content()
		print pid + '\t' + date + '\t' + text
	
	raw_input("Press Enter to continue...")