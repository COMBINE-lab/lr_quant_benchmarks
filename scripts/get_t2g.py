import pandas as pd

### t2g code taken from https://github.com/pachterlab/LSRRSRLFKOTWMWMP_2024


def generate_t2g(gtf_file, output_file):
    # Load GTF file
    df = pd.read_csv(
        gtf_file,
        sep="\t",
        comment="#",
        header=None,
        usecols=[0, 2, 8],
        names=["chr", "feature", "attributes"],
    )

    # Filter for 'transcript' feature
    df = df[df["feature"] == "transcript"]

    # Extract transcript ID and gene ID from attributes
    df["transcript_id"] = df["attributes"].str.extract('transcript_id "([^"]+)"')
    df["gene_id"] = df["attributes"].str.extract('gene_id "([^"]+)"')

    # Save to file
    df[["transcript_id", "gene_id"]].dropna().to_csv(
        output_file, sep="\t", index=False, header=False
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="get_t2g")

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    generate_t2g(args.input, args.output)
