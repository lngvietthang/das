import os
import argparse
import ast
import pickle

import plotly.plotly as py
import plotly.graph_objs as go

def drawChart(path2InDir, path2OutDir, lstCorpus):
    '''

    :param path2InDir:
    :param path2OutDir:
    :param lstCorpus:
    :return: None
    '''

    lstStatsInfo = []

    #TODO: Load statistical info from the different corpus
    for corpus in lstCorpus:
        with open(os.path.join(path2InDir, corpus + '.pkl')) as fread:
            lstStatsInfo.append(pickle.load(fread))

    #TODO: Draw chart
    # The number of documents Chart
    xCorpus = [corpus for corpus in lstCorpus]
    yNbDoc = [stInfo['nbDocument'] for stInfo in lstStatsInfo]
    nbDocData = [go.Bar(x = xCorpus, y = yNbDoc)]
    nbDocLayout = go.Layout(title = 'Number of Documents', width=800, height=640, \
                            annotations = [\
                                           dict(x=xi, y=yi, text=str(yi), \
                                                xanchor='center', yanchor='bottom',\
                                                showarrow=False) for xi, yi in zip(xCorpus, yNbDoc)\
                                           ]\
                            )
    nbDocFig = go.Figure(data=nbDocData, layout=nbDocLayout)
    py.image.save_as(nbDocFig, os.path.join(path2OutDir, 'NbDoc.png'))
    # The Vocabulary Size
    yVocabSizeContent = [stInfo['vbSizeContent'] for stInfo in lstStatsInfo]
    yVocabSizeHglight = [stInfo['vbSizeHglight'] for stInfo in lstStatsInfo]
    vocabSizeContentData = go.Bar(x = xCorpus, y=yVocabSizeContent, name = 'The Content')
    vocabSizeHglightData = go.Bar(x=xCorpus, y=yVocabSizeHglight, name = 'The Highlight')
    vocabSizeData = [vocabSizeContentData, vocabSizeHglightData]
    vocabSizeLayout = go.Layout(title='The Vocabulary Size', width=800, height=640, barmode='group', \
                                annotations=[ \
                                    dict(x=xi, y=yi, text=str(yi) + ' '*40, \
                                         xanchor='center', yanchor='bottom', \
                                         showarrow=False) for xi, yi in zip(xCorpus, yVocabSizeContent) \
                                    ] + [\
                                    dict(x=xi, y=yi, text=' '*40 + str(yi), \
                                         xanchor='center', yanchor='bottom', \
                                         showarrow=False) for xi, yi in zip(xCorpus, yVocabSizeHglight) \
                                    ] \
                                )
    vocabSizeFig = go.Figure(data=vocabSizeData, layout=vocabSizeLayout)
    py.image.save_as(vocabSizeFig, os.path.join(path2OutDir, 'VSize.png'))
    # The Average number of words
    yAvgNbWordsContent = [stInfo['avgNbWordsContent'] for stInfo in lstStatsInfo]
    yAvgNbWordsHglight = [stInfo['avgNbWordsHglight'] for stInfo in lstStatsInfo]
    avgNbWordsContentData = go.Bar(x=xCorpus, y=yAvgNbWordsContent, name='The Content')
    avgNbWordsHglightData = go.Bar(x=xCorpus, y=yAvgNbWordsHglight, name='The Highlight')
    avgNbWordsData = [avgNbWordsContentData, avgNbWordsHglightData]
    avgNbWordsLayout = go.Layout(title='The Average Number of Words', width=800, height=640, barmode='group')
    avgNbWordsFig = go.Figure(data=avgNbWordsData, layout=avgNbWordsLayout)
    py.image.save_as(avgNbWordsFig, os.path.join(path2OutDir, 'ANWords.png'))
    # The Average number of sentences
    yAvgNbSentsContent = [stInfo['avgNbSentsContent'] for stInfo in lstStatsInfo]
    yAvgNbSentsHglight = [stInfo['avgNbSentsHglight'] for stInfo in lstStatsInfo]
    avgNbSentsContentData = go.Bar(x=xCorpus, y=yAvgNbSentsContent, name='The Content')
    avgNbSentsHglightData = go.Bar(x=xCorpus, y=yAvgNbSentsHglight, name='The Highlight')
    avgNbSentsData = [avgNbSentsContentData, avgNbSentsHglightData]
    avgNbSentsLayout = go.Layout(title='The Average Number of Sentences', width=800, height=640, barmode='group')
    avgNbSentsFig = go.Figure(data=avgNbSentsData, layout=avgNbSentsLayout)
    py.image.save_as(avgNbSentsFig, os.path.join(path2OutDir, 'ANSents.png'))
    # The Average number of new words
    yNbNewWords = [stInfo['avgNbNewWords'] for stInfo in lstStatsInfo]
    avgNbNewWordsData = [go.Bar(x=xCorpus, y=yNbNewWords)]
    avgNbNewWordsLayout = go.Layout(title='The Average Number of New Words', width=800, height=640, \
                            annotations=[ \
                                dict(x=xi, y=yi, text=str(yi), \
                                     xanchor='center', yanchor='bottom', \
                                     showarrow=False) for xi, yi in zip(xCorpus, yNbNewWords) \
                                ] \
                            )
    avgNbNewWordsFig = go.Figure(data=avgNbNewWordsData, layout=avgNbNewWordsLayout)
    py.image.save_as(avgNbNewWordsFig, os.path.join(path2OutDir, 'ANNWords.png'))

def main():
    # TODO: Parse the list of arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-indir', required=True, type=str)
    parser.add_argument('-outdir', required=True, type=str)
    parser.add_argument('-corpus', required=True, type=str)
    args = parser.parse_args()

    path2InDir = args.indir
    path2OutDir = args.outdir
    corpus = args.corpus

    lstCorpus = ast.literal_eval(corpus)

    #TODO: Load plotly username and api-key to use plotly package
    with open('plotly-user-api.key') as fread:
        username = fread.readline().strip()
        apikey = fread.readline().strip()
    print username, apikey
    py.sign_in(username, apikey)
    #tls.set_credentials_file(username=username, api_key=apikey)

    drawChart(path2InDir, path2OutDir, lstCorpus)


if __name__ == '__main__':
    main()