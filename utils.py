import os
import sys
import io
import xml.etree.ElementTree as ET
import nltk
from exsum.exsum import select_k_sents, select_k_words
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

verbose = os.environ.get('VERBOSE', 'no') == 'yes'
debug = os.environ.get('DEBUG', 'no') == 'yes'

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

def getContentAndHighlight(path2File, format='raw'):
    '''
    Get content and highlights from a story in the file
    :param path2File: path to file
    :return: a tuple (content, highlights)
    '''

    # TODO: Data khong thong nhat, cai thi co nguoi publish, thoi gian, cai ko co, chi co noi dung

    content = []
    highlights = []
    lines = []
    #TODO: read file
    with io.open(path2File, encoding='utf8') as fread:
        for line in fread:
            line = line.strip()
            lines.append(line)
    #TODO: get content and highlights
    paragraph = []
    if format == 'raw':
        idxCont = 0
        for line in lines:
            if line != '':
                if line == '@highlight':
                    if len(paragraph) != 0:
                        content.append(' '.join([line for line in paragraph]))
                        paragraph = []
                    break
                paragraph.append(line)
            else:
                if len(paragraph) != 0:
                    content.append(' '.join([line for line in paragraph]))
                    paragraph = []
            idxCont += 1
        paragraph = []
        for line in lines[idxCont+1:]:
            if line != '':
                if line != '@highlight':
                    paragraph.append(line)
                else:
                    if len(paragraph) != 0:
                        highlights.append(' '.join([line for line in paragraph]))
                        paragraph = []
        if len(paragraph) != 0:
            highlights.append(' '.join([line for line in paragraph]))
    elif format == 'pre':
        N = int(lines[0].split()[1]) # The format of first line is @content N, where N is number of sentences in content part.
        content = lines[1:N+1]
        highlights = lines[N+1:]

    if len(content) == 0:
        return (None, None)
        raise ValueError('Length of Content is zero!', path2File)
    if len(highlights) == 0:
        return (None, None)
        raise ValueError('Length of Highlight is zero!', path2File)
    return (content, highlights)

def getFilenames(path2Dir):
    '''
    Get list of file names in the directory.
    :param path2Dir: path to directory
    :return: list of files name
    '''
    lstFiles = [filename for filename in os.listdir(path2Dir) if os.path.isfile(os.path.join(path2Dir, filename))]

    return lstFiles

def loadData(path2Dir, earlystop = -1):
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
    for counter,filename in enumerate(lstFiles):
        if filename[0] == ".":
            continue
        content, highlights = getContentAndHighlight(os.path.join(path2Dir, filename))
        if content is None or highlights is None:
            continue
        data.append((filename, content, highlights))
        progress_bar.Increment()
        if earlystop != -1 and counter == earlystop:
            break

    return data

def saveData(dataset, path2OutDir, extension):
    '''
    Save dataset in the directory. One tuple (content, highlights) to one file following the format:
    @content M
    content 1
    ...
    content M
    @highlight N
    hightlight 1
    ...
    hightlight N
    :param dataset: A list of tuple (filename, content, highlights)
    :param path2OutDir: Path to the output directory.
    :param extension: Extension of the file
    :return: None
    '''
    print "Saving data..."
    progress_bar = ProgressBar(len(dataset))
    for filename, content, highlights in dataset:
        with io.open(os.path.join(path2OutDir, filename + '.' + extension), 'w', encoding='utf8') as fwrite:
            fwrite.write(u'@content %d\n' % len(content))
            fwrite.write(u'\n'.join([line for line in content]))
            fwrite.write(u'\n')
            fwrite.write(u'@highlight %d\n' % len(highlights))
            fwrite.write(u'\n'.join([line for line in highlights]))
            fwrite.flush()
            progress_bar.Increment()

