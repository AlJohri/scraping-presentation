import re
import unicodecsv as csv
import requests, lxml.html

# letters = ['a', 'b'. 'c', ... 'x', 'y', 'z', 'numbers']
letters = ['c'] # only download letter c for demo

pagination_regex = re.compile(r'Page \d+ of (\d+)')
artist_id_regex = re.compile(r'http://songmeanings.com/artist/view/songs/(\d+)')

songs = []

for letter in letters:

	# find number of pages
	page = 1
	response = requests.get('http://songmeanings.com/artist/directory/%s/?page=%d' % (letter, page))
	doc = lxml.html.fromstring(response.content)
	pagination_text = doc.cssselect('.song-info li:nth-child(2)')[0].text_content().strip()
	pages = pagination_regex.findall(pagination_text)[0]

	pages = 2 # only download 1 page for demo

	# scrape pages
	for page in range(1, int(pages)):
		response = requests.get('http://songmeanings.com/artist/directory/%s/?page=%d' % (letter, page))
		artists_doc = lxml.html.fromstring(response.content)
		artists = artists_doc.cssselect("#artistslist table tbody tr")

		for artist in artists:
			artist_url = artist.cssselect('a')[0].get('href')
			artist_title = artist.cssselect('a')[0].get('title')
			artist_id = artist_id_regex.findall(artist_url)[0]
			print artist_id + '\t' + artist_title

			response = requests.get(artist_url)
			songs_doc = lxml.html.fromstring(response.content)
			artist_songs = songs_doc.cssselect('#songslist tr')
			for song in artist_songs:
				song_id = song.get('id').replace("lyric-", "")
				song_url = song.cssselect('a')[0].get('href')
				song_title = song.cssselect('a')[0].text_content()
				print "\t" + song_id.rjust(20) + '\t' + song_title

				songs.append( (song_id, song_url, song_title, artist_id, artist_url, artist_title) )

			print "-------------------------------------------------------"

# write to csv
with open("songmeanings.csv", "w") as outfile:
	writer = csv.writer(outfile)
	writer.writerow(["song_id", "song_url", "song_title", "artist_id", "artist_url", "artist_title"])
	writer.writerows(songs)