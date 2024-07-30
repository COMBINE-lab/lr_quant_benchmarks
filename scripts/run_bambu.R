library(bambu)

args <- commandArgs(trailingOnly = TRUE)

bam <- args[1]
annot <- args[2]
genome <- args[3]
out <- args[4]

se.quantOnly <- bambu(reads = bam, annotations = annot, genome = genome, discovery = FALSE, verbose = TRUE)
writeBambuOutput(se.quantOnly, path=out)