def saveData_ksent(dataset, path2OutDir, extension, k_sent= 5, tf_idf_vectorizer = None):
    '''
    Save dataset in the directory. One tuple (content, highlights) to one file following the format:
    @content M
    content 1
    ...
    content M
    @highlight N
    hightlight 1
    ...
    hightlight N
    :param dataset: A list of tuple (filename, content, highlights)
    :param path2OutDir: Path to the output directory.
    :param extension: Extension of the file
    :return: None
    '''
    if tf_idf_vectorizer is None:
        with open("exsum/tf_idf_vectorizer_100_01.pickle", mode="rb") as f:
            tf_idf_vectorizer = pickle.load(f)

    print "Saving data..."
    progress_bar = ProgressBar(len(dataset))
    for filename, content, highlights in dataset:
        selected_sents = select_k_sents(content,tf_idf_vectorizer, k_sent)
        saveContentandHighlights(selected_sents,highlights,os.path.join(path2OutDir, filename + '.' + extension))
        progress_bar.Increment()

def save_data_4_nn_k_sents(dataset, path2OutDir, k_sent= -1, tf_idf_vectorizer = None, data_name = "cnn"):

    if os.path.isdir(path2OutDir + data_name) is False:
        os.makedirs(path2OutDir + data_name)

    fo_content = io.open(path2OutDir + "{0}/{1}sent_{2}line.content".format(data_name,k_sent,len(dataset)), "w", encoding='utf8')
    fo_sum = io.open(path2OutDir + "{0}/{1}sent_{2}line.summary".format(data_name,k_sent,len(dataset)), "w", encoding='utf8')
    if k_sent != -1:
        if tf_idf_vectorizer is None:
            with open("exsum/tf_idf_vectorizer_100_01.pickle", mode="rb") as f:
                tf_idf_vectorizer = pickle.load(f)
        print "Saving ", k_sent, " sent ..."
        progress_bar = ProgressBar(len(dataset))
        for filename, content, highlights in dataset:
            selected_sents = select_k_sents(content,tf_idf_vectorizer, k_sent)
            fo_content.write(" ".join(selected_sents).replace("\n"," ") + "\n")
            fo_sum.write(" ".join(highlights).replace("\n"," ") + "\n")
            progress_bar.Increment()
    else:
        print "Saving all sent ..."
        progress_bar = ProgressBar(len(dataset))
        for filename, content, highlights in dataset:
            fo_content.write(" ".join(content).replace("\n"," ") + "\n")
            fo_sum.write(" ".join(highlights).replace("\n"," ") + "\n")
            progress_bar.Increment()
    fo_content.close()
    fo_sum.close()

def filter_sent(sentences):
    for idx in range(len(sentences)):
        if sentences[idx][-1].isalnum() or sentences[idx][-1] == " ":
            sentences[idx]+="."
    return sentences

def save_data_4_nn_k_words(dataset, path2OutDir, k_words= -1, tf_idf_vectorizer = None, data_name = "cnn"):
    if os.path.isdir(path2OutDir) is False:
        os.makedirs(path2OutDir)
    if os.path.isdir(path2OutDir + "/content") is False:
        os.makedirs(path2OutDir + "/content")
    if os.path.isdir(path2OutDir + "/summary") is False:
        os.makedirs(path2OutDir + "/summary")

    fo_content = io.open(path2OutDir + "/content/{0}words_{1}line.content".format(k_words,len(dataset)), "w", encoding='utf8')
    fo_sum = io.open(path2OutDir + "/summary/{0}words_{1}line.summary".format(k_words,len(dataset)), "w", encoding='utf8')
    if k_words != -1:
        if tf_idf_vectorizer is None:
            with open("exsum/tf_idf_vectorizer_100_01.pickle", mode="rb") as f:
                tf_idf_vectorizer = pickle.load(f)
        print "Saving ", k_words, " sent ..."
        progress_bar = ProgressBar(len(dataset))
        for filename, content, highlights in dataset:
            selected_sents = select_k_words(content,tf_idf_vectorizer, k_words)
            highlights = filter_sent(highlights)
            fo_content.write(" ".join(selected_sents).replace("\n"," ") + u"\n")
            fo_sum.write(" ".join(highlights).replace("\n"," ") + u"\n")
            progress_bar.Increment()
    else:
        print "Saving all sent ..."
        progress_bar = ProgressBar(len(dataset))
        for filename, content, highlights in dataset:
            highlights = filter_sent(highlights)
            fo_content.write(" ".join(content).replace("\n"," ") + "\n")
            fo_sum.write(" ".join(highlights).replace("\n"," ") + "\n")
            progress_bar.Increment()
    fo_content.close()
    fo_sum.close()


