type=$1
TOP_LEVEL_INPUT="input"
TOP_LEVEL_RESULTS="results"
python scripts/eval_quants.py --truth ${TOP_LEVEL_INPUT}/isoquant/ground_truth/mouse_${type}_ground_truth.csv \
  --oarfish ${TOP_LEVEL_RESULTS}/isoquant/oarfish_quant/mouse/${type}/out_cov.quant \
  --oarfish-nocov ${TOP_LEVEL_RESULTS}/isoquant/oarfish_quant/mouse/${type}/out_nocov.quant \
  --oarfish-prev ${TOP_LEVEL_RESULTS}/isoquant/oarfish_main_quant/mouse/${type}/out_cov.quant \
  --oarfish-prev-nocov ${TOP_LEVEL_RESULTS}/isoquant/oarfish_main_quant/mouse/${type}/out_nocov.quant \
  --kallisto ${TOP_LEVEL_RESULTS}/isoquant/kallisto/mouse/${type}/bus_quant_tcc.tsv \
  --nanocount ${TOP_LEVEL_RESULTS}/isoquant/NanoCount_quant/mouse/${type}/quant.tsv \
  --nanocount-nofilt ${TOP_LEVEL_RESULTS}/isoquant/NanoCount_quant_nofilt/mouse/${type}/quant.tsv \
  --bambu ${TOP_LEVEL_RESULTS}/isoquant/bambu_quant/mouse/${type}/counts_transcript.txt \
  --out plots/isoseq/${type}
