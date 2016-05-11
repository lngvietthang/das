import os
import sys
import io

class ProgressBar(object):
  """Simple progress bar.

  Output example:
    100.00% [2152/2152]
  """

  def __init__(self, total=100, stream=sys.stderr):
    self.total = total
    self.stream = stream
    self.last_len = 0
    self.curr = 0

  def Increment(self):
    self.curr += 1
    self.PrintProgress(self.curr)

    if self.curr == self.total:
      print ''

  def PrintProgress(self, value):
    self.stream.write('\b' * self.last_len)
    pct = 100 * self.curr / float(self.total)
    out = '{:.2f}% [{}/{}]'.format(pct, value, self.total)
    self.last_len = len(out)
    self.stream.write(out)
    self.stream.flush()

def getContentAndHighlight(path2File):
    '''
    Get content and highlights from a story in the file
    :param path2File: path to file
    :return: a tuple (content, highlights)
    '''

    content = []
    highlights = []
    lines = []
    #TODO: read file
    with io.open(path2File, encoding='utf8') as fread:
        for line in fread:
            line = line.strip()
            if line != '':
                lines.append(line)
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
    :return: a list of tuple (filename, content, highlights)
    '''
    print "Loading data..."
    # TODO: Get list files in directory
    lstFiles = [filename for filename in os.listdir(path2Dir) if os.path.isfile(os.path.join(path2Dir, filename))]
    # TODO: Get content and highlights from a file
    data = []
    progress_bar = ProgressBar(len(lstFiles))
    for filename in lstFiles:
        content, highlights = getContentAndHighlight(os.path.join(path2Dir, filename))
        data.append((filename, content, highlights))
        progress_bar.Increment()

    return data

def saveData(dataset, path2OutDir, extension):
    '''
    Save dataset in the directory. One tuple (content, highlights) to one file following the format:
    Content
    @highlight
    hightlight 1
    ...
    :param dataset: A list of tuple (filename, content, highlights)
    :param path2OutDir: Path to the output directory.
    :param extension: Extension of the file
    :return: None
    '''
    print "Saving data..."
    progress_bar = ProgressBar(len(lstFiles))
    for filename, content, highlights in dataset:
        with open(os.path.join(path2OutDir, filename + '.' + extension), 'w', encoding='utf8') as fwrite:
            fwrite.write('\n'.join([line for line in content]))
            fwrite.write('\n')
            fwrite.write('\n'.join(['@highlight\n' + line for line in highlights]))
            fwrite.flush()
            progress_bar.Increment()

def loadRule(path2File):
    '''
    Load rule
    :param path2File: path to file has rules (a can be change to b)
    :return: list of rule (a, b)
    '''
    with open(path2File) as fread:
        lines = [line.strip() for line in fread]
    rules = []
    for line in lines:
        a, b = line.split()
        rules.append((a, b))

    return rules

def merge2Dict(dict1, dict2):
    '''
    Merge 2 dictionary, if dict1 and dict2 have same key then final value = dict1.value + dict2.value
    :param dict1: Dictionary 1
    :param dict2: Dictionay 2
    :return: dict
    '''
    result = dict1
    for key, value in dict2.items():
        if result.has_key(key):
            result[key] += value
        else:
            result[key] = value

    return result

def buildDict(sents):
    '''
    Build dictionary, key: word - value: index (start from 1)
    :param sents: list of sentences
    :return: dict
    '''

    dictWords = {}
    key = 1
    for sent in sents:
        words = sent.split()
        for word in words:
            if not dictWords.has_key(word):
                dictWords[word] = key
                key += 1
    dictWords['UNK'] = key

    return dictWords

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

def countDiff21(list1, list2):
    '''
    Count the number of different between list2 and list1
    :param list1: list 1
    :param list2: list 2
    :return: the number of different
    '''

    diff21 = len(list(set(list2) - set(list1)))

    return diff21