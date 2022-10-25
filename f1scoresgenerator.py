import re
import argparse
import numpy as np
from pythonrouge.pythonrouge import Pythonrouge
from pprint import pprint
from numpy import random
from nltk.stem.porter import *


def evaluate_func(opts):
    preds_file = open(opts.pred, encoding='utf-8')
    preds_lines = preds_file.readlines()
    target_file = open(opts.tgt, encoding='utf-8')
    target_lines = target_file.readlines()
    file_len = len(target_lines)

    stemmer = PorterStemmer()
    trg_cnt = []
    correct_cnt = {}
    gold_cnt = 0
    for top_k in [1, 5, 10, 15]:
        correct_cnt[top_k] = 0

    ap_cnt = []
    trg_cnt = []
 
    for pred, tgt in zip(preds_lines, target_lines):
        preds = pred.split(';')
        tgts = tgt.split(';')
        preds = [stemmer.stem(t.strip()) for t in preds if t.strip()]
        tgts = [stemmer.stem(t.strip()) for t in tgts if t.strip()]
        gold_cnt += len(tgts)
        trg_cnt.append(len(tgts))
        for top_k in [1, 5, 10, 15]:
            top_preds = preds[:top_k]
            for tag in tgts:
                if tag in top_preds:
                    correct_cnt[top_k] += 1
        tmp_cnt = [1 if t in tgts else 0 for t in preds]
        ap_cnt.append(tmp_cnt)
    for top_k in [1, 5, 10, 15]:
        ap_topk = []
        f1 = 0
        acc = correct_cnt[top_k] / float(top_k * file_len)
        recall = correct_cnt[top_k] / float(gold_cnt)
        if acc == 0 or recall == 0:
            f1 = 0
        else:
            f1 = 2 * acc * recall / (acc + recall)

        print('The top_k %d: accuracy = %.6f, recall =  %.6f , f scores =  %.6f ' %
              (top_k, acc, recall, f1))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluation')
    parser.add_argument('-tgt', type=str, required=True)
    parser.add_argument('-train_tgt', type=str)
    parser.add_argument('-pred', type=str, required=True)
    parser.add_argument('-random', type=int, default=0)

    opts = parser.parse_args()

    evaluate_func(opts=opts)