# Maryland Polyvore dataset

This data set is used in [(X. Han et al. 2017) Bi-LSTM | Learning Fashion Compatibility with Bidirectional LSTMs.](https://arxiv.org/pdf/1707.05691.pdf).

## Dataset Schema

- sequences of shop item images as an outfit
- item description
- See [original dataset](https://github.com/xthan/polyvore-dataset) for details.


# Setup

- Clone this repository.
- Download `polyvore.tar.gz` and `polyvore-images.tar.gz` into `raw` directory in this repository from the [original repository](https://github.com/xthan/polyvore-dataset).
- Extract them.
    - `tar zxvf polyvore.tar.gz`
    - `tar zxcf polyvore-images.tar.gz`
- Move them to `main` directory.
    - `mkdir main` (at this repository root)
    - `mv polyvore/* ../main/labels`
    - `mv polyvore-images ../main/images`
- `pip install -r requirements.txt`


# My contribution

- `label/category2categorytype.tsv`: I categorised Han's category into 11 coarse categories in `label/categorytype.tsv`.