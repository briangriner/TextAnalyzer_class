import requests, re
from bs4 import BeautifulSoup
from collections import Counter
import statistics as stats
import string
import pandas as pd


# create your class here
class TextAnalyzer:
    """Reads a source: url, text file or string obj and provides methods
    and properties as well as plots to analyze the distributions of words
    and characters in the text of the source file.

    Keyword arguments:
    src (obj) -- a url path, text file or string obj to analyze.
    src_type -- source type. Options are: url, path to text file, text
    string contained in program or discover method to determine source
    type."""

    def __init__(self, src, src_type=None):
        """Creates object from source file to analyze text.

        Keyword arguments:
        src (str) -- URL, path to text file or string containing text.
        src_type (str) -- file type of input source (URL, path to text
        file, string containing text or None to call discover method)."""
        self._src = src
        self._src_type = src_type
        self._orig_content = None
        self._content = None
        if self._src_type is None:
            self._src_type = self.discover()
            print(f'Source type from discover method is {self._src_type}.')
        elif self._src_type in ('url', 'path', 'text'):
            self.fetch_by_src_type(self._src_type)
        else:
            print(f'''The source type {self._src_type} is not recognized. 
            Try removing src_type= parameter for discover method.''')
        self.minlen = None
        self.maxlen = None
        self.count = None
        self.casesensitive = None

    def discover(self):
        """Determines if source object is an html file, text file or
        text string."""
        if self._src.startswith('http'):
            self._src_type = 'url'
        elif self._src.endswith('txt'):
            self._src_type = 'path'
        else:
            self._src_type = 'text'
        return self._src_type

    def fetch_by_src_type(self, src_type):
        """Method uses src_type to determine how to read the source file.

        Keyword arguments: src_type (str) -- URL, path to text file or
        text string."""
        self._src_type = src_type
        # select correct read method for source type
        if self._src_type == 'url':
            headers = {'user-agent': 'my-app/0.0.1'}
            req = requests.get(self._src, headers=headers)
            self._orig_content = req.text
            # print(self._orig_content)
            return self._orig_content
        elif self._src_type == 'path':
            with open(self._src, 'r') as f:
                self._orig_content = f.read().strip(string.punctuation)
                # print(self._orig_content)
                return self._orig_content
        else:
            self._src_type = 'text'
            self._orig_content = self._src  # read text string in prg
            # print(self._orig_content)
            return self._orig_content

    @property
    def orig_content(self):
        """Property to directly access results from fetch_by_src_type
        method."""
        return self._orig_content

    def set_content_to_tag(self, tag='div', tag_id='content-main'):
        """Method uses beautiful soup library to parse HTML for a given
        tag and id after call to fetch_by_src_type(src_type='url).
        Throws ValueError exception if tag not found.
        Method is only used if src_type is URL.

        Keyword arguments:
        tag('str') -- HTML tag name
        tag_id('str') -- HTML tag id"""
        # call fetch method for URL
        self.fetch_by_src_type(src_type='url')
        try:
            # create beautiful soup object for tag and id
            soup = BeautifulSoup(self._orig_content, 'html.parser')
            # get text and assign to _content attribute
            self._content = soup.find(tag, {'id': tag_id}).get_text()
            # print(self._content)
        except ValueError:
            # raise exception of tag or tag_id is not found
            if tag is None or tag_id is None:
                print(f"Tag {tag} or Tag_id {tag_id} is not found.")
        return self._orig_content

    def reset_content(self):
        """Reset _content attribute to _orig_content fetched by requests
         module. Useful after call to set_content_to_tag method, e.g. if
          you want to use a different tag or id to analyze the same URL.

        Use when you want to create a new beautiful soup object based on
         a new tag or tag id using set_content_to_tag method. Saves call
          to requests module since html content is already in
          _orig_content attribute."""
        if self._src_type == 'url':
            self._content = self._orig_content
            # confirm reset to _orig_content
            print('confirm reset_content: ', self._content[0])
            return self._content
        else:
            print(f'Source type {self._src_type} is not a URL.')

    def _words(self, casesensitive=False):
        """If casesensitive=False: returns list of words in upper case.
        If casesensitive=True: returns list of words from _orig_content.
        Returns list of words.

        Keyword arguments:
        casesensitive (bool) -- Returns uppercase words if False
         (default)."""
        if casesensitive is False:
            self._content = [word.strip(string.punctuation).upper() for word in self._orig_content.split()]
        else:
            self._content = [word.strip(string.punctuation) for word in self._orig_content.split()]
        # print('_words(): self._content:\n', self._content)
        return self._content

    def common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        """Returns list of 2-element tuples in the format: (word: num)
         where num is a count of word occurences in the content obtained
          from the _words method using Counter().most_common() method
           from collections module.

        Keyword arguments:
        minlen (int) -- Minimum length for word to be included.
        maxlen (int) -- Maximum length for word to be included.
        count (int) -- Number of words to include in the results.
        casesensitive (bool) -- Returns uppercase words if False
         (default)."""
        self.minlen = minlen
        print('self.minlen:', self.minlen)
        self.maxlen = maxlen
        print('self.maxlen:', self.maxlen)
        self.count = count
        print('self.count:', self.count)
        self.casesensitive = casesensitive
        print('self.casesensitive:', self.casesensitive)
        _word_list = []
        if casesensitive is False:
            _word_list = [w.upper() for w in self.words if (len(w) >= self.minlen) & (len(w) <= self.maxlen)]
            # print('self.words: casesensitive is False\n', _word_list)
        else:
            _word_list = [w for w in self.words if (len(w) >= self.minlen) & (len(w) <= self.maxlen)]
            # print('_word_list: casesensitive is True\n', _word_list)
        # use Counter from collections module
        cnt = Counter(_word_list)
        return cnt.most_common(count)

    def plot_common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        """Plots distribution of most common words in a bar chart from
         matplotlib module.

        Keyword arguments:
        minlen (int) -- Minimum length for word to be included.
        maxlen (int) -- Maximum length for word to be included.
        count (int) -- Number of words to include in the results.
        casesensitive (bool) -- Returns uppercase words if False
         (default)."""
        self.minlen = minlen
        print('self.minlen:', self.minlen)
        self.maxlen = maxlen
        print('self.maxlen:', self.maxlen)
        self.count = count
        print('self.count:', self.count)
        self.casesensitive = casesensitive
        print('self.casesensitive:', self.casesensitive)
        # convert list into DF
        _words = self.common_words(minlen=5, maxlen=10)
        df_cw = pd.DataFrame(self.common_words(self.minlen, self.maxlen, self.count, self.casesensitive))
        print('df_cw shape is: ', df_cw.shape)
        df_cw.columns = ['Word', 'Count']
        df_cw.index = df_cw['Word']
        # print(df_cw)
        plt_words = df_cw.plot(kind='bar',
                               title='Common Words',
                               figsize=(12, 6),
                               width=.8,
                               fontsize=16)
        plt_words.set_ylabel('Word', fontsize=20)
        plt_words.set_xlabel('Count', fontsize=20)
        plt_words.grid(True)

    def char_distribution(self, casesensitive=False, letters_only=False):
        """Returns a list of 2 element tuples (char, num) where char is
        character and num is the count of char.

        Keyword arguments:
        casesensitive (bool) -- Returns uppercase words if False
         (default).
        letters_only (bool) -- Includes alpha characters only if True."""
        # re for selecting only alpha chars for letters_only=True
        notalpha = re.compile('[^a-zA-Z]')
        _chars_only = notalpha.sub('', self._orig_content.rstrip('\n'))
        if not casesensitive and not letters_only:
            _chars_clean = [char.upper() for char in self._orig_content]
        elif casesensitive and not letters_only:
            _chars_clean = [char for char in self._orig_content]
        elif not casesensitive and letters_only:
            _chars_clean = [char.strip(string.punctuation).upper() for char in _chars_only]
        elif casesensitive and letters_only:
            _chars_clean = [char.strip(string.punctuation) for char in _chars_only]
        else:
            _chars_clean = []
        # use Counter from collections module
        cnt_chars = Counter(_chars_clean)
        char_dist = cnt_chars.most_common()  # [(char, num)]
        # print('char_dist:\n', char_dist)
        char_dist_sorted = sorted(char_dist, key=lambda x: x[1], reverse=False)
        print('char_dist_sorted:\n', char_dist_sorted)
        return char_dist

    def plot_char_distribution(self, casesensitive=False, letters_only=False):
        """Plots distribution of most common characters in a bar chart
         from matplotlib module.

        Keyword arguments:
        casesensitive (bool) -- Returns uppercase words if False
         (default).
        letters_only (bool) -- Includes alpha characters only if True."""
        # convert list into DF
        df_cd = pd.DataFrame(self.char_distribution(casesensitive, letters_only))
        df_cd.columns = ['Character', 'Count']
        df_cd.index = df_cd['Character']
        # print(df_cd)
        plt_chars = df_cd.plot(kind='bar',
                               title='Character Distribution',
                               figsize=(12, 6),
                               width=.8,
                               fontsize=16)
        plt_chars.set_ylabel('Character', fontsize=20)
        plt_chars.set_xlabel('Count', fontsize=20)
        plt_chars.grid(True)

    @property
    def avg_word_length(self):
        """Calculates the average word length in content."""
        _words = [_w.upper() for _w in self._words()]
        # print(f'Total # words:\n {_words}')
        _avg_word_length = sum([len(_w) for _w in _words]) / len(_words)
        # print(f'The average word length is {_avg_word_length:.2f} characters.')
        return round(_avg_word_length, 2)

    @property
    def word_count(self):
        """Number words in content."""
        # print(f'Total word count: {len(self._words()):,}')
        return len(self._words())

    @property
    def distinct_word_count(self):
        """Number of distinct words in content."""
        # print(f'Distinct word count: {len(set(self._words())):,}')
        return len(set(self._words()))

    @property
    def words(self):
        """List of all words in content, including repeats, in UPPERCASE."""
        return self._words(casesensitive=False)

    @property
    def positivity(self):
        """Calculate positivity score defined as difference between the
         number of words in a text that match a positive word corpus vs.
          the number of words that match a negative word corpus.
        Positivity score calculation:
        Initialize local var tally to 0.
        Increment tally by 1 for every word match in positive.txt.
        Decrement tally by 1 for every word match in negative.txt.
        Final positivity score:
            round( tally / self.word_count * 1000)"""
        # 1. read and parse positive word file 'positive.txt' into list
        with open('positive.txt', 'r') as _f:
            # f.read().strip(string.punctuation)
            _pdoc = _f.readlines()  # .strip(string.punctuation)
            pos_words = []
        for word in _pdoc:
            pos_words = [word.strip(string.punctuation).rstrip('\n').upper() for word in _pdoc]
            # print('pos_words:\n', pos_words)
        print(f'# of words in positive.txt is {len(pos_words):,}')
        # dedup word list with set
        print(f'# of distinct words in positive.txt is {len(set(pos_words)):,}\n')
        # 2. read and parse negative word file 'negative.txt' into list
        with open('negative.txt', 'r') as _f:
            _ndoc = _f.readlines()
            neg_words = []
        for word in _ndoc:
            neg_words = [word.strip(string.punctuation).rstrip('\n').upper() for word in _ndoc]
            # print('neg_words:\n', neg_words)
        print(f'# of words in negative.txt is {len(neg_words):,}')
        # create distinct word list with set
        print(f'# of distinct words in negative.txt is {len(set(neg_words)):,}\n')
        # 3. calculate positivity score based on pos/neg word matches
        _matches = []
        _tally = 0
        _pos = 0
        _neg = 0
        _words = self.words
        for _w in _words:
            for _p in pos_words:
                if _w == _p:
                    _pos += 1
                    _tally += 1
                    _matches.append((_w, _p, _tally))
            for _n in neg_words:
                if _w == _n:
                    _neg += 1
                    _tally -= 1
                    _matches.append((_w, _n, _tally))
        print(f'# of positive matches: {_pos:,}')
        print(f'# of negative matches: {_neg:,}')
        print(f'Tally of positive - negative matches: {_tally:,}')
        # print(f'Check: Positive - Negative Matches (should equal tally: {(_pos - _neg):,}')
        print(f'% positive matches: {_pos / (_pos + _neg):.1%}')
        # _word_count = int(self.word_count)
        _positivity = round(_tally / self.word_count * 1000)
        print('Positivity score: ', '{:,}'.format(_positivity))
        return _positivity


