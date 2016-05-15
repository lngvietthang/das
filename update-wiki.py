import argparse
import pickle
import ast
import os

def updateWiki(path2StatsDir, path2WikiDir, lstCorpus):
    '''

    :param path2StatsDir:
    :param path2WikiDir:
    :param lstCorpus:
    :return:
    '''
    lstStatsInfo = []

    #TODO: Load statistical info from the different corpus
    for corpus in lstCorpus:
        with open(os.path.join(path2StatsDir, corpus.lower() + '.pkl')) as fread:
            lstStatsInfo.append(pickle.load(fread))
    #TODO: Draw table
    with open(os.path.join(path2WikiDir, 'cnn-dailymail-stats-info.md'), 'w') as fwrite:
        fwrite.write('#CNN/Dailymail Dataset Statistical Information:')
        fwrite.write('\n')
        # Title
        fwrite.write('|     | ')
        fwrite.write('    | '.join([corpus for corpus in lstCorpus]))
        fwrite.write('    |\n')
        # Setting alignment in column
        fwrite.write('|---- |')
        for i in range(len(lstCorpus)):
            fwrite.write('----:|')
        fwrite.write('\n')
        # The number of Documents
        fwrite.write('| Number of Document |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['nbDocument'])
        fwrite.write('\n')
        # The Vocabulary Size
        fwrite.write('| The Content Vocabulary Size |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['vbSizeContent'])
        fwrite.write('\n')
        fwrite.write('| The Highlights Vocabulary Size |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['vbSizeHglight'])
        fwrite.write('\n')
        # The Average Number of Words
        fwrite.write('| The Average Number of Word in Content |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['avgNbWordsContent'])
        fwrite.write('\n')
        fwrite.write('| The Average Number of Word in Highlight |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['avgNbWordsHglight'])
        fwrite.write('\n')
        # The Average Number of Sentences
        fwrite.write('| The Average Number of Sentences in Content |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['avgNbSentsContent'])
        fwrite.write('\n')
        fwrite.write('| The Average Number of Sentences in Highlight |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['avgNbSentsHglight'])
        fwrite.write('\n')
        # The Average Number of New Words
        fwrite.write('| The Average Number of New Words in Highlight |')
        for stInfo in lstStatsInfo:
            fwrite.write(' %d |' % stInfo['avgNbNewWords'])
        fwrite.write('\n')

        # The list of charts
        fwrite.write('Some dataset\'s statistical information:\n')
        fwrite.write('![Number of Documents](https://github.com/lngvietthang/das/blob/master/stats-info/NDoc.png)\n')
        fwrite.write('![Vocabulary Size](https://github.com/lngvietthang/das/blob/master/stats-info/VSize.png)\n')
        fwrite.write('![Average number of words](https://github.com/lngvietthang/das/blob/master/stats-info/ANWords.png)\n')
        fwrite.write('![Average number of sentences](https://github.com/lngvietthang/das/blob/master/stats-info/ANSents.png)\n')
        fwrite.write('![Average number of new words](https://github.com/lngvietthang/das/blob/master/stats-info/ANNWords.png)\n')

        fwrite.flush()

def main():
    #TODO: parse list of arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-statsdir', required=True, type=str)
    parser.add_argument('-wikidir', required=True, type=str)
    parser.add_argument('-corpus', required=True, type=str)
    args = parser.parse_args()

    path2StatsDir = args.statsdir
    path2WikiDir = args.wikidir
    corpus = args.corpus

    lstCorpus = ast.literal_eval(corpus)

    updateWiki(path2StatsDir, path2WikiDir, lstCorpus)

if __name__ == '__main__':
    main()