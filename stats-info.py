import os
import argparse

def getContentAndHighlight(path2File):
    '''
    Get content and highlights from a story in the file
    :param path2File: path to file
    :return: a tuple (content, highlights)
    '''

    content = []
    highlights = []
    #TODO: read file
    with open(path2File) as fread:
        lines = [line.strip() for line in fread]
    #TODO: get content and highlights
    isHighlight = False
    for line in lines:
        if line == '@highlight':
            isHighlight = True
            continue
        if isHighlight:
            highlights.append(line)
            isHighlight = False
        else:
            content.append(line)

    return (content, highlights)

def loadData(path2Dir):
    '''
    Load all stories in the directory
    :param path2Dir: path to directory
    :return: a list of tuple (content, highlights)
    '''

    # TODO: Get list files in directory
    lstFiles = [os.path.join(path2Dir, f) for f in os.listdir(path2Dir) if os.path.isfile(os.path.join(path2Dir, f))]
    # TODO: Get content and highlights from a file
    data = []
    for f in lstFiles:
        content, highlights = getContentAndHighlight(f)
        data.append((content, highlights))

    return data

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

    for content, highlights in dataset:
        nbWordsCont = 0
        nbWordsHglight = 0

        nbSentsAllConts += len(content)
        nbSentsAllHglights += len(highlights)

        for line in content:
            nbWordsCont += len(line.split())
        nbwordsAllConts += nbWordsCont

        for line in highlights:
            nbWordsHglight += len(line.split())
        nbWordsAllHglights += nbWordsHglight

    avgWordAllConts = nbwordsAllConts * 1.0 / nbDocuments
    avgWordAllHglights = nbWordsAllHglights * 1.0 / nbDocuments
    avgSentAllConts = nbSentsAllConts * 1.0 / nbDocuments
    avgSentAllHglights = nbSentsAllHglights * 1.0 / nbDocuments

    print "Number of documents: ", nbDocuments
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