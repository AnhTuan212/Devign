import glob

import pandas as pd
import numpy as np
import os
import src.utils.functions.parse as parse

from os import listdir
from os.path import isfile, join
from src.utils.objects.input_dataset import InputDataset
from sklearn.model_selection import train_test_split


def read(path, json_file):
    """
    :param path: str
    :param json_file: str
    :return DataFrame
    """
    return pd.read_json(path + json_file)

def get_ratio(dataset, ratio):
    approx_size = int(len(dataset) * ratio)
    return dataset[:approx_size]


def load(path, pickle_file, ratio=1):
    dataset = pd.read_pickle(path + pickle_file)
    dataset.info(memory_usage='deep')
    if ratio < 1:
        dataset = get_ratio(dataset, ratio)

    return dataset


def write(data_frame: pd.DataFrame, path, file_name):
    data_frame.to_pickle(path + file_name)


def apply_filter(data_frame: pd.DataFrame, filter_func):
    return filter_func(data_frame)


def rename(data_frame: pd.DataFrame, old, new):
    return data_frame.rename(columns={old: new})


def tokenize(data_frame: pd.DataFrame):
    print(data_frame.columns)
    data_frame.function = data_frame.function.apply(parse.tokenizer)    
    # Change column name
    data_frame = rename(data_frame, 'function', 'tokens')
    # Keep just the tokens
    return data_frame[["tokens"]]


def to_files(data_frame: pd.DataFrame, out_path):
    # path = f"{self.out_path}/{self.dataset_name}/"
    os.makedirs(out_path,exist_ok=True)

    for idx, row in data_frame.iterrows():
        file_name = f"{idx}.c"
        with open(out_path + file_name, 'w') as f:
            f.write(row.function)


def create_with_index(data, columns):
    data_frame = pd.DataFrame(data, columns=columns)
    data_frame.index = list(data_frame["Index"])

    return data_frame


def inner_join_by_index(df1, df2):
    return pd.merge(df1, df2, left_index=True, right_index=True)


def train_val_test_split(data_frame: pd.DataFrame, shuffle=True):
    print("Splitting Dataset")

    # false = data_frame[data_frame.vulnerable == 0]
    # true = data_frame[data_frame.vulnerable == 1]
    # print("Day la 0 va 1 :", len(false)," ",len(true))
    # train_false, test_false = train_test_split(false, test_size=0.2, shuffle = True , random_state = 42)
    # test_false, val_false = train_test_split(test_false, test_size=0.5, shuffle = True , random_state = 42)
    # train_true, test_true = train_test_split(true, test_size=0.2, shuffle = True , random_state = 42)
    # test_true, val_true = train_test_split(test_true, test_size=0.5, shuffle = True , random_state = 42)
    # print("Day la test_true va val_true :", len(test_true)," ",len(val_true))
    # print(test_true)
    # train =pd.concat([train_true, train_false], ignore_index=True) 
    # val =pd.concat([val_true, val_false], ignore_index=True)
    # test =pd.concat([test_true,test_false], ignore_index=True) 

    # train = train.reset_index(drop=True)
    # val = val.reset_index(drop=True)
    # test = test.reset_index(drop=True)
    print(len(data_frame))
    train , both = train_test_split(data_frame , test_size = 0.1 , shuffle = True , random_state = 42)
    val , test = train_test_split(both , test_size = 0.5 , shuffle = True , random_state = 42)
    print(f"Train size: {len(train)}, Validation size: {len(val)}, Test size: {len(test)}")
    return InputDataset(train), InputDataset(test), InputDataset(val)


def get_directory_files(directory):
    return [os.path.basename(file) for file in glob.glob(f"{directory}/*.pkl")]


def loads(data_sets_dir, ratio=1):
    data_sets_files = sorted([f for f in listdir(data_sets_dir) if isfile(join(data_sets_dir, f))])

    if ratio < 1:
        data_sets_files = get_ratio(data_sets_files, ratio)

    dataset = load(data_sets_dir, data_sets_files[0])
    data_sets_files.remove(data_sets_files[0])

    for ds_file in data_sets_files:
        dataset = pd.concat([dataset, load(data_sets_dir, ds_file)], ignore_index=True)

    return dataset


def clean(data_frame: pd.DataFrame):
    return data_frame.drop_duplicates(subset="function", keep=False)


def drop(data_frame: pd.DataFrame, keys):
    for key in keys:
        del data_frame[key]


def slice_frame(data_frame: pd.DataFrame, size: int):
    data_frame_size = len(data_frame)
    return data_frame.groupby(np.arange(data_frame_size) // size)
