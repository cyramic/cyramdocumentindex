import Words

wobj = Words.Words()
wobj.stopwords = Words.loadStopWords()
Words.esIndexDocs(wobj.stopwords)
