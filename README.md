[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13130623.svg)](https://doi.org/10.5281/zenodo.13130623)

# A replicable and modular benchmark for long-read RNA quantification methods

This repository provides a Snakemake-based workflow for evaluating the accuracy
of different methods for transcript-level quantification from long-read RNA-seq
data. It accompanies the paper ["A replicable and modular benchmark for long-read transcript quantification methods"](https://www.biorxiv.org/content/10.1101/2024.07.30.605821v1).

At a high-level the organization of the repository is as follows.

The top-level Snakemake files are in the `snakemake_rules` directory, with one sub-directory 
for each of the main simulations.  Each subdirectory has it's own `config.yml` file that specifies
the relevant paths needed to run the rules in that subdirectory, and the `main.snk` file has an 
`all` target that should run everything.

You can put the requisite input data in any place you wish, but it is recommended to place it in 
a directory named `input` at the top-level of this repository.  You can obtain the input using 
the following command (it is 43G compressed and may take a while to download):

```{sh}
wget https://zenodo.org/records/13130623/files/input.tar.zstd?download=1 -O input.tar.zstd
```

and it can then be decompressed with the command

```{sh}
tar --use-compress-program=zstd -xf input.tar.zstd
```

This will create a directory called `input` with the relevant input files for the `Snakemake` rules.

Likewise, make note that the full output for all simulations will take aroun 93GB; we recommend the ouputs
be placed in a directory named `results` at the top level of this repository, but the output directory 
is configurable via the `config.yml` files.

The `snakemake_rules` directory has a subdirectory for each of the different simulations.  The main simulations
corresponding to the paper are `isoquant_sim_data` and `transigner_sim_data`. Each directory contains a
`config.yml` file that you will need to fill in with the appropriate directories and tool paths, and a `main.snk`
file that has an `all` rule to run all of the quantification tools.

## Additional data

The directory `snakemake_rules/nanosim_NA12878_dRNA__guppy` contains the rules
for processing a simulated dataset of ONT directRNA data as the
`isoquant_sim_data` and `transigner_sim_data` directories above have for their
respective data, as well as a `config.yml` that will also need to be
appropriately filled in. The simulated data is originally obtained from
[https://zenodo.org/records/11201284](https://zenodo.org/records/11201284),
uploaded by Loving et al. You can obtain the simulated reads as well as all of
the other necessary input files like the reference transcriptome and ground
truth counts can be obtained from [this link](https://umd.box.com/shared/static/0kibdjw9yohkbw3xi92fgcr112xsuseg.zstd).

Specfically, you can obtain the data with the command:

```{sh}
$ wget  -O nanosim_NA12878_dRNA__guppy.tar.zstd https://umd.box.com/shared/static/0kibdjw9yohkbw3xi92fgcr112xsuseg.zstd
```

you can then decompress it in the top-level input directory as follows

```{sh}
$ mkdir -p input
$ tar --use-compress-program=zstd nanosim_NA12878_dRNA__guppy.tar.zstd -C input
```

_Note_: Currently this additional dataset only runs the `oarfish` and `NanoCount` quantifiers.

### Program versions and information

This benchmark was developed using the following tools and versions:

| Tool | version |
| -------- | ------- |
| bambu     | 3.4.1  |
| bustools  | 0.43.2 |
| kallisto  | 0.51.0 |
| NanoCount | 1.1.0  |
| oarfish   | 0.4.0 & 0.5.0 |
| Python    | 3.12.3 |
| R         | 4.3.3  |
| Snakemake | 8.16.0 |


#### Conda installation

You can install the latest versions of the requirements via e.g.

```sh
micromamba create -f environment.yml
micromamba activate lr_quant_benchmark
```
