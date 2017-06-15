''' Simply indexes the docs in the docs directory in Elasticsearch
 This would need to be a separate process that is run in the 
 background eventually.  Ideally it would monitor the docs
 directory and compare time stamps.  For now, this is pretty basic!'''

import Words

if __name__ == "__main__":
	wobj = Words.Words()
	Words.esIndexDocs()
