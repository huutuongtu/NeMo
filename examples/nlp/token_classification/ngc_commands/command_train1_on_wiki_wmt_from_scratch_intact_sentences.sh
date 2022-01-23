set -x
WANDB_API_KEY="$1"
exp_name="$2"
gpus="$3"

set -e -x
mkdir -p /result/nemo_experiments
cd /workspace/NeMo
git checkout feat/punc_tarred
cd examples/nlp/token_classification
wandb login ${WANDB_API_KEY}
python punctuation_capitalization_train.py --config-path=conf/wiki_wmt \
    --config-name local_base_intact_sentences_bs20k_lr1e-4_steps500k \
    exp_manager.wandb_logger_kwargs.name=${exp_name} \
    trainer.gpus=${gpus} \
    model.train_ds.ds_item=/data/train_bert_tarred_10000 \
    model.validation_ds.ds_item=[/data/IWSLT_tst2019,/data/europarl_dev,/data/news_commentary_dev,/data/news_crawl_dev,/data/rapid_dev]
set +x