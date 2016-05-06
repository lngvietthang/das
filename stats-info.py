import argparse
from utils import loadData, merge2Dict

def countWords(lines):
    '''
    Count words in lines
    :param lines:
    :return: tuple: (number of word, vocabulary)
    '''
    nbWords = 0
    dictWords = {}

    for line in lines:
        words = line.split()
        nbWords += len(words)
        for word in words:
            if not dictWords.has_key(word):
                dictWords[word] = 1
            else:
                dictWords[word] += 1
    return (nbWords, dictWords)

def getStatsInfo(path2Dir):
    '''
    Get some statistical information from the dataset
    :param path2Dir:
    :return: None
    '''
    dataset = loadData(path2Dir)

    nbwordsAllConts = 0
    nbWordsAllHglights = 0
    nbSentsAllConts = 0
    nbSentsAllHglights = 0
    nbDocuments = len(dataset)
    dictWordsAllConts = {}
    dictWordsAllHglights = {}

    for _, content, highlights in dataset:

        nbSentsAllConts += len(content)
        nbSentsAllHglights += len(highlights)

        nbWordsCont, dictWordsCont = countWords(content)
        nbwordsAllConts += nbWordsCont
        dictWordsAllConts = merge2Dict(dictWordsAllConts, dictWordsCont)

        nbWordsHglight, dictWordsHglight = countWords(highlights)
        nbWordsAllHglights += nbWordsHglight
        dictWordsAllHglights = merge2Dict(dictWordsAllHglights, dictWordsHglight)

    avgWordAllConts = nbwordsAllConts * 1.0 / nbDocuments
    avgWordAllHglights = nbWordsAllHglights * 1.0 / nbDocuments
    avgSentAllConts = nbSentsAllConts * 1.0 / nbDocuments
    avgSentAllHglights = nbSentsAllHglights * 1.0 / nbDocuments

    print "Number of documents: ", nbDocuments
    print "Vocabulary size of contents: ", len(dictWordsAllConts)
    print "Vocabulary size of highlights: ", len(dictWordsAllHglights)
    print "Average words in the content: %.2f" % avgWordAllConts
    print "Average words in the highlights: %.2f" % avgWordAllHglights
    print "Average sentences in the content: %.2f" % avgSentAllConts
    print "Average sentences in the highlights: %.2f" % avgSentAllHglights

def main():
    #TODO: Parse the list argruments
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', required=True, type=str)

    args = parser.parse_args()

    path2Dir = args.dir

    getStatsInfo(path2Dir)


if __name__ == '__main__':
    main()