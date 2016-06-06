import numpy
import os

from nmt import train

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
                                        maxlen_src=300,
                                        maxlen_trg= 75,
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

if __name__ == '__main__':
    main(0, {
        'model': ['/ichec/home/users/%s/models/model_session1.npz'%os.environ['USER']],
        'dim_word': [500],
        'dim': [1024],
        'n-words': [30000],
        'optimizer': ['adadelta'],
        'decay-c': [0.],
        'use-dropout': [False],
        'learning-rate': [0.0001],
        'reload': [False]})


