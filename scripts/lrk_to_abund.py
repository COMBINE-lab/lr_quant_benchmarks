import pandas as pd
import sys
import numpy as np
from scipy.io import mmread

### lrk to quant code taken from https://github.com/pachterlab/LSRRSRLFKOTWMWMP_2024


def get_lrk_quant(opath):
    count = mmread(f"{opath}/matrix.abundance.mtx")
    labels = pd.read_csv(f"{opath}/transcripts.txt", header=None, sep="\t")
    count_bus = pd.DataFrame(count.todense().T, columns=["bus_counts"])
    count_bus["transcript_id"] = [
        labels.values[i][0] for i in range(np.shape(labels.values)[0])
    ]
    count_bus.index.name = "transcript_id"
    count_bus.to_csv(
        f"{opath}/bus_quant_tcc.tsv",
        sep="\t",
        columns=["transcript_id", "bus_counts"],
        header=1,
        index=0,
    )


if __name__ == "__main__":
    get_lrk_quant(sys.argv[1])
