#! /nfshomes/zzare/miniconda3/envs/env-lrqnt/bin/Rscript

## Libraries
library(bambu)

## the args part is taken from this link: https://github.com/IARCbioinfo/R-tricks
## Collect arguments
args <- commandArgs(TRUE)

## Parse arguments (we expect the form --arg=value)
parseArgs <- function(x) strsplit(sub("^--", "", x), "=")
argsL <- as.list(as.character(as.data.frame(do.call("rbind", parseArgs(args)))$V2))
names(argsL) <- as.data.frame(do.call("rbind", parseArgs(args)))$V1
args <- argsL
rm(argsL)


## Bambu quantification
bambuAnnotations <- prepareAnnotations(args$annotation)
RcOut1 <- bambu(reads = args$LongRead, ncore=args$ncore, annotations = bambuAnnotations, genome = args$genome, discovery = FALSE)
writeBambuOutput(RcOut1, path = args$output)

q(save = "no")
