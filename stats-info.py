import argparse
import os
from utils import merge2Dict, ProgressBar, countWords, countDiff21, getFilenames, getContentAndHighlight

verbose = os.environ.get('VERBOSE', 'no') == 'yes'
debug = os.environ.get('DEBUG', 'no') == 'yes'

def getStatsInfo(path2Dir):
    '''
    Get some statistical information from the dataset
    :param path2Dir:
    :return: None
    '''
    print 'Processing...'
    lstFiles = getFilenames(path2Dir)

    nbwordsAllConts = 0
    nbWordsAllHglights = 0
    nbSentsAllConts = 0
    nbSentsAllHglights = 0
    diffHglightsVsContent = 0
    nbDocuments = len(lstFiles)
    dictWordsAllConts = {}
    dictWordsAllHglights = {}

    progress_bar = ProgressBar(nbDocuments)

    for filename in lstFiles:
        fullPath = os.path.join(path2Dir, filename)
        content, highlights = getContentAndHighlight(fullPath, format='pre')
        nbSentsAllConts += len(content)
        nbSentsAllHglights += len(highlights)

        nbWordsCont, dictWordsCont = countWords(content)
        nbwordsAllConts += nbWordsCont
        dictWordsAllConts = merge2Dict(dictWordsAllConts, dictWordsCont)

        nbWordsHglight, dictWordsHglight = countWords(highlights)
        nbWordsAllHglights += nbWordsHglight
        #TODO: Xem lai cach tinh trung binh so luong tu moi
        dictWordsAllHglights = merge2Dict(dictWordsAllHglights, dictWordsHglight)
        diffHglightsVsContent += countDiff21(dictWordsCont.keys(), dictWordsHglight.keys())
        progress_bar.Increment()

    avgWordAllConts = nbwordsAllConts * 1.0 / nbDocuments
    avgWordAllHglights = nbWordsAllHglights * 1.0 / nbDocuments
    avgSentAllConts = nbSentsAllConts * 1.0 / nbDocuments
    avgSentAllHglights = nbSentsAllHglights * 1.0 / nbDocuments
    avgDiffHglightsVsContent = diffHglightsVsContent * 1.0 /nbDocuments

    print '========================================================'
    print 'Statistical Information'
    print 'Number of documents: ', nbDocuments
    print 'Vocabulary size of contents: ', len(dictWordsAllConts)
    print 'Vocabulary size of highlights: ', len(dictWordsAllHglights)
    print 'Average words in the content: %.2f' % avgWordAllConts
    print 'Average words in the highlights: %.2f' % avgWordAllHglights
    print 'Average sentences in the content: %.2f' % avgSentAllConts
    print 'Average sentences in the highlights: %.2f' % avgSentAllHglights
    print 'Average new words in the highlights: %.2f' % avgDiffHglightsVsContent
    print '========================================================'

def main():
    #TODO: Parse the list argruments
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', required=True, type=str)

    args = parser.parse_args()

    path2Dir = args.dir

    getStatsInfo(path2Dir)
    print 'DONE!'

if __name__ == '__main__':
    main()