import argparse
import os
from utils import merge2Dict, ProgressBar, countWords, countDiff21, getFilenames, getContentAndHighlight
import numpy as np
import pickle

verbose = os.environ.get('VERBOSE', 'no') == 'yes'
debug = os.environ.get('DEBUG', 'no') == 'yes'

def getStatsInfo(path2InDir, path2OutDir, corpus):
    '''
    Get some statistical information from the dataset
    :param path2InDir:
    :param path2OutDir:
    :param corpus:
    :return: None
    '''
    print 'Processing...'
    lstFiles = getFilenames(path2InDir)

    nbwordsAllConts = 0
    nbWordsAllHglights = 0
    nbSentsAllConts = 0
    nbSentsAllHglights = 0
    diffHglightsVsContent = 0
    nbDocuments = len(lstFiles)
    dictWordsAllConts = {}
    dictWordsAllHglights = {}

    lstNbWordsConts = []
    lstNbWordsHglights = []

    progress_bar = ProgressBar(nbDocuments)

    for filename in lstFiles:
        fullPath = os.path.join(path2InDir, filename)
        content, highlights = getContentAndHighlight(fullPath, format='pre')
        nbSentsAllConts += len(content)
        nbSentsAllHglights += len(highlights)

        nbWordsCont, dictWordsCont = countWords(content)
        lstNbWordsConts.append(nbWordsCont)
        nbwordsAllConts += nbWordsCont
        dictWordsAllConts = merge2Dict(dictWordsAllConts, dictWordsCont)

        nbWordsHglight, dictWordsHglight = countWords(highlights)
        lstNbWordsHglights.append(nbWordsHglight)
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
    print 'Maximum number of words in the content: ', np.max(lstNbWordsConts)
    print 'Maximum number of words in the highlights: ', np.max(lstNbWordsHglights)
    print 'Minimum number of words in the content: ', np.min(lstNbWordsConts)
    print 'Minimum number of words in the highlights: ', np.min(lstNbWordsHglights)
    print '========================================================'

    #TODO: Write statistical info into the file
    with open(os.path.join(path2OutDir, corpus + '.info'), 'w') as fwrite:
        fwrite.write('========================================================')
        fwrite.write('Statistical Information')
        fwrite.write('Number of documents: %d' % nbDocuments)
        fwrite.write('Vocabulary size of contents: %d' % len(dictWordsAllConts))
        fwrite.write('Vocabulary size of highlights: %d' % len(dictWordsAllHglights))
        fwrite.write('Average words in the content: %.2f' % avgWordAllConts)
        fwrite.write('Average words in the highlights: %.2f' % avgWordAllHglights)
        fwrite.write('Average sentences in the content: %.2f' % avgSentAllConts)
        fwrite.write('Average sentences in the highlights: %.2f' % avgSentAllHglights)
        fwrite.write('Average new words in the highlights: %.2f' % avgDiffHglightsVsContent)
        fwrite.write('Maximum number of words in the content: %d' % np.max(lstNbWordsConts))
        fwrite.write('Maximum number of words in the highlights: %d' % np.max(lstNbWordsHglights))
        fwrite.write('Minimum number of words in the content: %d' % np.min(lstNbWordsConts))
        fwrite.write('Minimum number of words in the highlights: %d' % np.min(lstNbWordsHglights))
        fwrite.write('========================================================')
        fwrite.flush()

    #TODO: Save all statistical information into the file
    statsInfo = {}
    statsInfo['nbDocument'] = nbDocuments
    statsInfo['vbSizeContent'] = len(dictWordsAllConts)
    statsInfo['vbSizeHglight'] = len(dictWordsAllHglights)
    statsInfo['avgNbWordsContent'] = avgWordAllConts
    statsInfo['avgNbWordsHglight'] = avgWordAllHglights
    statsInfo['avgNbSentsContent'] = avgSentAllConts
    statsInfo['avgNbSentsHglight'] = avgSentAllHglights
    statsInfo['avgNbNewWords'] = avgDiffHglightsVsContent
    statsInfo['lstNbWordsCont'] = lstNbWordsConts
    statsInfo['lstNbWordsHglight'] = lstNbWordsHglights
    with open(os.path.join(path2OutDir, corpus + '.pkl'), 'w') as fwrite:
        pickle.dump(statsInfo, fwrite)

def main():
    #TODO: Parse the list argruments
    parser = argparse.ArgumentParser()
    parser.add_argument('-indir', required=True, type=str)
    parser.add_argument('-outdir', required=True, type=str)
    parser.add_argument('-corpus', required=True, type=str)
    args = parser.parse_args()

    path2InDir = args.indir
    path2OutDir = args.outdir
    corpus = args.corpus

    getStatsInfo(path2InDir, path2OutDir, corpus)
    print 'DONE!'

if __name__ == '__main__':
    main()