[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13130623.svg)](https://doi.org/10.5281/zenodo.13130623)

# Oarfish-only results
Pre-computed results appear below.

### dRNA simulations (using human_NA12878_dRNA_Bham1_guppy_reads.fastq.gz from [https://zenodo.org/records/11201284](https://zenodo.org/records/11201284))

#### run on a BAM file *with* filtering using `-F2052`

Alignments were generated with:
```
minimap2 -eqx -ax map-ont -t 32 -N 100 input/nanosim_drna/reference/transcripts.fa input/nanosim_drna/dataset/human/drna/human_NA12878_dRNA_Bham1_guppy_reads.fastq.gz | samtools view -@8 -
h -F2052 -bS > results/nanosim_drna/alignments/aln_T_filtered.bam
```

oarfish 0.4 (with directional filtering) was run as:

```
oarfish --three-prime-clip 4294967295 --five-prime-clip 4294967295 \
  --score-threshold 0.0 --min-aligned-fraction 0.0 --min-aligned-len 1 \
  --alignments results/nanosim_drna/alignments/aln_T_filtered.bam --threads 32 \
  --output results/nanosim_drna/filtered_oarfish_prev_quant/quant_cov --model-coverage
```

to generate the cov result and as

```
oarfish --three-prime-clip 4294967295 --five-prime-clip 4294967295 \
  --score-threshold 0.0 --min-aligned-fraction 0.0 --min-aligned-len 1 \
  --alignments results/nanosim_drna/alignments/aln_T_filtered.bam --threads 32 \
  --output results/nanosim_drna/filtered_oarfish_prev_quant/quant_no_cov
```

to generate the no_cov result (with directional filtering). These flags replicate the contents of `--filter-group no-filters` but properly filter out alignments to the negative strand of the RNA.

To generate the results without directional filtering, oarfish 0.4 was run as

```
oarfish --alignments results/nanosim_drna/alignments/aln_T_filtered.bam --threads 32 --output results/nanosim_drna/filtered_oarfish_prev_quant/quant_cov_nodir --model-coverage --filter-group no-filters
```

to produce results with the coverage model and no alignment orientation filtering and as 

```
oarfish --alignments results/nanosim_drna/alignments/aln_T_filtered.bam --threads 32 --output results/nanosim_drna/filtered_oarfish_prev_quant/quant_no_cov_nodir --filter-group no-filters
```

to produce results without the coverage model and no orientation filtering.

oarfish 0.5 was run as:

```
oarfish --filter-group no-filters -d fw --alignments results/nanosim_drna/alignments/aln_T_filtered.bam --threads 32 --output results/nanosim_drna/filtered_oarfish_quant/quant_cov --model-coverage
```

to generate the cov result and as 

```
oarfish --filter-group no-filters -d fw --alignments results/nanosim_drna/alignments/aln_T_filtered.bam --threads 32 --output results/nanosim_drna/filtered_oarfish_quant/quant_no_cov
```

to generate the no coverage result.

|                           |   MARD |   Pearson ($\log_{1p}$) |   Kendall-$\tau$ |   Spearman $\rho$ |   CCC |   CCC_non_log |   NRMSE |   NRMSE_std |
|:--------------------------|-------:|------------------------:|-----------------:|------------------:|------:|--------------:|--------:|------------:|
| count_oarfish 0.5 (cov w/dfilt)   |  0.028 |                   0.969 |            0.86  |             0.868 | 0.969 |         0.998 |   2.744 |       0.069 |
| count_oarfish 0.5 (nocov w/dfilt) |  0.03  |                   0.956 |            0.851 |             0.859 | 0.956 |         0.994 |   4.459 |       0.113 |
| count_oarfish 0.5 (cov no/dfilt)   |  0.026 |                   0.969 |            0.856 |             0.864 | 0.969 |         0.998 |   2.78  |       0.068 |
| count_oarfish 0.5 (nocov no/dfilt) |  0.029 |                   0.956 |            0.847 |             0.855 | 0.956 |         0.994 |   4.594 |       0.112 |
| count_oarfish 0.4 (cov w/dfilt)   |  0.068 |                   0.888 |            0.715 |             0.73  | 0.885 |         0.984 |   7.046 |       0.178 |
| count_oarfish 0.4 (nocov w/dfilt) |  0.031 |                   0.952 |            0.849 |             0.858 | 0.952 |         0.992 |   4.815 |       0.122 |
| count_oarfish 0.4 (cov no/dfilt)   |  0.065 |                   0.887 |            0.709 |             0.724 | 0.884 |         0.984 |   7.124 |       0.174 |
| count_oarfish 0.4 (nocov no/dfilt) |  0.029 |                   0.952 |            0.846 |             0.854 | 0.952 |         0.993 |   4.969 |       0.121 |

#### run on a BAM file *without* filtering

Alignments were generated with:
```
minimap2 -eqx -ax map-ont -t 32 -N 100 input/nanosim_drna/reference/transcripts.fa input/nanosim_drna/dataset/human/drna/human_NA12878_dRNA_Bham1_guppy_reads.fastq.gz | samtools view -@8 -
h -bS > results/nanosim_drna/alignments/aln_T.bam
```

all versions of oarfish were run exactly as above, but with the input being `aln_T.bam` rather than `aln_T_filtered.bam`.

|                           |   MARD |   Pearson ($\log_{1p}$) |   Kendall-$\tau$ |   Spearman $\rho$ |   CCC |   CCC_non_log |   NRMSE |   NRMSE_std |
|:--------------------------|-------:|------------------------:|-----------------:|------------------:|------:|--------------:|--------:|------------:|
| count_oarfish 0.5 (cov w/dfilt)   |  0.028 |                   0.969 |            0.86  |             0.868 | 0.969 |         0.998 |   2.744 |       0.069 |
| count_oarfish 0.5 (nocov w/dfilt) |  0.03  |                   0.956 |            0.851 |             0.859 | 0.956 |         0.994 |   4.459 |       0.113 |
| count_oarfish 0.5 (cov no/dfilt)   |  0.026 |                   0.969 |            0.856 |             0.864 | 0.969 |         0.998 |   2.78  |       0.068 |
| count_oarfish 0.5 (nocov no/dfilt) |  0.029 |                   0.956 |            0.847 |             0.855 | 0.956 |         0.994 |   4.594 |       0.112 |
| count_oarfish 0.4 (cov w/dfilt)   |  0.068 |                   0.888 |            0.715 |             0.73  | 0.885 |         0.984 |   7.046 |       0.178 |
| count_oarfish 0.4 (nocov w/dfilt) |  0.031 |                   0.952 |            0.849 |             0.858 | 0.952 |         0.992 |   4.815 |       0.122 |
| count_oarfish 0.4 (cov no/dfilt)   |  0.065 |                   0.887 |            0.709 |             0.724 | 0.884 |         0.984 |   7.124 |       0.174 |
| count_oarfish 0.4 (nocov no/dfilt) |  0.029 |                   0.952 |            0.846 |             0.854 | 0.952 |         0.993 |   4.969 |       0.121 |

This benchmark was developed using the following tools and versions:

| Tool | version |
| -------- | ------- |
| oarfish   | 0.4.0 & 0.5.0 |
| Python    | 3.12.3 |
| R         | 4.3.3  |
| Snakemake | 8.16.0 |
