from flask import Flask, render_template
import os, sys
import json
import Words

wobj = Words.Words()
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/getwordlist/<num>/')
def getWords(num):
	topwords = wobj.getWords(int(num))
	return render_template('wordlist.html', words=topwords)

if __name__ == "__main__":
	wobj.stopwords = Words.loadStopWords()
	wobj.wordlist, wobj.wordfreq = Words.indexDocs(wobj.stopwords)

	wobj.wordListToFreqDict()
	wobj.sortFreqDict()

	app.run()
