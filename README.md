# Maryland Polyvore dataset

This data set is used in [(X. Han et al. 2017) Bi-LSTM | Learning Fashion Compatibility with Bidirectional LSTMs.](https://arxiv.org/pdf/1707.05691.pdf).

## Dataset Schema

- sequences of shop item images as an outfit
- item description
- See [original dataset](https://github.com/xthan/polyvore-dataset) for details.


# Setup

Clone this repository.

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

Install [hrsma2i/ml_json_processor](https://github.com/hrsma2i/ml_json_processor).
Make tiny dataset, sampling `N` samples from json files in `main` directory.

```sh
$ python make_tiny.py
```

# My contribution

- `label/category2categorytype.tsv`: I categorised Han's category into 11 coarse categories in `label/categorytype.tsv`.