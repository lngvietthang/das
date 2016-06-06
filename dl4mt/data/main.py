__author__ = 'HyNguyen'

import pickle

with open("all_content-summary.content.tok.bpe.pkl", mode="rb") as f:
    hyhy = pickle.load(f)

with open("all_content-summary.summary.tok.bpe.pkl", mode="rb") as f:
    hyhy2 = pickle.load(f)

