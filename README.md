# A replicable and modular benchmark for long-read RNA quantification methods

This repository provides a Snakemake-based workflow for evaluating the accuracy of 
different methods for transcript-level quantification from long-read RNA-seq data.

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

This benchmark was developed using the following tools and versions:

| Tool | version |
| -------- | ------- |
| Python    | 3.12.3 |
| Snakemake | 8.16.0 |
| NanoCount | 1.1.0  |
| R         | 4.3.3  |
| oarfish   | 0.4.0 & 0.5.0 |
| kallisto  | 0.51.0 |
| bustools  | 0.43.2 |
