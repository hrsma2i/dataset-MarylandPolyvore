import os
import json
import argparse
from pprint import PrettyPrinter

from tqdm import tqdm
import pandas as pd
from pandas.io.json import json_normalize

CATEGORY = 'category'
CATEGORY_ID = 'category_id'
CATEGORYTYPE = 'categorytype'
CATEGORYTYPE_ID = 'categorytype_id'


def main(mode, order, size, dataset_root):
    # setup
    label_dir = os.path.join(dataset_root, size, 'labels')

    json_file = os.path.join(
        label_dir,
        '{}_no_dup.json'.format(mode))
    df_outfits = pd.read_json(json_file)
    print('#outfits: ', len(df_outfits))
    df_items = json_normalize(
        df_outfits.to_dict(orient='records'),
        'items', 'set_id')
    print('#items: ', len(df_items))

    ctg_tsv_file = os.path.join(
        label_dir,
        'category2categorytype.tsv')
    df_ctg = pd.read_csv(ctg_tsv_file, sep='\t')\
        .drop('num items', axis=1)

    out_file = os.path.join(
        label_dir,
        '{}_cr_{}.json'.format(mode, order))
    print('OUT FILE:', out_file)

    # '01234' -> [0, 1, 2, 3, 4]
    order = [int(i) for i in order]

    # filter
    df_items = add_ctgtp_and_remove_accessories(df_items, df_ctg, order)
    df_items = drop_tanktop_camisole(df_items)
    df_items = drop_outfit_category_duplicated(df_items)
    df_items = drop_outfit_with_full_tops_bottoms(df_items)
    df_outfits = df_items_to_df_outfits(df_items)
    df_outfits = regulate_outfit_len(df_outfits, min_=2, max_=4)
    df_outfits = drop_len2_outfit_except_for_full_shoes(df_outfits)
    df_outfits = sort_items_by_target_category(df_outfits, order)

    # save
    out_dir = os.path.dirname(out_file)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(out_file, 'w') as f:
        json.dump(df_outfits.to_dict(orient='records'), f, indent=4)


def verbose(type_='items'):
    def _verbose(func):
        def wrapper(*args, **kwargs):
            print()
            print()
            print(func.__name__)
            df_outfits_ = func(*args, **kwargs)
            print('#{}: '.format(type_), len(df_outfits_))
            return df_outfits_
        return wrapper
    return _verbose


@verbose()
def add_ctgtp_and_remove_accessories(df_items, df_ctg, order):
    df_items = df_items\
        .rename(columns={'categoryid': CATEGORY_ID})
    # add CATEGORY, CATEGORYTYPE, CATEGORYTYPE_ID columns
    df_items = df_items.merge(df_ctg, how='left', on=CATEGORY_ID)

    # remove items of accessories
    df_items = df_items[df_items[CATEGORYTYPE_ID].isin(order)]
    return df_items


@verbose()
def drop_tanktop_camisole(df_items):
    ctgids_tanktop_camisole = [
        247,
        248,
        104,
        309,
        343,
    ]
    df_items = df_items[
        ~(df_items[CATEGORY_ID].isin(ctgids_tanktop_camisole))]
    return df_items


@verbose()
def drop_outfit_category_duplicated(df_items):
    # TODO: exclude tops duplication
    # Tops duplicaiton is often.

    # TODO: keep=False -> keep='first' or 'last'
    # Ideally keep both, spliting the outfit.

    # These TODOs are not important because even the num. of
    # remained items are sufficient.

    df_items = df_items\
        .drop_duplicates(
            ['set_id', CATEGORYTYPE],
            keep=False)
    return df_items


@verbose()
def drop_outfit_with_full_tops_bottoms(df_items):
    """
    This drops outfits that have full and tops/bottoms.
    """

    def set_ids_have(categorytype):
        set_ids = df_items['set_id'][
            df_items[CATEGORYTYPE] == categorytype].tolist()
        return set(set_ids)

    set_ids_to_drop = list(
        (set_ids_have('tops') | set_ids_have('bottoms'))
        & set_ids_have('full')
    )
    df_items = df_items[~df_items['set_id'].isin(set_ids_to_drop)]
    return df_items


@verbose('outfits')
def df_items_to_df_outfits(df_items):
    tqdm.pandas(desc="df_items -> df_outfits")
    df_outfits = df_items.sort_values('set_id')\
        .groupby('set_id')[list(set(df_items.columns)-{'set_id'})]\
        .progress_apply(lambda df_outfits: df_outfits.to_dict('records'))\
        .rename('items')\
        .reset_index()
    return df_outfits


@verbose('outfits')
def regulate_outfit_len(df_outfits, min_=2, max_=4):
    df_outfits = df_outfits[
        (df_outfits['items'].apply(len) >= min_)
        & (df_outfits['items'].apply(len) <= max_)]
    return df_outfits


@verbose('outfits')
def drop_len2_outfit_except_for_full_shoes(df_outfits):
    """
    Drop outfits whose length is 2, 
    except for outfits with full and shoes
    """
    # bi: boolean index. e.g., [True, False, ...]
    len_is_2 = df_outfits['items'].apply(len) == 2
    only_have_full_shoes = df_outfits['items']\
        .apply(
            lambda items:
                set([item[CATEGORYTYPE]
                    for item in items])
                == {'full', 'shoes'}
        )

    df_outfits = df_outfits[~(
        len_is_2
        & ~only_have_full_shoes
    )]
    return df_outfits


@verbose('outfits')
def sort_items_by_target_category(df_outfits, order):
    tqdm.pandas(desc='sort by category')
    df_outfits['items'] = df_outfits['items']\
        .progress_apply(
            lambda items:
                sorted(
                    items,
                    key=lambda item:
                        order.index(item[CATEGORYTYPE_ID])))
    return df_outfits


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
    args = parser.parse_args()
    args = vars(args)

    for mode in ['train', 'valid', 'test']:
        print('------------------------------------------------------------------------------------------')
        print('MODE:', mode)
        pp = PrettyPrinter(indent=4)
        pp.pprint(args)
        args['mode'] = mode
        main(**args)
