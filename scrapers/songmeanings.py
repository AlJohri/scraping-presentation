import re, csv, string
import requests, lxml.html

letters = list(string.ascii_lowercase) + ['numbers']

pagination_regex = re.compile(r'Page \d+ of (\d+)')

for letter in letters:

	# find number of pages
	page = 1
	response = requests.get('http://songmeanings.com/artist/directory/%s/?page=%d' % (letter, page))
	doc = lxml.html.fromstring(response.content)
	pagination_text = doc.cssselect('.song-info li:nth-child(2)')[0].text_content().strip()
	import pdb; pdb.set_trace()
	pages = pagination_regex.findall(pagination_text)[0]

	# start from page 2 to number of pages
	for page in range(2, int(pages)):
		response = requests.get('http://songmeanings.com/artist/directory/%s/?page=%d' % (letter, page))
		doc = lxml.html.fromstring(response.content)
		artists = doc.cssselect("#artistslist table tbody tr")
		for artist in artists:
			print artist.text_content()

		# raw_input("Press Enter to continue...")