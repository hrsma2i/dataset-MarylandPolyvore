import os
import json
import argparse
from pprint import PrettyPrinter

from tqdm import tqdm
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize


BLANK_POS = 'blank_pos'
QUESTION = 'question'
ANSWER = 'answer'
CHOICES = 'choices'
CATEGORY_ID = 'category_id'
CATEGORYTYPE = 'categorytype'


def main(
        order, size, dataset_root,
        k=10, unify_category=True, seed=12345):
    # setup
    label_dir = os.path.join(dataset_root, size, 'labels')

    json_file = os.path.join(
        label_dir,
        'test_cr_{}.json'.format(order))
    df_outfits = pd.read_json(json_file)
    print('#outfits: ', len(df_outfits))

    if unify_category:
        # cr: category restriction
        out_file = os.path.join(
            label_dir,
            'fitb_k{}_cr_{}.json'.format(k, order))
    else:
        # cr: category restriction
        # ncu: not category unification of choices
        out_file = os.path.join(
            label_dir,
            'fitb_k{}_cr_{}_ncu.json'.format(k, order))
    print('OUT FILE:', out_file)

    # filter
    np.random.seed(seed)
    df_outfits = make_blank_pos(df_outfits)
    df_outfits = make_answer(df_outfits)
    df_outfits = make_question(df_outfits)
    df_outfits = make_choices(df_outfits, k=k, unify_category=unify_category)
    df_outfits = add_answer_to_choices(df_outfits)
    df_outfits = df_outfits[['set_id', QUESTION, CHOICES, BLANK_POS]]

    # save
    out_dir = os.path.dirname(out_file)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(out_file, 'w') as f:
        json.dump(df_outfits.to_dict(orient='records'), f, indent=4)


def verbose(type_='outfits'):
    def _verbose(func):
        def wrapper(*args, **kwargs):
            print()
            print(func.__name__)
            df_ = func(*args, **kwargs)
            print('\t#{}: '.format(type_), len(df_))
            return df_
        return wrapper
    return _verbose


@verbose()
def make_blank_pos(df):
    tqdm.pandas(desc='make blank_pos')
    df[BLANK_POS] = df['items']\
        .progress_apply(
            lambda items:
                np.random.randint(len(items))+1)
    return df


@verbose()
def make_answer(df):
    df[ANSWER] = df\
        .apply(
            lambda row:
                dict(
                    row['items'][row[BLANK_POS]-1],
                    set_id=row['set_id']),
            axis=1)
    return df


@verbose()
def make_question(df):
    df[QUESTION] = df\
        .apply(
            lambda row:
                _list_without(
                    row['items'],
                    row[BLANK_POS]-1
                ),
            axis=1)
    return df


def _list_without(ls, ids):
    if type(ids) == int:
        ids = [ids]

    return [
        e for i, e in enumerate(ls)
        if i not in ids]


@verbose()
def make_choices(df, k=10, unify_category=True):
    df_items = json_normalize(
        df.to_dict('records'),
        'items', 'set_id')

    def is_proper_as_choice(
            row, df_items=df_items, unify_category=unify_category):
        # bi: boolean indices
        bi = df_items['set_id'] != row[ANSWER]['set_id']
        if unify_category:
            bi &= df_items[CATEGORYTYPE] == row[ANSWER][CATEGORYTYPE]
            bi &= df_items[CATEGORY_ID] != row[ANSWER][CATEGORY_ID]
        return bi

    df[CHOICES] = df\
        .progress_apply(
            lambda row:
                df_items[
                    is_proper_as_choice(row)
                ].sample(k-1).to_dict('records'),
                axis=1)

    return df


@verbose()
def add_answer_to_choices(df):
    tqdm.pandas(desc='ans + choi')
    df[CHOICES] = df\
        .progress_apply(
            lambda row:
                [row[ANSWER]] + row[CHOICES],
            axis=1)
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--order',
        default='01234',
        type=str,
        help='0: outer, 1: tops, 2: full, 3: bottoms, 4: shoes',
    )
    parser.add_argument(
        '-s', '--size',
        default='tiny',
        help='tiny, main'
    )
    parser.add_argument(
        '--dataset_root',
        default=os.environ['THIS_REPO'],
    )
    parser.add_argument(
        '-k', '--k',
        default=10,
        type=int,
        help='the number of choices',
    )
    parser.add_argument(
        "-nuc", '--not_unify_category',
        action='store_false',
        dest='unify_category',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=12345,
    )
    args = parser.parse_args()
    args = vars(args)

    pp = PrettyPrinter(indent=4)
    pp.pprint(args)
    main(**args)
