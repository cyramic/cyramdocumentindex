''' Simply indexes the docs in the docs directory in Elasticsearch
 This would need to be a separate process that is run in the 
 background eventually.  Ideally it would monitor the docs
 directory and compare time stamps.  For now, this is pretty basic!'''

def esDeleteIndex(indx):
	''' Deletes a given index from Elasticsearch '''
	try:
		es.indices.delete(index=indx)
	except:
		return False
	return True

def esIndexDocs():
	'''Indexes documents into the Elasticsearch engine'''
	text_docs = []
	wordfreq = []
	overallwords = []
	for f in os.listdir("docs"):
		#Cycle through the docs
		if f.endswith('.txt'):
			# Only index text files.
			fp = open(os.path.join(docdir, f), encoding='utf8')
			data = fp.read()
			
			# Use NLTK to break into sentences
			tokendata = tokenizer.tokenize(data)
			for item in tokendata:
				# Add to the Elasticsearch index
				es.index(index=INDEX, doc_type=TYPE, body={
					'filename': os.path.join(docdir, f),
					'lastmodified': os.path.getmtime(os.path.join(docdir, f)),
					'text': item
				})
	return True


if __name__ == "__main__":
	esIndexDocs()
