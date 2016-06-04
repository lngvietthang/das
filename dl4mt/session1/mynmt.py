__author__ = 'HyNguyen'

from data_iterator import TextIterator
import pickle as  pkl
import numpy as np

def main(job_id, params):
    print params
    validerr = train(saveto=params['model'][0],
                                        reload_=params['reload'][0],
                                        dim_word=params['dim_word'][0],
                                        dim=params['dim'][0],
                                        n_words=params['n-words'][0],
                                        n_words_src=params['n-words'][0],
                                        decay_c=params['decay-c'][0],
                                        lrate=params['learning-rate'][0],
                                        optimizer=params['optimizer'][0],
                                        maxlen=50,
                                        batch_size=32,
                                        valid_batch_size=32,
					datasets=['/Users/HyNguyen/Documents/Research/Data/stories_4nncnn/test.content.tok',
					'/Users/HyNguyen/Documents/Research/Data/stories_4nncnn/test.summary.tok'],
					valid_datasets=['/Users/HyNguyen/Documents/Research/Data/stories_4nncnn/train100.content.tok',
					'/Users/HyNguyen/Documents/Research/Data/stories_4nncnn/train100.summary.tok'],
					dictionaries=['/Users/HyNguyen/Documents/Research/Data/stories_4nncnn/dict.content.pkl',
					"/Users/HyNguyen/Documents/Research/Data/stories_4nncnn/dict.summary.pkl"],
                                        validFreq=5000,
                                        dispFreq=10,
                                        saveFreq=5000,
                                        sampleFreq=1000,
                                        use_dropout=params['use-dropout'][0],
                                        overwrite=False)
    return validerr

# batch preparation, returns padded batches for both source and target
# sequences with their corresponding masks
def prepare_data(seqs_x, seqs_y, maxlen=None, maxlen_src= None, maxlen_trg = None ,n_words_src=30000, n_words=30000):

    # x: a list of sentences
    lengths_x = [len(s) for s in seqs_x]
    lengths_y = [len(s) for s in seqs_y]

    # filter sequences according to maximum sequence length
    if maxlen is not None:
        new_seqs_x = []
        new_seqs_y = []
        new_lengths_x = []
        new_lengths_y = []
        # Todo, fix lai len of src and trg
        for l_x, s_x, l_y, s_y in zip(lengths_x, seqs_x, lengths_y, seqs_y):
            if l_x < maxlen_src and l_y < maxlen_trg:
                new_seqs_x.append(s_x)
                new_lengths_x.append(l_x)
                new_seqs_y.append(s_y)
                new_lengths_y.append(l_y)
            else:
                print("l_x", l_x, "l_y", l_y)
        lengths_x = new_lengths_x
        seqs_x = new_seqs_x
        lengths_y = new_lengths_y
        seqs_y = new_seqs_y

        if len(lengths_x) < 1 or len(lengths_y) < 1:
            return None, None, None, None

    n_samples = len(seqs_x)
    maxlen_x = np.max(lengths_x) + 1
    maxlen_y = np.max(lengths_y) + 1

    # pad batches and create masks
    x = np.zeros((maxlen_x, n_samples)).astype('int64')
    y = np.zeros((maxlen_y, n_samples)).astype('int64')
    x_mask = np.zeros((maxlen_x, n_samples)).astype('float32')
    y_mask = np.zeros((maxlen_y, n_samples)).astype('float32')
    for idx, [s_x, s_y] in enumerate(zip(seqs_x, seqs_y)):
        x[:lengths_x[idx], idx] = s_x
        x_mask[:lengths_x[idx]+1, idx] = 1.
        y[:lengths_y[idx], idx] = s_y
        y_mask[:lengths_y[idx]+1, idx] = 1.

    return x, x_mask, y, y_mask


def train(dim_word=100,  # word vector dimensionality
          dim=1000,  # the number of GRU units
          encoder='gru',
          decoder='gru_cond_simple',
          patience=10,  # early stopping patience
          max_epochs=5000,
          finish_after=10000000,  # finish after this many updates
          dispFreq=100,
          decay_c=0.,  # L2 regularization penalty
          alpha_c=0.,  # not used
          lrate=0.01,  # learning rate
          n_words_src=100000,  # source vocabulary size
          n_words=100000,  # target vocabulary size
          maxlen = 50,
          maxlencontent=100,  # maximum length of the description
          maxlensum= 50,
          optimizer='rmsprop',
          batch_size=16,
          valid_batch_size=16,
          saveto='model.npz',
          validFreq=1000,
          saveFreq=1000,  # save the parameters after every saveFreq updates
          sampleFreq=100,  # generate some samples after every sampleFreq
          datasets=[
              '/data/lisatmp3/chokyun/europarl/europarl-v7.fr-en.en.tok',
              '/data/lisatmp3/chokyun/europarl/europarl-v7.fr-en.fr.tok'],
          valid_datasets=['../data/dev/newstest2011.en.tok',
                          '../data/dev/newstest2011.fr.tok'],
          dictionaries=[
              '/data/lisatmp3/chokyun/europarl/europarl-v7.fr-en.en.tok.pkl',
              '/data/lisatmp3/chokyun/europarl/europarl-v7.fr-en.fr.tok.pkl'],
          use_dropout=False,
          reload_=False,
          overwrite=False):

    # Model options
    model_options = locals().copy()

    # load dictionaries and invert them
    worddicts = [None] * len(dictionaries)
    worddicts_r = [None] * len(dictionaries)
    for ii, dd in enumerate(dictionaries):
        with open(dd, 'rb') as f:
            worddicts[ii] = pkl.load(f)
        worddicts_r[ii] = dict()
        for kk, vv in worddicts[ii].iteritems():
            worddicts_r[ii][vv] = kk

    print 'Loading data'
    train = TextIterator(datasets[0], datasets[1],
                         dictionaries[0], dictionaries[1],
                         n_words_source=n_words_src, n_words_target=n_words,
                         batch_size=valid_batch_size,
                         maxlen_src=300,
                         maxlen_trg=50)
    # valid = TextIterator(valid_datasets[0], valid_datasets[1],
    #                      dictionaries[0], dictionaries[1],
    #                      n_words_source=n_words_src, n_words_target=n_words,
    #                      batch_size=valid_batch_size,
    #                      maxlen_src=300,
    #                      maxlen_trg=50)
    n_samples = 0
    for x, y in train:
        n_samples += len(x)
        x, x_mask, y, y_mask = prepare_data(x, y, maxlen=maxlen, maxlen_src=300, maxlen_trg=50,n_words_src=n_words_src,n_words=n_words)
        if x is None:
            continue
        print(x.shape, x_mask.shape, y.shape, y_mask.shape)


if __name__ == '__main__':
    main(0, {
        'model': ["hynguyen.model"],
        'dim_word': [500],
        'dim': [1024],
        'n-words': [30000],
        'optimizer': ['adadelta'],
        'decay-c': [0.],
        'use-dropout': [False],
        'learning-rate': [0.0001],
        'reload': [False]})

