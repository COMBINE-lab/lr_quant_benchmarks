TOP_LEVEL_INPUT="input"
TOP_LEVEL_RESULTS="results"
python scripts/eval_quants.py --truth ${TOP_LEVEL_INPUT}/nanosim_NA12878_dRNA__guppy/ground_truth/ground_truth.tsv \
  --oarfish ${TOP_LEVEL_RESULTS}/nanosim_NA12878_dRNA__guppy/oarfish_quant/drna/out_cov.quant \
  --oarfish-nocov ${TOP_LEVEL_RESULTS}/nanosim_NA12878_dRNA__guppy/oarfish_quant/drna/out_nocov.quant \
  --oarfish-prev ${TOP_LEVEL_RESULTS}/nanosim_NA12878_dRNA__guppy/oarfish_main_quant/drna/out_cov.quant \
  --oarfish-prev-nocov ${TOP_LEVEL_RESULTS}/nanosim_NA12878_dRNA__guppy/oarfish_main_quant/drna/out_nocov.quant \
  --nanocount ${TOP_LEVEL_RESULTS}/nanosim_NA12878_dRNA__guppy/NanoCount_quant/drna/quant.tsv \
  --nanocount-nofilt ${TOP_LEVEL_RESULTS}/nanosim_NA12878_dRNA__guppy/NanoCount_quant_nofilt/drna/quant.tsv \
  --out plots/nanosim_drna/
