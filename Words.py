'''This handles all of the searching and the tracking of word data'''
import re
import os, sys
import json
import nltk
from elasticsearch import Elasticsearch


es = Elasticsearch([{'host':'localhost', 'port': 9200}])
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
docdir = "docs"
HOST = "127.0.0.1:9200"
INDEX = "docs"
TYPE = "txt"

class Words:
	'''Handles the word frequencies, the most common words, etc'''
	def __init__(self):
		self.words = []
		self.topwords = []
		self.wordfreq = []
		self.wordlist = []

	def wordListToFreqDict(self):
		'''Counts the word frequencies for the given text, and compresses it into a dictionary.'''
		self.wordfreq = [self.wordlist.count(p) for p in self.wordlist]
		self.words = dict(zip(self.wordlist,self.wordfreq))

	def sortFreqDict(self):
		'''Sorts a dictionary generated by wordListToFreqDict() based on the calculated frequency'''
		aux = [(self.words[key], key) for key in self.words]
		aux.sort()
		aux.reverse()
		self.words = aux
		
	def getWords(self, num):
		'''Gets search results for the {{num}} most common words in the index'''
		thesewords = self.words[0:num]
		searchlist = []
		for w in thesewords:
			searchresults = self.search(w[1])
			for finding in searchresults:
				# Flatten the results so it can be used by datatables
				formatted = [w[1], finding["_source"]["filename"], self.highlightWord(finding["_source"]["text"], w[1])]
				searchlist.append(formatted)
		return searchlist
		
	def search(self, term):
		'''This performs the search on elasticsearch indexes'''
		result = es.search(index=INDEX, doc_type=TYPE, body={"query": {"match" : {"text": term.strip()}}})
		if result.get('hits') is not None and result['hits'].get('hits') is not None:
			hits = result['hits']['hits']
		else:
			hits = {}
		
		return hits
		
	def highlightWord(self, sentence, word):
		'''Simple function to highlight a given word and return the result with HTML formatting applied'''
		
		# We want to replace the word no matter the capitalisation...
		try:
			results = [m.start() for m in re.finditer(word.lower(), sentence.lower())]
		except:
			return sentence
			
		if results is None or len(results) == 0:
			return sentence
			
		#results = sorted(results, key=int, reverse=True)
		results.sort(reverse=True)
		
		# Find the search term (case insensitive) and replace it with formatting
		for widx in results:
			sentence = sentence[:widx] + "<b class='highlight'>" + sentence[widx:widx+len(word)] + "</b>" + sentence[widx+len(word):]
		
		return sentence
		
def indexDocs(stopwords):
	'''Originally it was planned that Elasticsearch do this, but I couldn't get the analatics to work right, so 
	I calculated word frequencies this way.'''
	text_docs = []
	wordfreq = []
	overallwords = []
	for f in os.listdir("docs"):
		# Cycle through files in docs
		if f.endswith('.txt'):
			# Only handle txt files
			fp = open(os.path.join(docdir, f), encoding='utf8')
			data = fp.read()
			wordlist = data.split()
			
			# Remove any special characters from words
			wordlist = [p.translate(dict.fromkeys(map(ord,u',!.-;"?:'))) for p in wordlist]
			for w in wordlist:
				w = w.strip().lower()
				if w in stopwords:
					# Only add if the words aren't in the "stopwords" list
					continue
				elif len(w) > 0:
					# Ignore blank strings
					wordfreq.append(wordlist.count(w))
					overallwords.append(w)
	return overallwords, wordfreq

def loadStopWords():
	# Load stopwords from file
	words = []
	with open("stopwords.txt", encoding='utf8') as stopfile:
		words = stopfile.readlines()
	words = [x.strip() for x in words]
	words = list(filter(None, words))
	return words
