import argparse
import os
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer

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
    tokenizer = TreebankWordTokenizer()
    result = [tokenizer.tokenize(sent) for sent in sents]
    result = [' '.join([word for word in sent]) for sent in result]

    return result

def preprocess(content, highlights):
    '''
    Preprocess the dataset:
        ./ Sentence segmentation
        ./ Word segmentation
        ./ ... (Update lated)
    :param dataset: list of tuple (filename, content, highlights)
    :return: list - Preprocessed dataset which have same format like the original
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

    return (content, highlights)

def main():
    #TODO: Parse the list of arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', required=True, type=str)
    parser.add_argument('-outdir', required=True, type=str)
    parser.add_argument('-corpus', required=True, type=str)
    args = parser.parse_args()

    path2Dir = args.dir
    path2OutDir = args.outdir
    corpus = args.corpus

    if not os.path.exists(path2OutDir):
        os.mkdir(path2OutDir)
    print "Preprocessing ..."
    count = 0
    lstFiles = getFilenames(path2Dir)
    progress_bar = ProgressBar(len(lstFiles))
    for filename in lstFiles:
        fullPath = os.path.join(path2Dir, filename)
        content, highlights = getContentAndHighlight(fullPath)
        content, highlights = preprocess(content, highlights)
        if corpus.lower() == 'dailymail':
            if content[0] == 'By':
                count += 1
        saveContentandHighlights(content, highlights, os.path.join(path2OutDir, filename + '.pre'))
        progress_bar.Increment()
    print count
    print 'DONE!'

if __name__ == '__main__':
    main()