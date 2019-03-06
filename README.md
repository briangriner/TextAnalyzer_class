# TextAnalyzer_class
Python TextAnalyzer class for analysis of html pages, text files and text strings

Help on class TextAnalyzer in module __main__:

class TextAnalyzer(builtins.object)
    Reads a source: url, text file or string obj and provides methods 
    and properties as well as plots to analyze the distributions of words
    and characters in the text of the source file.
    
    Keyword arguments:
    src (obj) -- a url path, text file or string obj to analyze.
    src_type -- source type. Options are: url, path to text file, text 
    string contained in program or discover method to determine source type.
    
    Methods defined here:
    
    __init__(self, src, src_type=None)
        Creates object from source file to analyze text.
        
        Keyword arguments:
        src (str) -- URL, path to text file or string containing text.
        src_type (str) -- file type of input source (URL, path to text file, 
        string containing text or None to call discover method)
    
    char_distribution(self, casesensitive=False, letters_only=False)
        Returns a list of 2 element tuples (char, num) where char is
        character and num is the count of char.
        
        Keyword arguments:
        casesensitive (bool) -- Returns uppercase words if False (default).
        letters_only (bool) -- Includes alpha characters only if True.
    
    common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False)
        Returns list of 2-element tuples in the format: (word: num) where
        num is a count of word occurences in the content obtained from the _words 
        method using Counter().most_common() method from collections module.
        
        Keyword arguments:
        minlen (int) -- Minimum length for word to be included.
        maxlen (int) -- Maximum length for word to be included.
        count (int) -- Number of words to include in the results.
        casesensitive (bool) -- Returns uppercase words if False (default).
    
    discover(self)
        Determines if source object is an html file, text file or text string.
    
    fetch_by_src_type(self, src_type)
        Method using src_type to determine how to read the source file.
        
        Keyword arguments: src_type (str) -- URL, path to text file or 
        text string.
    
    plot_char_distribution(self, casesensitive=False, letters_only=False)
        Plots distribution of most common characters in a bar chart from matplotlib module.
        
        Keyword arguments:
        casesensitive (bool) -- Returns uppercase words if False (default).
        letters_only (bool) -- Includes alpha characters only if True.
    
    plot_common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False)
        Plots distribution of most common words in a bar chart from matplotlib module.
        
        Keyword arguments:
        minlen (int) -- Minimum length for word to be included.
        maxlen (int) -- Maximum length for word to be included.
        count (int) -- Number of words to include in the results.
        casesensitive (bool) -- Returns uppercase words if False (default).
    
    reset_content(self)
        Reset _content attribute to _orig_content fetched by requests module.
        Useful after call to set_content_to_tag method, e.g. if you want to use 
        a different tag or id to analyze the same URL.
        
        Use when you want to create a new beautiful soup object based on a new
         tag or tag id using set_content_to_tag method. Saves call to requests
         module since html content is already in _orig_content attribute.
    
    set_content_to_tag(self, tag='div', tag_id='content-main')
        Method uses beautiful soup library to parse HTML for a given tag 
        and id after call to fetch_by_src_type(src_type='url). 
        Throws ValueError exception if tag not found. 
        Method is only used if src_type is URL.
        
        Keyword arguments:
        tag('str') -- HTML tag name
        tag_id('str') -- HTML tag id
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)
    
    avg_word_length
        Calculates the average word length in content.
    
    distinct_word_count
        Number of distinct words in content.
    
    orig_content
        Property for directly access results from fetch method if needed.
    
    positivity
        Calculate positivity score defined as difference between the number
        of words in a text that match a positive word corpus vs. the number
        of words that match a negative word corpus.
        Positivity score calculation:
        Initialize local var tally to 0.
        Increment tally by 1 for every word match in positive.txt.
        Decrement tally by 1 for every word match in negative.txt.
        Final positivity score:
            round( tally / self.word_count * 1000)
    
    word_count
        Number words in content.
    
    words
        List of all words in content, including repeats, in UPPERCASE.
        
