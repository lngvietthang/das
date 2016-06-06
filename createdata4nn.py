__author__ = 'HyNguyen'

from utils import loadData, save_data_4_nn_k_words, time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-indir', required=True, type=str)
    parser.add_argument('-outdir', required=True, type=str)
    parser.add_argument('-kwords', required=True, type=int)
    parser.add_argument('-nsample', type=str, default=-1)
    args = parser.parse_args()

    path2InDir = args.indir
    path2OutDir = args.outdir
    kwords = args.kwords
    nsample = args.nsample

    dataset = loadData(path2InDir,nsample)
    start = time.time()
    save_data_4_nn_k_words(dataset,path2OutDir,k_words=kwords ,data_name="cnn")
    end = time.time()
    print("Time for ", len(dataset), ": ", end-start)