# unittests

import unittest


def main():
    """Run unittests."""
    url = 'https://www.webucator.com/how-to/address-by-bill-clinton-1997.cfm'
    path = 'pride-and-prejudice.txt'
    text = '''The outlook wasn't brilliant for the Mudville Nine that day;
    the score stood four to two, with but one inning more to play.
    And then when Cooney died at first, and Barrows did the same,
    a sickly silence fell upon the patrons of the game.'''

    class TestTextAnalyzer(unittest.TestCase):
        def test_discover_url(self):
            ta = TextAnalyzer(url)
            self.assertEqual(ta._src_type, 'url')

        def test_discover_path(self):
            ta = TextAnalyzer(path)
            self.assertEqual(ta._src_type, 'path')

        def test_discover_text(self):
            ta = TextAnalyzer(text)
            self.assertEqual(ta._src_type, 'text')

        def test_set_content_to_tag(self):
            ta = TextAnalyzer(url)
            ta.set_content_to_tag('div', 'content-main')
            self.assertEqual(ta._content[0:25], '\n\nAddress by Bill Clinton')

        def test_reset_content(self):
            ta = TextAnalyzer(url)
            ta.set_content_to_tag('div', 'content-main')
            ta.reset_content()
            self.assertEqual(ta._content[0], '<')

        def test_common_words(self):
            ta = TextAnalyzer(path, src_type='path')
            common_words = ta.common_words(minlen=5, maxlen=10)
            liz = common_words[0]
            self.assertEqual(liz[0], 'ELIZABETH')

        def test_avg_word_length(self):
            ta = TextAnalyzer(text, src_type='text')
            self.assertEqual(ta.avg_word_length, 4.16)

        def test_word_count(self):
            ta = TextAnalyzer(text, src_type='text')
            self.assertEqual(ta.word_count, 45)

        def test_distinct_word_count(self):
            ta = TextAnalyzer(text, src_type='text')
            self.assertEqual(ta.distinct_word_count, 38)

        def test_char_distribution(self):
            ta = TextAnalyzer(text, src_type='text')
            char_dist = ta.char_distribution(letters_only=True)
            self.assertEqual(char_dist[1][1], 20)

        def test_positivity(self):
            ta = TextAnalyzer(text, src_type='text')
            positivity = ta.positivity
            self.assertEqual(positivity, -44)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestTextAnalyzer)
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    main()
else:
    print('TextAnalyzer loaded as module')
