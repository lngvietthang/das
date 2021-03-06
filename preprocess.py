import argparse
import os
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import StanfordTokenizer, wordpunct_tokenize
from nltk.corpus import stopwords

from utils import loadRule, ProgressBar, getFilenames, getContentAndHighlight, saveContentandHighlights

verbose = os.environ.get('VERBOSE', 'no') == 'yes'
debug = os.environ.get('DEBUG', 'no') == 'yes'

def sentTokenize(lines):
    '''
    Tokenize the line in lines into sentences
    :param lines: list of paragraphs
    :return: list of sentence
    '''
    lstSents = []
    for line in lines:
        sents = sent_tokenize(line)
        lstSents += sents

    return lstSents

def wordTokenize(sents):
    '''
    Tokenize the sentence in sents into words
    :param sents: list of sentences
    :return: list of sentences which words are separated by one whitespace
    '''
    #tokenizer = StanfordTokenizer()
    result = [wordpunct_tokenize(sent) for sent in sents]
    result = [' '.join([word for word in sent]) for sent in result]

    return result

def removePunct(sents):
    '''
    Remove the punctuations in sentence
    :param sents: list of sentences
    :return: list of sentences which not contain any punctuations.
    '''
    punctuation = list(string.punctuation)
    unicodeMap = dict((ord(char), None) for char in string.punctuation)
    result = []

    for sent in sents:
        words = sent.split()
        words = [word for word in words if word not in punctuation]
        words = [word.translate(unicodeMap) for word in words]
        result.append(u' '.join([word for word in words if word != '']))

    return result

def removeStopwords(sents):
    '''
    Remove stop-words in sentences
    :param sents: list of sentences
    :return: list of sentences which not contain any punctuations.
    '''
    lstStopwords = stopwords.words('english')
    result = []

    for sent in sents:
        words = sent.split()
        words = [word for word in words if word not in lstStopwords]
        result.append(u' '.join([word for word in words]))

    return result

def preprocess(content, highlights, config):
    '''
    Preprocess the dataset:
        ./ Sentence segmentation
        ./ Word segmentation
        ./ ... (Update lated)
    :param content: list of paragraph in the content part
    :param highlights: list of highlights
    :param config: dict of config. E.g. dict['remove stopword'] = True, ...
    :return: tuple (content, highlights) are processed
    '''

    #TODO: Tokenize list of paragraphs in content part into list of sentences
    content = sentTokenize(content)
    #TODO: Tokenize words in sentences
    content = wordTokenize(content)
    highlights = wordTokenize(highlights)
    #TODO: Convert some abbreviation to standard format (more details see in abbreviation.txt)
    rules = loadRule('abbreviation.txt')
    for rule in rules:
        content = [sent.replace(rule[0], rule[1]) for sent in content]
        highlights = [sent.replace(rule[0], rule[1]) for sent in highlights]
    #TODO: Remove punctuations
    if config['remove punct']:
        content = removePunct(content)
        highlights = removePunct(highlights)
    # TODO: Remove stop-word
    if config['remove stopword']:
        content = removeStopwords(content)
        highlights = removeStopwords(highlights)

    return (content, highlights)

def main():
    #TODO: Parse the list of arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-indir', required=True, type=str)
    parser.add_argument('-outdir', required=True, type=str)
    args = parser.parse_args()

    path2InDir = args.indir
    path2OutDir = args.outdir

    if not os.path.exists(path2OutDir):
        os.mkdir(path2OutDir)
    print "Preprocessing ..."
    confPreprocess = {}
    confPreprocess['remove stopword'] = False
    confPreprocess['remove punct'] = True
    nbSkipFile = 0
    lstErrors = []
    lstFiles = getFilenames(path2InDir)
    progress_bar = ProgressBar(len(lstFiles))
    for filename in lstFiles:
        fullPath = os.path.join(path2InDir, filename)
        try:
            content, highlights = getContentAndHighlight(fullPath)
        except ValueError:
            nbSkipFile += 1
            continue
        content, highlights = preprocess(content, highlights, confPreprocess)
        saveContentandHighlights(content, highlights, os.path.join(path2OutDir, filename + '.pre'))
        progress_bar.Increment()
    print 'NOTE: We skip %d file because length of content or highlights is zero.' % nbSkipFile
    print 'DONE!'

if __name__ == '__main__':
    main()