import os, sys
import json
import nltk
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost', 'port': 9200}])
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
docdir = "docs"
HOST = "127.0.0.1:9200"
INDEX = "testdocs"
TYPE = "txt"


class Words:
	def __init__(self):
		self.words = []
		self.topwords = []
		self.wordfreq = []
		self.wordlist = []

	def wordListToFreqDict(self):
		self.wordfreq = [self.wordlist.count(p) for p in self.wordlist]
		self.words = dict(zip(self.wordlist,self.wordfreq))
		#return dict(zip(self.wordlist,wordfreq))

	def sortFreqDict(self):
		aux = [(self.words[key], key) for key in self.words]
		aux.sort()
		aux.reverse()
		self.words = aux
		
	def getWords(self, num):
		thesewords = self.words[0:num]
		searchlist = []
		for w in thesewords:
			searchresults = self.search(w[1])
			for finding in searchresults:
				formatted = [w[1], finding["_source"]["filename"], self.highlightWord(finding["_source"]["text"], w[1])]
				searchlist.append(formatted)
		return searchlist
		
	def search(self, term):
		result = es.search(index='docs', doc_type='txt', body={"query": {"match" : {"text": term.strip()}}})
		if result.get('hits') is not None and result['hits'].get('hits') is not None:
			hits = result['hits']['hits']
		else:
			hits = {}
		
		return hits
		
	def highlightWord(self, sentence, word):
		sentence = sentence.replace(word, "<b class='highlight'>"+word+"</b>")
		try:
			word = word.title()
			sentence = sentence.replace(word, "<b class='highlight'>"+word+"</b>")
		except:
			pass
		
		return sentence
		
def esDeleteIndex(indx):
	try:
		es.indices.delete(index=indx)
	except:
		return False
	return True

def esIndexDocs(stopwords):
	text_docs = []
	wordfreq = []
	overallwords = []
	for f in os.listdir("docs"):
		if f.endswith('.txt'):
			fp = open(os.path.join(docdir, f), encoding='utf8')
			data = fp.read()
			#with open(os.path.join(docdir, f), encoding='utf8') as openfile:
			tokendata = tokenizer.tokenize(data)
			for item in tokendata:
				es.index(index='docs', doc_type='txt', body={
					'filename': os.path.join(docdir, f),
					'text': item
				})
	return True

def indexDocs(stopwords):
	text_docs = []
	wordfreq = []
	overallwords = []
	for f in os.listdir("docs"):
		if f.endswith('.txt'):
			fp = open(os.path.join(docdir, f), encoding='utf8')
			data = fp.read()
			wordlist = data.split()
			wordlist = [p.translate(dict.fromkeys(map(ord,u',!.-;"?:'))) for p in wordlist]
			for w in wordlist:
				w = w.strip().lower()
				if w in stopwords:
					continue
				elif len(w) > 0:
					wordfreq.append(wordlist.count(w))
					overallwords.append(w)
	return overallwords, wordfreq

def loadStopWords():
	words = []
	with open("stopwords.txt", encoding='utf8') as stopfile:
		words = stopfile.readlines()
	words = [x.strip() for x in words]
	words = list(filter(None, words))
	return words
