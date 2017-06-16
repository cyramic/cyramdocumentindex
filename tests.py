'''A selection of unit tests'''

import unittest
import Words

class WordsTest(unittest.TestCase):
	def test_Highlight(self):
		wobj = Words.Words()
		self.assertEqual(wobj.highlightWord("","the"), "")
		self.assertEqual(wobj.highlightWord("Hello, the rain is nice","the"), "Hello, <b class='highlight'>the</b> rain is nice")
		self.assertEqual(wobj.highlightWord("Greenhithe","the"), "Greenhi<b class='highlight'>the</b>")
		self.assertEqual(wobj.highlightWord("Testing","the"), "Testing")
		self.assertEqual(wobj.highlightWord("The sentence starts with a highlighted word","the"), "<b class='highlight'>The</b> sentence starts with a highlighted word")
		self.assertEqual(wobj.highlightWord("The the tHe thE.","the"), "<b class='highlight'>The</b> <b class='highlight'>the</b> <b class='highlight'>tHe</b> <b class='highlight'>thE</b>.")

	def test_sortFreqDict(self):
		wobj = Words.Words()
		wobj.words = {"word": 1, "another": 3, "next": 2, "final": 50}
		expectedresults = [(50, "final"), (3, "another"), (2, "next"), (1, "word")]
		
		wobj.sortFreqDict()
		
		self.assertEqual(expectedresults, wobj.words)
		
	def test_wordListToFreqDict(self):
		wobj = Words.Words()
		wobj.wordlist = ["Joy", "Joy", "Happy", "Happy", "Happy"]
		wobj.wordListToFreqDict()
		self.assertEqual(wobj.words, {'Happy': 3, 'Joy': 2})
		self.assertEqual(wobj.wordfreq, [2,2,3,3,3])
		
		wobj.wordlist = ["I", "stepped", "on", "a", "Corn", "Flake", "now", "I'm", "a", "Cereal", "Killer"]
		wobj.wordListToFreqDict()
		self.assertEqual(wobj.words, {'I': 1, 'stepped': 1, 'on': 1, 'a': 2, 'Corn': 1, 'Flake': 1, 'now': 1, "I'm": 1, "Cereal": 1, "Killer": 1})
		self.assertEqual(wobj.wordfreq, [1,1,1,2,1,1,1,1,2,1,1])


if __name__ == "__main__":
	unittest.main()
