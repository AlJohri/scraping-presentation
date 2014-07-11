import re, csv, string
import requests, lxml.html

# letters = ['a', 'b'. 'c', ... 'x', 'y', 'z', 'numbers']
letters = list(string.ascii_lowercase) + ['numbers']

pagination_regex = re.compile(r'Page \d+ of (\d+)')
artist_id_regex = re.compile(r'http://songmeanings.com/artist/view/songs/(\d+)')

letters = ['c'] # only download letter c for example script

for letter in letters:

	# find number of pages
	page = 1
	response = requests.get('http://songmeanings.com/artist/directory/%s/?page=%d' % (letter, page))
	doc = lxml.html.fromstring(response.content)
	pagination_text = doc.cssselect('.song-info li:nth-child(2)')[0].text_content().strip()
	pages = pagination_regex.findall(pagination_text)[0]

	# redownloading page 1 for simplicity of example
	# start from page 1 to number of pages
	for page in range(1, int(pages)):
		response = requests.get('http://songmeanings.com/artist/directory/%s/?page=%d' % (letter, page))
		doc = lxml.html.fromstring(response.content)
		artists = doc.cssselect("#artistslist table tbody tr")
		for artist in artists:
			artist_url = artist.cssselect('a')[0].get('href')
			artist_title = artist.cssselect('a')[0].get('title')
			artist_id = artist_id_regex.findall(artist_url)[0]
			print artist_id + '\t' + artist_title

			response = requests.get(artist_url)
			doc = lxml.html.fromstring(response.content)
			songs = doc.cssselect('#songslist tr')
			for song in songs:
				song_id = song.get('id').replace("lyric-", "")
				song_url = song.cssselect('a')[0].get('href')
				song_title = song.cssselect('a')[0].text_content()
				print "\t" + song_id.rjust(20) + '\t' + song_title

			print "-------------------------------------------------------"

		# raw_input("Press Enter to continue...")