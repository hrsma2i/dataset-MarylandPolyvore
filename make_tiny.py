import os
import shutil
from distutils import dir_util

from tqdm import tqdm
import pandas as pd
from mljsp.sample_json import sample


def main():
    THIS_REPO = os.environ['THIS_REPO']
    in_dir = os.path.join(THIS_REPO, "main/labels")
    out_dir = os.path.join(THIS_REPO, "tiny/labels")

    print("Sample large-size json files and save them to tiny/lables")
    json_filenames = [
        "train_no_dup.json",
        "valid_no_dup.json",
        "test_no_dup.json",
        "fill_in_blank_test.json",
    ]
    for json_filename in json_filenames:
        json_file = os.path.join(in_dir, json_filename)
        out_file = os.path.join(out_dir, json_filename)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        sample(json_file, n_sample=10, seed=12345, out_file=out_file)
    
    print("Copy other ordinary-size files to tiny/labels")
    other_filenames = [
        "category2categorytype.tsv",
        "category_id.tsv",
        "categorytype.tsv",
        "categorytype_order_main.txt",
    ]
    for filename in other_filenames:
        in_file = os.path.join(in_dir, filename)
        shutil.copy(in_file, out_dir)

    print("Copy images used in sampled json files to tiny/images")
    in_img_dir = os.path.join(THIS_REPO, "main/images")
    out_img_dir = os.path.join(THIS_REPO, "tiny/images")
    for json_filename in json_filenames:
        print("    Copy images used in {}".format(json_filename))
        json_file = os.path.join(out_dir, json_filename)
        if json_filename == 'fill_in_blank_test.json':
            set_ids = pd.read_json(json_file)['question']\
                .apply(lambda item_ids: item_ids[0])\
                .apply(lambda item_id: item_id.split('_')[0])\
                .tolist()
            # item_ids: [119704139_1, 119704139_3, 119704139_4, 119704...
            # -> item_id: 119704139_1
            # -> set_id: 119704139
            set_ids += pd.read_json(json_file)['answers']\
                .apply(lambda item_ids:\
                    [item_id.split('_')[0] for item_id in item_ids])\
                .sum()
            # item_ids: [119704139_2, 148511719_1, 206598043_4, 106043...
            # -> set_ids: [119704139, 148511719, 206598043, 106043...
        else:
            set_ids = pd.read_json(json_file)["set_id"]

        for set_id in set_ids:
            in_img_sub_dir = os.path.join(in_img_dir, str(set_id))
            out_img_sub_dir = os.path.join(out_img_dir, str(set_id))
            dir_util.copy_tree(in_img_sub_dir, out_img_sub_dir)


if __name__ == "__main__":
    main()