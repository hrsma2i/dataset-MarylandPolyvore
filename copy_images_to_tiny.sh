set -eu

LABELS=tiny/labels
TINY_IMAGES=tiny/images
MAIN_IMAGES=../../main/images

cat $LABELS/train_no_dup.jsonlines | jq -r ".set_id" > $LABELS/set_id_train.txt
cat $LABELS/fill_in_blank_test.jsonlines | jq -r ".question[]" | cut -d_ -f 1 | sort | uniq > $LABELS/set_id_fitb_q.txt
cat $LABELS/fill_in_blank_test.jsonlines | jq -r ".answers[]" | cut -d_ -f 1 | sort | uniq > $LABELS/set_id_fitb_a.txt
cat $LABELS/set_id_* | sort | uniq > $LABELS/set_id.txt

mkdir $TINY_IMAGES
for set_id in $(cat $LABELS/set_id.txt); do
    ln -sfn $MAIN_IMAGES/$set_id $TINY_IMAGES/$set_id
done