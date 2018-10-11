# Maryland Polyvore dataset

This data set is used in [(X. Han et al. 2017) Bi-LSTM | Learning Fashion Compatibility with Bidirectional LSTMs.](https://arxiv.org/pdf/1707.05691.pdf).

## Dataset Schema

- sequences of shop item images as an outfit
- item description
- See [original dataset](https://github.com/xthan/polyvore-dataset) for details.


# Setup

- Download [original dataset](https://github.com/xthan/polyvore-dataset).
- Put image data into `images`.
- Put text data into `label`.
- `pip install -r requirements.txt`


# My contribution

- `label/category2categorytype.tsv`: I categorised Han's category into 11 coarse categories in `label/categorytype.tsv`.