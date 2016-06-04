__author__ = 'HyNguyen'

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pickle
import numpy as np
import time


def cosine(a, b):
    c =  np.dot(a,b)
    d =  np.linalg.linalg.norm(a)*np.linalg.linalg.norm(b)
    if d == 0:
        return 0
    return c/d

def cos_sim_matrix(sents_vec):
    sim_matrix = np.zeros((sents_vec.shape[0],sents_vec.shape[0]),dtype=np.float32)
    for i in range(0,sents_vec.shape[0]):
        for j in range(i+1,sents_vec.shape[0]):
            sim_matrix[i][j] = cosine(sents_vec[i],sents_vec[j])
            sim_matrix[j][i] = sim_matrix[i][j]
    return sim_matrix

def select_k_sents(sents, tf_idf_vectorize = None , k_sent = 5):

    content_str = ""
    for content in sents:
        if content[-1] != ".":
            content += "."
        content_str += " " + content

    sents = nltk.sent_tokenize(content_str)
    sents_matrix = np.array(tf_idf_vectorize.transform(sents).A, dtype=np.float32)
    sents_sim = cos_sim_matrix(sents_matrix)
    simscore = np.sum(sents_sim,axis=0)

    selected = []
    for idx in range(k_sent):
        max_idx = np.argmax(simscore)
        selected.append(sents[max_idx])
        simscore[max_idx] = 0
    return selected

def select_k_words(sents, tf_idf_vectorize = None , k_words = 300):

    content_str = ""
    for content in sents:
        if content[-1] != ".":
            content += "."
        content_str += " " + content

    sents = nltk.sent_tokenize(content_str)
    sents_matrix = np.array(tf_idf_vectorize.transform(sents).A, dtype=np.float32)
    sents_sim = cos_sim_matrix(sents_matrix)
    simscore = np.sum(sents_sim,axis=0)

    counter = 0
    selected = []
    for idx in range(len(sents)):
        max_idx = np.argmax(simscore)
        counter += len(sents[max_idx].strip().split())
        if counter > k_words:
            break
        selected.append(max_idx)
        simscore[max_idx] = 0

    selected = sorted(selected)
    result = [sents[idx] for idx in selected]
    return result

if __name__ == "__main__":

    # print(tf_idf_vectorize_path)
    # compute_idf()

    with open("testcorpus.txt", mode="r") as f:
        sents = nltk.sent_tokenize(f.read())
    #
    with open("tf_idf_vectorizer_100_01.pickle", mode="rb") as f:
        tf_idf_vectorizer = pickle.load(f)
        print ("Tf-idf Vectorizer: length of vocabulary: ", len(tf_idf_vectorizer.vocabulary_))


    start = time.time()
    selected = select_k_words(sents, tf_idf_vectorizer,300)
    end = time.time()
    print(len(" ".join(selected).strip().split()))
    print selected, end-start
