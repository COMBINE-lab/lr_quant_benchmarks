type=$1
TOP_LEVEL_INPUT="input"
TOP_LEVEL_RESULTS="results"
python scripts/eval_quants.py --truth ${TOP_LEVEL_INPUT}/transigner/ground_truth/${type}_ground_truth.csv \
  --oarfish ${TOP_LEVEL_RESULTS}/transigner/oarfish_quant/${type}/out_cov.quant \
  --oarfish-nocov ${TOP_LEVEL_RESULTS}/transigner/oarfish_quant/${type}/out_nocov.quant \
  --oarfish-prev ${TOP_LEVEL_RESULTS}/transigner/oarfish_main_quant/${type}/out_cov.quant \
  --oarfish-prev-nocov ${TOP_LEVEL_RESULTS}/transigner/oarfish_main_quant/${type}/out_nocov.quant \
  --kallisto ${TOP_LEVEL_RESULTS}/transigner/kallisto/${type}/bus_quant_tcc.tsv \
  --nanocount ${TOP_LEVEL_RESULTS}/transigner/NanoCount_quant/${type}/quant.tsv \
  --nanocount-nofilt ${TOP_LEVEL_RESULTS}/transigner/NanoCount_quant_nofilt/${type}/quant.tsv \
  --bambu ${TOP_LEVEL_RESULTS}/transigner/bambu_quant/${type}/counts_transcript.txt \
  --out plots/transigner/${type}
