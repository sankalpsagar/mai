from jikanpy import Jikan
import urllib
import subprocess
import textwrap

wrapper=textwrap.TextWrapper(initial_indent='', subsequent_indent='\t'*2, width=50)

# Color Escape Characters
CEND = '\33[0m'
CRED = '\33[31m'
CGREEN = '\33[32m'

def query_helper(s):

	s = s.lower()

	if (s[0:3] != 'mai'):
		print(CGREEN + "[Mai] Couldn't find a Mai command anywhere. Use mai help to see how commands to Mai works." + CEND)
	if (s[0:3] == 'mai'):
		
		if (s[4:8] == 'exit'):
			print(CGREEN + '[Mai] Sayonara!' + CEND)
			raise SystemExit

		if (s[4:10] == 'search'):
			search_anime(s[11:])

		if (s[4:8] == 'help'):
			print(CGREEN + "[Mai] Commands to mai are prefaced by using mai." + CEND)
			print(CGREEN + "mai [help] [exit] [search]" + CEND)
			print(CGREEN + "Use Mai followed by any of the commands." + CEND)
	return

def search_anime(s):
	jikan = Jikan()
	results = jikan.search('anime', s)
	
	result = {}

	print(CGREEN + "[Mai] These are the top results I found." + CEND)

	for idx, resultitems in enumerate(results['results'], start=1):
		print("\t" + CRED + str(idx) + ". " + wrapper.fill(resultitems['title']) +CEND)
		# storing mal_id for later use
		result[idx] = resultitems['mal_id']

	# to check if everything is working as expected
	# print(result)

	print(CGREEN + "[Mai] Type the index of the anime you want information on or type 0 to exit: " + CEND, end = ' ')
	idx = int(input())

	if (idx == 0):
		return

	results = jikan.anime(result[idx])
	print(CGREEN + "[Mai] This is the information I found on the requested anime (press q to exit imageviewer)" + CEND)

	# sanity check
	# print(results)

	# downloading image and storing in cache
	f = open('cachepic.jpg', 'wb')
	f.write(urllib.request.urlopen(results['image_url']).read())
	f.close()

	# ugh i don't like this hack. depends too much on system and imageviewer installed. try to fix this later.
	subprocess.call(["feh", "-x", "cachepic.jpg"])

	title = results['title']
	episodes = results['episodes']
	status = results['status']
	# returns as list
	title_syns = results['title_synonyms']
	date = results['aired']['string']
	syn = results['synopsis']
	score = results['score']

	printnicely(title, title_syns, score, status, syn, episodes, date)

def printnicely(t, ts, s, st, syn, ep, d):
	print(CRED + "\tTitle:" + CEND + t)
	print("\tSynonyms: ", end='')

	tsstring = ""

	for i, synonyms in enumerate(ts):
		if len(ts) == 1:
			tsstring += synonyms
		elif len(ts) > 1:
				tsstring += synonyms + ", "
				if (i == len(ts)-1):
					tsstring += synonyms

	print(wrapper.fill(tsstring))

	print("\tScore: " + str(s))
	print("\tStatus: " + st)
	print(CGREEN + "\tSynopsis: " + CEND + wrapper.fill(syn))
	print("\tEpisodes: " + str(ep))
	print("\tDate Aired: "+ d)
	return


if __name__ == '__main__':
	print("Directly executing searchanime function.")
	while(1):
		print("$", end = ' ')
		query = input()  
		query_helper(query)