def saveXML(dataset, path_2_out_dir, extension):

    if not os.path.isdir(path_2_out_dir):
        os.makedirs(path_2_out_dir)

    print "Saving data..."
    progress_bar = ProgressBar(len(dataset))
    file_id = 1
    docs = ET.Element("docs")

    for counter, sample in enumerate(dataset):
        filename, contents, highlights = sample

        content_str = ""
        for content in contents:
            if content[-1] != ".":
                content += "."
            content_str += " " + content

        highlight_str = ""
        for highlight in highlights:
            if highlight[-1] != ".":
                highlight += "."
            highlight_str += " " + highlight

        doc = ET.SubElement(docs, "doc")
        ET.SubElement(doc, "content").text = content_str
        ET.SubElement(doc, "highlight").text = highlight_str


        if counter % 1 == 0 and counter !=0:
            tree = ET.ElementTree(docs)
            tree.write(path_2_out_dir +"/"+ str(file_id) + "." + extension)
            file_id +=1
            docs = ET.Element("docs")
        progress_bar.Increment()

    tree = ET.ElementTree(docs)
    tree.write(path_2_out_dir +"/"+ str(file_id) + "." + extension)
def loadXML(path2Dir):

    print "Loading data..."
    # TODO: Get list files in directory
    lstFiles = [filename for filename in os.listdir(path2Dir) if os.path.isfile(os.path.join(path2Dir, filename))]
    # TODO: Get content and highlights from a file
    data = []
    progress_bar = ProgressBar(len(lstFiles))
    for filename in lstFiles:
        tree = ET.parse(path2Dir + "/" +filename)
        root = tree.getroot()
        for child in root._children:
            content_str = child._children[0].text
            highlight_str = child._children[1].text
            hightlights = nltk.sent_tokenize(highlight_str)
            contents = nltk.sent_tokenize(content_str)
            data.append((filename, contents, hightlights))
        progress_bar.Increment()
    return data
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
    dictWords[u'UNK'] = key

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
def saveContentandHighlights(content, highlights, path2File):
    '''

    :param content: content of story
    :param highlights: highlights of story
    :param path2File: path to file
    :return: None
    '''
    with io.open(path2File, 'w', encoding='utf8') as fwrite:
        fwrite.write(u'@content %d\n' % len(content))
        fwrite.write(u'\n'.join([line for line in content]))
        fwrite.write(u'\n')
        fwrite.write(u'@highlight %d\n' % len(highlights))
        fwrite.write(u'\n'.join([line for line in highlights]))
        fwrite.flush()

import time

def compute_tf_idf_vectorizer(data_path="/Users/HyNguyen/Documents/Research/Data/stories", save_path="exsum/tf_idf_vectorizer_200_05.pickle", min_df = 200, max_df = 0.5):
    """
    Detail:
    Params:
        data_path: data directory
        save_path: idfs save to, suffix: 200_05: min_df= 200, max_df = 0.5(len(documents))
        min_df: lower bound
        max_df: upper bound
    """
    dataset = loadData(data_path)
    documents = []
    for counter, sample in enumerate(dataset):
        filename, contents, highlights = sample
        content_str = ""
        for content in contents:
            if content[-1] != ".":
                content += "."
            content_str += " " + content
        documents.append(content_str)

    tf_idf_vectorizer = TfidfVectorizer(max_df=max_df,min_df=min_df,stop_words=stopwords.words('english'))
    tf_idf_vectorizer.fit(documents)

    with open(save_path, mode="wb") as f:
        pickle.dump(tf_idf_vectorizer,f)

    print ("Tf-idf Vectorizer: length of vocabulary: ", len(tf_idf_vectorizer.vocabulary))


if __name__ == "__main__":



    # compute_tf_idf_vectorizer(save_path="exsum/tf_idf_vectorizer_200_01.pickle",max_df=0.1,min_df=200)

    dataset = loadData("/Users/HyNguyen/Documents/Research/Data/stories",100)
    start = time.time()
    save_data_4_nn_k_words(dataset,"/Users/HyNguyen/Documents/Research/Data/stories_4nn",k_words=100 ,data_name="cnn")
    end = time.time()
    print("time for ", len(dataset), ": ", end-start)
