import os
import numpy as np
from glob import glob
import re
import sys
from collections import Counter


def split_dataset(items):
    is_multi_speaker = False
    speakers = [item[-1] for item in items]
    is_multi_speaker = len(set(speakers)) > 1
    eval_split_size = 500 if len(items) * 0.01 > 500 else int(
        len(items) * 0.01)
    np.random.seed(0)
    np.random.shuffle(items)
    if is_multi_speaker:
        items_eval = []
        # most stupid code ever -- Fix it !
        while len(items_eval) < eval_split_size:
            speakers = [item[-1] for item in items]
            speaker_counter = Counter(speakers)
            item_idx = np.random.randint(0, len(items))
            if speaker_counter[items[item_idx][-1]] > 1:
                items_eval.append(items[item_idx])
                del items[item_idx]
        return items_eval, items
    else:
        return items[:eval_split_size], items[eval_split_size:]


def load_meta_data(datasets):
    meta_data_train_all = []
    meta_data_eval_all = []
    for dataset in datasets:
        name = dataset['name']
        root_path = dataset['path']
        meta_file_train = dataset['metafile_train']
        meta_file_val = dataset['metafile_val']
        preprocessor = get_preprocessor_by_name(name)

        meta_data_train = preprocessor(root_path, meta_file_train)
        if meta_file_val is None:
            meta_data_eval, meta_data_train = split_dataset(meta_data_train)
        else:
            meta_data_eval = preprocessor(root_path, meta_file_val)
        meta_data_train_all += meta_data_train
        meta_data_eval_all += meta_data_eval
    return meta_data_train_all, meta_data_eval_all


def get_preprocessor_by_name(name):
    """Returns the respective preprocessing function."""
    thismodule = sys.modules[__name__]
    return getattr(thismodule, name.lower())


def ljspeech(root_path, meta_file):
    """Normalizes the Nancy meta data file to TTS format"""
    txt_file = os.path.join(root_path, meta_file)
    items = []
    speaker_name = "ljspeech"
    with open(txt_file, 'r') as ttf:
        for line in ttf:
            cols = line.split('|')
            wav_file = os.path.join(root_path, 'wavs', cols[0] + '.wav')
            text = cols[1]
            items.append([wav_file, speaker_name])
    return items


def tts_gen(root_path, meta_file):
    txt_file = os.path.join(root_path, meta_file)
    items = []
    with open(txt_file, 'r') as ttf:
        for line in ttf:
            cols = line.split('|')
            wav_file = cols[0]
            mel_file = cols[1].strip()
            items.append([wav_file, mel_file])
    return items
