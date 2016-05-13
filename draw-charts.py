import os
import argparse
import ast
import pickle

import plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

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
    nbDocChartData = [go.Bar(x = [corpus for corpus in lstCorpus], y = [stInfo['nbDocument'] for stInfo in lstStatsInfo])]
    nbDocChart = py.offline.plot(nbDocChartData, os.path.join(path2OutDir, 'NbDoc'))

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
        username = fread.readline()
        apikey = fread.readline()
    #py.sign_in(username, apikey)
    #tls.set_credentials_file(username=username, api_key=apikey)

    drawChart(path2InDir, path2OutDir, lstCorpus)


if __name__ == '__main__':
    main()