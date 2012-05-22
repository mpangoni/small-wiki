import re

def mark_paragraphs(text):
    pattern = re.compile(r'^(?!<.*>)(.+)(?!</.*>)$', flags=re.MULTILINE)

    return pattern.sub(r'<p>\1</p>', text)

def mark_links(text):

    pattern = re.compile(r'(?!<span class="ignore">)(\[(.*?)\][ \n?]?\((.*?)\))(?!</span>)', flags=re.MULTILINE)
    
    return pattern.sub(r'<a href="\3">\2</a>', text)
        

def mark_titles(text):
    
    regex = [re.compile("#{3}(.*)#{3}", flags=re.MULTILINE), re.compile("#{2}(.*)#{2}", flags=re.MULTILINE), re.compile("#{1}(.*)#{1}", flags=re.MULTILINE)]
    size = len(regex)
    result = text
    
    for i in range(size):
        if regex[i].search(result):
            title = r'<h{0}>\1</h{0}>\n'.format(size - i)
            result = regex[i].sub(title, result)
    
    return result

def mark_spans(text):
    pattern = re.compile(r' \[(.*?)\]:(.*?) ')

    return pattern.sub(r' <span class="\2" title="\2">\1</span> ', text)

def mark_unordered_list(text):
    
    li_pattern = re.compile(r'^-(.*?)$', flags=re.MULTILINE)    
    ul_pattern = re.compile(r'((^-(.*)\n)+)', flags=re.MULTILINE)
    
    return li_pattern.sub(r'<li>\1</li>',  ul_pattern.sub(r'<ul>\n\1</ul>\n', text))

def mark_ordered_list(text):
    
    li_pattern = re.compile(r'^[0..9]{1,3}\.(.*?)$', flags=re.MULTILINE)    
    ol_pattern = re.compile(r'((^[0..9]{1,3}\.(.*)\n)+)', flags=re.MULTILINE)
    
    return li_pattern.sub(r'<li>\1</li>',  ol_pattern.sub(r'<ol>\n\1</ol>\n', text))

def mark_me(text):

    marks = [mark_titles, mark_unordered_list, mark_ordered_list, mark_paragraphs, mark_links, mark_spans]

    marked = text
    for mark in marks:
        marked = mark(marked)
        
    return marked

if __name__ == '__main__':
    import unittest

    class TestMarkme(unittest.TestCase):

        def test_mark_links(self):
            self.assertEqual('<a href="http://hello.html">hello Im a link</a>',
                             mark_links("[hello Im a link](http://hello.html)"))

            self.assertEqual('some text some text',
                            mark_links("some text some text"))

        def test_mark_multiple_links(self):
            self.assertEqual('<a href="http://hello.html">hello Im a link</a> e <a href="http://anotherhello.html">hello Im another link</a>',
                             mark_links('[hello Im a link](http://hello.html) e [hello Im another link] (http://anotherhello.html)'))

            self.assertEqual('some text <a href="http://hello.html">hello Im a link</a> some text <a href="http://anotherhello.html">hello Im another link</a>',
                            mark_links("some text [hello Im a link] (http://hello.html) some text [hello Im another link] (http://anotherhello.html)"))

            self.assertEqual('<a href="http://hello.html">hello Im a link</a>, <a href="http://anotherhello.html">hello Im another link</a>',
                             mark_links('[hello Im a link](http://hello.html), [hello Im another link] (http://anotherhello.html)'))

        def test_mark_titles(self):

            self.assertEqual('<h1> Some Title </h1>\n',
                            mark_titles("# Some Title #"))


            self.assertEqual('<h2> Some Title </h2>\n',
                            mark_titles("## Some Title ##"))


            self.assertEqual('<h3> Some Title </h3>\n',
                            mark_titles("### Some Title ###"))

        def test_mark_paragraphs(self):
            self.assertEqual('<p>   Some Text</p>\n<p>Some Text 2</p>',
                            mark_paragraphs('''   Some Text
Some Text 2'''))


        def test_mark_lists(self):
            print(mark_unordered_list('teste\n\n-hello\n-world\nteste\n-hello\n-world\n'))
                        
        def test_mark_me(self):
            sample ='''
### This is a word of conflicts ###

Some people think in war as a terrible event, but we forgot the other side.

   Generary this happens by saddness of a few peopple, remeber [second war](http://secondwar.com), where allies as vigence machine.

# [There is no place like a home](./home) #

'''
            print(mark_me(sample))

    unittest.main()

