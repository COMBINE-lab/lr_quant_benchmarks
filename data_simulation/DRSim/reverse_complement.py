import gzip
from Bio.Seq import Seq

def reverse_complement_fastq_gz(input_path, output_path):
    with gzip.open(input_path, 'rt') as fin, gzip.open(output_path, 'wt') as fout:
        line_num = 0

        while True:
            header = fin.readline()
            line_num += 1
            if not header:
                break  # End of file

            seq = fin.readline()
            plus = fin.readline()
            qual = fin.readline()
            line_num += 3

            if not seq or not plus or not qual:
                raise ValueError(f"File truncated or malformed near line {line_num - 3}")

            if not header.startswith('@'):
                raise ValueError(f"Invalid FASTQ format at line {line_num - 3}: expected '@'")
            if not plus.startswith('+'):
                raise ValueError(f"Invalid FASTQ format at line {line_num - 1}: expected '+'")

            seq = seq.strip()
            qual = qual.strip()
            if len(seq) != len(qual):
                raise ValueError(f"Sequence and quality length mismatch at line {line_num - 3}")

            if "-strand" in header:
                seq = str(Seq(seq).reverse_complement())
                qual = qual[::-1]

            fout.write(f"{header}{seq}\n{plus}{qual}\n")

# 🔽 Main section for command-line execution
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Reverse complement reads on the reverse strand in a gzipped FASTQ file.")
    parser.add_argument("-i", "--input", required=True, help="Input .fastq.gz file")
    parser.add_argument("-o", "--output", required=True, help="Output .fastq.gz file")
    args = parser.parse_args()

    reverse_complement_fastq_gz(args.input, args.output)
