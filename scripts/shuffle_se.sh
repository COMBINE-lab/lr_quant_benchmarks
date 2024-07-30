#!/bin/sh

#from https://gist.githubusercontent.com/iam28th/49a245427ea2b8ed5f1f9889c13468bf/raw/1e9c7b503335543977b59236309bba69219c8ac0/shuf_se.sh
#

# Usage: ./shuf_se.sh <reads1>
# The output file 1_shuffled.fastq contains shuffled reads.

# For shuffling PE reads:
# https://gist.github.com/iam28th/418dc7d5048067af194a76ffb5840c90

input="$1"
output="$2"

awk '{

# read 4 lines
lines[1] = $0;
for (i = 2; i <= 4; ++i)
    getline lines[i];

# and print them tab-separated on a single line
for (i = 1; i <= 4; ++i)
    printf("%s%s", lines[i], i == 4 ? "'"\n"'" : "'"\t"'")
}' "$input" | \

# shuffle
shuf | \

# replace all tabs back to newlines
tr '\t' '\n' | gzip -c > $2

