from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from itertools import islice
import re
import io
import nltk
import itertools
from nltk.corpus import stopwords
import networkx as nx
import os

#************************************************ TEXT EXTRACT *********************************************************
path = "E:\Acads\\2nd Year\sem 3\IR\Proj\\DEMO vtt files\\"
listing = os.listdir(path)

def remove(article):
    ct=0
    ck=0
    txt=[]
    text=article.readlines()
    text=text[10:]
    text=[x for x in text if x!='\n']
    for i in range(len(text)) :
        line=text[i]
        wordList = re.sub("[^\w]", " ", line).split()
        if('align' and 'start' in wordList) :
            ct=ct+1
            ck=1
        else :
            ck=ck+1
        if(ct==1) :
            if(ck>1) :
                txt.append(text[i])
        elif(ct%2!=0) :
            if(ck>=3) :
                txt.append(text[i])
    return(txt);

def jion(txt) :
    for i in range(len(txt)) :
        txt[i]=re.sub('<[^>]+>', '', txt[i])
        txt[i]=txt[i][:-1]
    return(txt)

for lst in listing :
    article = io.open(path+"/"+lst,'r',encoding='utf-8', errors='ignore')
    txt=remove(article)
    txt=jion(txt)
    f = io.open('E:\Acads\\2nd Year\IR\Proj\\Demo extracted text\\' + lst, 'w')
    with open('E:\Acads\\2nd Year\IR\Proj\\Demo extracted text\\' + lst, "a+") as myfile:
        txt = map(str, txt)
        line = " ".join(txt)
        myfile.write(line)


# *****************************TEXT EXTRACT END*****************************************************
#******************************KEYWORDS EXTRACT*****************************************************

stop_words=set(stopwords.words("english"))

# apply syntactic filters based on POS tags
def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP']):
    return [item for item in tagged if item[1] in tags]


def normalize(tagged):
    return [(item[0].replace('.', ''), item[1]) for item in tagged]


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def lDistance(firstString, secondString):
    "Function to find the Levenshtein distance between two words/sentences - gotten from http://rosettacode.org/wiki/Levenshtein_distance#Python"
    if len(firstString) > len(secondString):
        firstString, secondString = secondString, firstString
    distances = range(len(firstString) + 1)
    for index2, char2 in enumerate(secondString):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(firstString):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1], distances[index1 + 1], newDistances[-1])))
        distances = newDistances
    return distances[-1]


def buildGraph(nodes):
    "nodes - list of hashables that represents the nodes of the graph"
    gr = nx.Graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    # add edges to the graph (weighted by Levenshtein distance)
    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        levDistance = lDistance(firstString, secondString)
        gr.add_edge(firstString, secondString, weight=levDistance)

    return gr


def extractKeyphrases(text):
    # tokenize the text using nltk
    wordTokens = nltk.word_tokenize(text)

    for word in wordTokens:
        if word in stop_words:
            wordTokens.remove(word)

    # assign POS tags to the words in the text
    tagged = nltk.pos_tag(wordTokens)
    textlist = [x[0] for x in tagged]

    tagged = filter_for_tags(tagged)
    tagged = normalize(tagged)

    unique_word_set = unique_everseen([x[0] for x in tagged])
    word_set_list = list(unique_word_set)

    # this will be used to determine adjacent words in order to construct keyphrases with two words

    graph = buildGraph(word_set_list)

    # pageRank - initial value of 1.0, error tolerance of 0,0001,
    calculated_page_rank = nx.pagerank(graph, weight='weight')

    # most important words in ascending order of importance
    keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)

    # the number of keyphrases returned will be relative to the size of the text (a third of the number of vertices)
    aThird = len(word_set_list)
    #forkeyphrases = keyphrases[0 : (int)(aThird+1)]

    # take keyphrases with multiple words into consideration as done in the paper - if two words are adjacent in the text and are selected as keywords, join them
    # together
    modifiedKeyphrases = set([])
    dealtWith = set([])  # keeps track of individual keywords that have been joined to form a keyphrase
    i = 0
    j = 1
    while j < len(textlist):
        firstWord = textlist[i]
        secondWord = textlist[j]
        if firstWord in keyphrases and secondWord in keyphrases:
            keyphrase = firstWord + ' ' + secondWord
            modifiedKeyphrases.add(keyphrase)
            dealtWith.add(firstWord)
            dealtWith.add(secondWord)
        else:
            if firstWord in keyphrases and firstWord not in dealtWith:
                modifiedKeyphrases.add(firstWord)

            # if this is the last word in the text, and it is a keyword,
            # it definitely has no chance of being a keyphrase at this point
            if j == len(textlist) - 1 and secondWord in keyphrases and secondWord not in dealtWith:
                modifiedKeyphrases.add(secondWord)

        i = i + 1
        j = j + 1
    modifiedKeyphrases=list(modifiedKeyphrases)
    modifiedKeyphrases = modifiedKeyphrases[0: (int)(aThird + 1)]
    return modifiedKeyphrases


