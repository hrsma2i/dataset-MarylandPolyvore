# Maryland Polyvore dataset

This data set is used in [(X. Han et al. 2017) Bi-LSTM | Learning Fashion Compatibility with Bidirectional LSTMs.](https://arxiv.org/pdf/1707.05691.pdf).

<!-- TOC -->

- [Maryland Polyvore dataset](#maryland-polyvore-dataset)
    - [Dataset Schema](#dataset-schema)
- [Setup](#setup)
- [My contribution](#my-contribution)

<!-- /TOC -->


## Dataset Schema

- sequences of shop item images as an outfit
- item description
- See [original dataset](https://github.com/xthan/polyvore-dataset) for details.


# Setup

Install the dependencies with [potry](https://python-poetry.org/).

```sh
$ poetry install
```

Make `raw` directory.

```sh
$ export THIS_REPO=/path/to/this/repo
$ mkdir -p $THIS_REPO/raw/labels
```

Download `polyvore.tar.gz` and `polyvore-images.tar.gz` into `raw/labels` and `raw` directory in this repository from the [original repository](https://github.com/xthan/polyvore-dataset).

Extract them.

```sh
$ cd $THIS_REPO/raw
$ tar zxvf $THIS_REPO/raw/labels/polyvore.tar.gz
$ tar zxvf $THIS_REPO/raw/polyvore-images.tar.gz
```

Move them to `main` directory.
Note that `main/labels` already exists,
move each file in `polyvore` into `main/labels`.

```sh
$ mv $THIS_REPO/raw/labels/* $THIS_REPO/main/labels
$ mv $THIS_REPO/raw/images $THIS_REPO/main
```

Sample data to make tiny dataset for efficient debugging.

```sh
$ brew install jq
$ cd main/labels
$ jq -c '.[]' train_no_dup.json > train_no_dup.jsonlines
$ jq -c '.[]' fill_in_blank_test.json > fill_in_blank_test.jsonlines

$ cd $THIS_REPO
$ mkdir -p tiny/labels
$ brew install coreutils
$ gshuf -n $NUM_SAMPLE main/labels/train_no_dup.jsonlines > tiny/labels/train_no_dup.jsonlines
$ gshuf -n $NUM_SAMPLE main/labels/fill_in_blank_test.jsonlines > tiny/labels/fill_in_blank_test.jsonlines

$ ./copy_images_to_tiny.sh
```


# My contribution

- `label/category2categorytype.tsv`: I categorised Han's category into 11 coarse categories in `label/categorytype.tsv`.