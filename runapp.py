''' Web interface for the searching and display'''

from flask import Flask, render_template
import os, sys
import json
import Words

# Load the words object to track data
wobj = Words.Words()
app = Flask(__name__)

@app.route('/')
def index():
	#Simple main index page
	return render_template('index.html')
	
@app.route('/getwordlist/<num>/')
def getWords(num):
	# This renders the top {num} words in the datatable
	topwords = wobj.getWords(int(num))
	return render_template('wordlist.html', words=topwords)

if __name__ == "__main__":
	# Get list of words to ignore
	wobj.stopwords = Words.loadStopWords()
	
	# Do my own word count frequency calculations
	wobj.wordlist, wobj.wordfreq = Words.indexDocs(wobj.stopwords)
	
	# Sort the word count frequency dictionary from high to low
	wobj.wordListToFreqDict()
	wobj.sortFreqDict()

	# Run the server
	app.run()