def writeFiles(keyphrases, fileName):
    "outputs the keyphrases and summaries to appropriate files"
    keyphraseFile = io.open('E:\Acads\\2nd Year\IR\Proj\\Demo keywords\\' + fileName, 'w')
    for keyphrase in keyphrases:
        keyphraseFile.write(keyphrase + '\n')
    keyphraseFile.close()


# retrieve each of the articles
articles = os.listdir("E:\Acads\\2nd Year\IR\Proj\\Demo extracted text\\")
for article in articles:
    print('Extracting keywords from  : /' + article)
    articleFile = io.open("E:\Acads\\2nd Year\IR\Proj\\Demo extracted text\\" + article, 'r')
    text = articleFile.read()
    keyphrases = extractKeyphrases(text)
    writeFiles( keyphrases, article)

#**************************************************************************************************
'''
stop_words=set(stopwords.words("english"))

def normalize(tagged):
    return [(item[0].replace('.', ''), item[1]) for item in tagged]

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def buildGraph(nodes):
    "nodes - list of hashables that represents the nodes of the graph"
    gr = nx.Graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    # add edges to the graph (weighted by Similarity)
    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        if(wn.synsets(firstString)):
            w1=wn.synsets(firstString)[0]
            if(wn.synsets(secondString)):
                w2=wn.synsets(secondString)[0]
                if(w1 and w2):
                    similarity = w1.wup_similarity(w2)
                else:
                    similarity=0
                if(str(similarity)!='None'):
                    gr.add_edge(firstString, secondString, weight=1-similarity)
    return gr

def extractKeyphrases(text):
    wordTokens = nltk.word_tokenize(text)

    for word in wordTokens:
        if word in stop_words:
            wordTokens.remove(word)

    # assign POS tags to the words in the text
    tagged = nltk.pos_tag(wordTokens)
    tagged = normalize(tagged)

    unique_word_set = unique_everseen([x[0] for x in tagged])
    word_set_list = list(unique_word_set)
    graph = buildGraph(word_set_list)
    # pageRank - initial value of 1.0, error tolerance of 0,0001,
    calculated_page_rank = nx.pagerank(graph, weight='weight')
    # most important words in ascending order of importance
    keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)
    # the number of keyphrases returned will be relative to the size of the text (a third of the number of vertices)
    aThird = len(word_set_list)/3
    keyphrases = keyphrases[0 : (int)(aThird+1)]
    return keyphrases

def writeFiles(keyphrases, fileName):
    "outputs the keyphrases and summaries to appropriate files"
    keyphraseFile = io.open('E:\Acads\\2nd Year\IR\Proj\\Demo keywords\\' + fileName, 'w')
    for keyphrase in keyphrases:
        keyphraseFile.write(keyphrase + '\n')
    keyphraseFile.close()

# retrieve each of the articles
articles = os.listdir("E:\Acads\\2nd Year\IR\Proj\\Demo extracted text\\")
for article in articles:
    print('Extracting keywords from  : /' + article)
    articleFile = io.open('E:\Acads\\2nd Year\IR\Proj\\Demo extracted text\\' + article, 'r')
    text = articleFile.read()
    keyphrases = extractKeyphrases(text)
    writeFiles(keyphrases, article)
'''
#******************************************KEYWORDS EXTRACT END*********************************************************


#********************************************LESK and  Getting Category ************************************************


outputFile=open('output.txt','a')
for n,textfile in enumerate(os.listdir(os.getcwd()+'\\Demo extracted text')):
    total={}
    content = open('Demo extracted text\\'+ textfile).read()
    content=content.split()

    keywords = open('Demo keywords\\' + textfile).read()
    keywords=keywords.split()

    for word in keywords:
        i=0
        while(i<len(content) and content[i]!=word  ):
            i=i+1
        if (i<len(content) and content[i]==word):
            if (i > 3):
                sent=content[i-3:i+3]
            else:
                sent=content[0:i+6]

            ss=lesk(sent,word)
            #print (ss)
            if(ss):
                ssid = str(ss.offset()).zfill(8) + '-' + ss.pos()
                for k,filename in enumerate(os.listdir(os.getcwd()+'\Wordnet Extended domains\\xwnd-30g')):
                    #print("FILE ",k,": ",filename)
                    address='\Wordnet Extended domains\\xwnd-30g\\'+filename
                    for pos,line in enumerate(islice(open(os.getcwd()+address ,  'r'),500)):
                        id, score = line.strip().split('\t')
                        score=float(score)
                        if (id == ssid):
                            if filename in total:
                                total[filename]+=score
                                #print(filename, ' ', score)
                            else:
                                total[filename]=score
                            #print(word,' ',filename,' ',score)


    print("THE RESULTS ARE: ")
    maxval=0
    maxkey=''
    for key,value in total.items():
        if(value>maxval):
            maxval=value
            maxkey=key
        #print(key,' ',value)
    print("\n\nTHE FINAL RESULT IS: ")
    print('FILE :'+str(textfile).ljust(100)+ 'CATEGORY:'+str(maxkey))
    outputFile.write('FILE :'+str(textfile).ljust(100)+ 'CATEGORY:'+str(maxkey)[:-3]+'\n')

outputFile.close()


