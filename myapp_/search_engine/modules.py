import xml.etree.ElementTree as ET
import os
import re
from django.utils.safestring import mark_safe
import re
import json
import nltk
import difflib
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from .models import Words
from .models import article


def highlight_text(text, search_word, mode):
    # 使用正則表達式進行關鍵字高亮，並標記為安全的 HTML
    flags = re.IGNORECASE
    if mode == 'Full':
        flags = 0
    highlighted = re.sub(f'({re.escape(search_word)})', r'<span class="bg-yellow-300 font-bold">\1</span>', text, flags=flags)

    return mark_safe(highlighted)

def cutTAG(xmlelement):
    xmlstr = ET.tostring(xmlelement, encoding='utf8')
    xmlstr = xmlstr.decode(encoding='utf8')
    xmlstr = re.sub('</?sup>', '', xmlstr)
    
    return ET.fromstring(xmlstr)

def findAbstract(xml_file):
    data_path = os.path.join(os.path.join(os.getcwd(), 'search_engine/data'), xml_file)


    # 读取并解析 XML 文件
    tree = ET.parse(data_path)
    root = tree.getroot()
    root = cutTAG(root)
    
    abstract = ''
    # 查找所有 AbstractText 元素
    for i, article in enumerate(root.findall(".//Abstract/AbstractText")):
        if i != 0:
            abstract += ' '
        abstract += article.text

    
    return abstract

def findtitle(xml_file):
    data_path = os.path.join(os.path.join(os.getcwd(), 'search_engine/data'), xml_file)

    # 读取并解析 XML 文件
    tree = ET.parse(data_path)
    root = tree.getroot()

    title = root.find(".//ArticleTitle")

    return title.text


def findByKeyWord(key, mode):
    data_dirPath = os.path.join(os.getcwd(), 'search_engine/data')
    XMLfile_list = os.listdir(data_dirPath)

    abstracts = []
    titles = []
    files = []
    suggestword = ''
    print(wordsuggest(key))
    if key != wordsuggest(key):
        key = wordsuggest(key)
        suggestword = wordsuggest(key)
        print('ji')
    

    for file in XMLfile_list:
        data_path = os.path.join(data_dirPath, file)
        
        # find the key word from title
        title = findtitle(file)
        abstract = findAbstract(data_path)
        flags = re.IGNORECASE
        if mode == 'Full':
            flags = 0

        if re.search(key, title, flags) or re.search(key, abstract, flags):
            # show some abstract ...
            abstracts.append(highlight_text(abstract, key, mode))
            titles.append(highlight_text(title, key, mode))
            files.append(file)
            
    
    return titles, abstracts, files, suggestword

def asciiCount(text):
    
    num_ascii = len([t for t in text if ord(t) < 128])
    num_nonascii = len(text) - num_ascii
    
    return num_ascii, num_nonascii

def sentenceCount(text):

    # replace (...)
    text = re.sub('\(.*?\)', '', text)

    sentences = text.split('.')
    num_split = len([sentence for sentence in sentences if sentence != ''])
    
    # count the num of float number
    num_float = len(re.findall('\d+\.\d+', text))

    return num_split - num_float 

def wordsCount(text):

    num = len([t for t in re.findall('\S*', text) if t != ''])

    return num
    

def staticsINFO(xml_file):
    
    # take article
    Abstract = findAbstract(xml_file)

    num_characters = len(Abstract)
    num_words = wordsCount(Abstract)
    num_sentences = sentenceCount(Abstract)
    num_ascii, num_nonascii = asciiCount(Abstract)
    
    return num_sentences, num_words, num_characters, num_ascii, num_nonascii

def Distributionbyterm(term = ''):
    data_dirPath = os.path.join(os.getcwd(), 'search_engine/data')

    if term == '':
        XMLfile_list = os.listdir(data_dirPath)

    else:
        if Words.objects.filter(term = term):
            key = Words.objects.filter(term = term)[0]
            articles = key.terms.all()
            XMLfile_list = []
            for article in articles:
                XMLfile_list.append(article.file)
            XMLfile_list = list(set(XMLfile_list))

    label, data, label_porter, data_porter = ZipfDistribution(XMLfile_list)

    return label, data, label_porter, data_porter
    
    
def ZipfDistribution(XMLfile_list):
    data_dirPath = os.path.join(os.getcwd(), 'search_engine/data')

    frequency = {}
    frequency_porter = {}
    for file in XMLfile_list:
        data_path = os.path.join(data_dirPath, file)
        
        # find the article
        abstract = findAbstract(data_path)
        words = Token(abstract)
        for word in words:

            # original chart
            count = frequency.get(word,0)
            frequency[word] = count + 1

            # porter chart
            porter_word = Words.objects.filter(term = word)[0].porter_term
            count_porter = frequency_porter.get(porter_word,0)
            frequency_porter[porter_word] = count_porter + 1
        
    frequency = {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}
    data = list(frequency.values())
    label = json.dumps(list(frequency.keys()))

    frequency_porter = {k: v for k, v in sorted(frequency_porter.items(), key=lambda item: item[1], reverse=True)}
    data_porter = list(frequency_porter.values())
    label_porter = json.dumps(list(frequency_porter.keys()))
    
    return label, data, label_porter, data_porter

def porter(word):
    # # Download required NLTK data
    # nltk.download('punkt')

    # Create a PorterStemmer object
    porter = PorterStemmer()

    # Apply Porter Stemming
    stemmed_words = porter.stem(word)

    return stemmed_words

def Token(abstract):
    words = re.findall('\S*\w+', abstract)
    Tokens = []
    for word in words:
        word = re.sub('[()]', '', word)
        Tokens.append(word)

    return Tokens

def wordsuggest(term):
    words = Words.objects.values_list('term', flat=True)

    # 使用 get_close_matches 查找相似的单词
    suggestions = difflib.get_close_matches(term, words, n=1, cutoff=0.6)[0]

    return suggestions
    