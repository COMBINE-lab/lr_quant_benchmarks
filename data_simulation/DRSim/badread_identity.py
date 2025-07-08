import collections
import re
import sys
import math
import argparse
import gzip  # Import gzip for handling compressed files

class Alignment(object):
    def __init__(self, paf_line):
        line_parts = paf_line.strip().split('\t')
        if len(line_parts) < 11:
            sys.exit('Error: alignment file does not seem to be in PAF format')

        self.read_name = line_parts[0]
        self.read_start = int(line_parts[2])
        self.read_end = int(line_parts[3])
        self.strand = line_parts[4]

        self.ref_name = line_parts[5]
        self.ref_start = int(line_parts[7])
        self.ref_end = int(line_parts[8])

        self.matching_bases = int(line_parts[9])
        self.num_bases = int(line_parts[10])
        self.percent_identity = 100.0 * self.matching_bases / self.num_bases

        self.cigar, self.alignment_score = None, None
        for part in line_parts:
            if part.startswith('cg:Z:'):
                self.cigar = part[5:]
            if part.startswith('AS:i:'):
                self.alignment_score = int(part[5:])
        if self.cigar is None:
            sys.exit('Error: no CIGAR string found')
        if self.alignment_score is None:
            sys.exit('Error: no alignment score')

def get_open_func(filename):
    # Return gzip.open if the file extension is .gz, else return open
    if filename.endswith('.gz'):
        return gzip.open
    else:
        return open

def load_alignments(filename, output=sys.stderr):
    print('Loading alignments', end='', file=output, flush=True)
    all_alignments = collections.defaultdict(list)
    with get_open_func(filename)(filename, 'rt') as paf_file:
        for line in paf_file:
            a = Alignment(line)
            all_alignments[a.read_name].append(a)

    print('Choosing best alignment per read', end='', file=output, flush=True)
    best_alignments = []
    for read_name, alignments in all_alignments.items():
        best = sorted(alignments, key=lambda x: x.alignment_score)[-1]
        if best.num_bases > 100 and best.percent_identity > 80.0:
            best_alignments.append(best)

    return best_alignments

def calculate_beta_distribution_params(identities):
    mean_identity = sum(identities) / len(identities)
    variance = sum((x - mean_identity) ** 2 for x in identities) / len(identities)
    stddev = math.sqrt(variance)
    m = max(identities)
    #alpha = ((1 - (mean_identity / m)) / ((stddev / m) ** 2) - (m / mean_identity)) * ((mean_identity / m) ** 2)
    #beta = alpha * (m / mean_identity - 1)
    return mean_identity, m, stddev

def main():
    parser = argparse.ArgumentParser(description="Process a PAF file and calculate beta distribution parameters for read identities.")
    parser.add_argument("paf_file", help="Path to the input PAF file (can be .paf or .paf.gz)")
    args = parser.parse_args()

    best_alignments = load_alignments(args.paf_file)
    identities = [min(alignment.percent_identity, 100.0) for alignment in best_alignments]

    if identities:
        mean, max, stddev = calculate_beta_distribution_params(identities)
        print(f"mean: {mean:.2f}, max: {max:.2f}, stddev: {stddev:.2f}")
    else:
        print("No valid alignments found.")

if __name__ == "__main__":
    main()
