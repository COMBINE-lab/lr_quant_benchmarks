#!/usr/bin/env python

import pandas as pd
import numpy as np
import scipy.stats as st
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from DensityPlot.plot import density2d


def load_lrk(f):
    x = pd.read_csv(f, sep="\t")
    x["tid"] = x.transcript_id.str.split(".").str.get(0)
    x["count_kallisto"] = x["bus_counts"]
    x = x.drop(["transcript_id"], axis=1)
    return x


def load_transigner(f):
    x = pd.read_csv(f, sep="\t", names=["transcript_name", "tpm_ts", "count_ts"])
    x["tid"] = x.transcript_name.str.split(".").str.get(0)
    x["count_transigner"] = x["count_ts"]
    x = x.drop(["transcript_name"], axis=1)
    return x


def load_nanocount(f, k):
    x = pd.read_csv(f, sep="\t")
    x["tid"] = x.transcript_name.str.split(".").str.get(0)
    x[f"count_{k}"] = x["est_count"]
    x = x.drop(
        ["transcript_name", "raw", "est_count", "tpm", "transcript_length"], axis=1
    )
    return x


def load_oarfish(f, k):
    x = pd.read_csv(f, sep="\t")
    x["tid"] = x.tname.str.split(".").str.get(0)
    x[f"count_{k}"] = x["num_reads"]
    x = x.drop(["tname", "len", "num_reads"], axis=1)
    return x


def load_bambu(f):
    x = pd.read_csv(f, sep="\t", skiprows=1, names=["TXNAME", "GNAME", "COUNT"])
    x = x.drop("GNAME", axis=1)
    x["tname"] = x.TXNAME.str.split(".").str.get(0)
    z = x.groupby(["tname"]).sum()
    z["tid"] = z.index
    z["count_bambu"] = z["COUNT"]
    z = z.drop(["TXNAME", "COUNT"], axis=1)
    return z


def load_truth(f):
    x = pd.read_csv(f, sep=r"\s+", names=["tid", "count_true"])
    return x


def get_mard_table(m, true_key, pred_counts):
    res = {}
    x = m.loc[:, true_key]
    for n in pred_counts:
        y = m.loc[:, n]
        r = (np.abs(x - y) / np.abs(x + y)).fillna(0)
        res[n] = r.mean()
    return pd.DataFrame.from_dict(res, orient="index", columns=["MARD"])


def get_nrmse_table(m, true_key, pred_counts, norm="mean"):
    f = None
    if norm == "mean":
        def f(z): return np.mean(z)
    elif norm == "std":
        def f(z): return np.std(z)
    else:
        print(f"don't know norm method {norm}")
        exit(1)
    res = {}
    x = m.loc[:, true_key]
    for n in pred_counts:
        y = m.loc[:, n]
        rmse = np.sqrt(mean_squared_error(x, y))
        mean_observed = f(x)
        res[n] = rmse / mean_observed
    return pd.DataFrame.from_dict(res, orient="index", columns=["NRMSE"])


def get_ccc_table(m, true_key, pred_counts, use_log=True):
    f = None
    if use_log:
        def f(z): return np.log1p(z)
    else:
        def f(z): return z

    ccc_correlation = {}
    pearson_table = f(m.drop(["tid"], axis=1)).corr(method="pearson").loc[:, true_key]
    y_true = f(m.loc[:, true_key])
    for column_name in pred_counts:
        y_pred = f(m.loc[:, column_name])
        # obtain the mean value
        mean_true = np.mean(y_true)
        mean_pred = np.mean(y_pred)
        # obtain the standard deviation
        std_true = np.std(y_true)
        std_pred = np.std(y_pred)
        ccc_correlation[column_name] = (
            2 * pearson_table[column_name] * std_true * std_pred
        ) / (std_true**2 + std_pred**2 + (mean_true - mean_pred) ** 2)
    return pd.DataFrame.from_dict(ccc_correlation, orient="index", columns=["CCC"])


def main(args):
    pd.options.display.float_format = "{:.3f}".format
    pd.set_option("display.precision", 3)

    t = load_truth(args.truth)
    meth_d = {}
    for k, v in args.__dict__.items():
        if v is None:
            continue
        if k == "oarfish":
            k = "oarfish 0.5 (cov)"
            meth_d[k] = load_oarfish(v, k)
        elif k == "oarfish_prev":
            k = "oarfish 0.4 (cov)"
            meth_d[k] = load_oarfish(v, k)
        elif k == "oarfish_nocov":
            k = "oarfish 0.5 (nocov)"
            meth_d[k] = load_oarfish(v, k)
        elif k == "oarfish_prev_nocov":
            k = "oarfish 0.4 (nocov)"
            meth_d[k] = load_oarfish(v, k)
        elif k == "nanocount":
            meth_d[k] = load_nanocount(v, k)
        elif k == "nanocount_nofilt":
            k = "nanocount (nofilt)"
            meth_d[k] = load_nanocount(v, k)
        elif k == "bambu":
            meth_d[k] = load_bambu(v)
        elif k == "kallisto":
            meth_d[k] = load_lrk(v)
        elif k == "transigner":
            meth_d[k] = load_transigner(v)
        else:
            pass

    if "bambu" in meth_d:
        b = None
        for other in [
            "nanocount",
            "nanocount (nofilt)",
            "oarfish 0.5 (cov)",
            "oarfish 0.5 (nocov)",
            "oarfish 0.4 (cov)",
            "oarfish 0.4 (nocov)",
            "kallisto",
            "transigner",
        ]:
            if other in meth_d:
                b = meth_d[other]
                break
        if b is None:
            print(
                "Must evaluate at least one other method along with bambu to elimiate extra annotations from the base set"
            )
        else:
            x = meth_d["bambu"]
            meth_d["bambu"] = x.loc[x["tid"].isin(b["tid"]), :]

    # true_nnz = t.loc[t.count_true > 0, :].shape[0]
    # print(f"There are {true_nnz} true transcripts with abundance > 0")

    plt.rc("font", size=8)
    plt.rc("axes", labelsize=8)
    from pathlib import Path

    outdir = args.out
    Path(outdir).mkdir(parents=True, exist_ok=True)

    ms = {}
    for join_strategy in ["outer"]:
        m = t.copy()
        for x, name in [(v, k) for k, v in meth_d.items()]:
            m = pd.merge(m, x, left_on="tid", right_on="tid", how=join_strategy).fillna(
                0
            )
            fig, ax = density2d(
                x=np.log1p(m.loc[:, "count_true"].values),
                y=np.log1p(m.loc[:, f"count_{name}"].values),
                xlabel="$\\log($ True Count + 1 $)$",
                ylabel=f"$\\log($ {name} Count + 1 $)$",
                cmap="jet",
                logz=True,
                smooth=True,
                figsize=(4, 3),
                alpha=1.0,
                bins=1000,
                mode="scatter",
                s=3,
                colorbar=True,
            )
            spearman_res = st.spearmanr(
                m.loc[:, "count_true"].values, m.loc[:, f"count_{name}"].values
            )
            spearman_r = spearman_res.correlation
            text_str = f"Spearman's $\\rho$ = {spearman_r:.3f}"
            ax.text(2.0, 12.0, text_str, size=5, backgroundcolor="none")
            plt.tight_layout()
            plt.savefig(f"{outdir}/scatter_{join_strategy}_{name}.pdf")
            plt.clf()
            plt.cla()
        ms[join_strategy] = m

    for join_strategy, m in ms.items():
        # print(f"\n\njoin strategy = {join_strategy}")
        # print(f"\nThere were {m.shape[0]} transcripts in the unfiltered annotation\n")
        pred_array = [f"count_{k}" for k in meth_d.keys()]
        key_array = ["count_true"] + pred_array
        print("computing Spearman correlations")
        spearman_table = m[key_array].corr(method="spearman").loc[:, "count_true"]
        # print(spearman_table.round(decimals=3).to_latex())

        print("computing Kendall-Tau correlations")
        kendall_table = m[key_array].corr(method="kendall").loc[:, "count_true"]
        # print(kendall_table.round(decimals=3).to_latex())

        print("computing Pearson correlations (of log1p)")
        pearson_table = (
            np.log1p(m[key_array]).corr(method="pearson").loc[:, "count_true"]
        )
        # print(pearson_table.round(decimals=3).to_latex())
        # print("\n")

        print("computing MARDs")
        mard_table = get_mard_table(m, "count_true", pred_array)
        # print(mard_table.round(decimals=3).to_latex())
        # print("\n")

        print("computing CCC")
        ccc_table = get_ccc_table(m, "count_true", pred_array)
        # print(ccc_table.round(decimals=3).to_latex())
        # print("\n")

        ccc_table_non_log = get_ccc_table(m, "count_true", pred_array, use_log=False)

        nrmse_table = get_nrmse_table(m, "count_true", pred_array)
        nrmse_table_std = get_nrmse_table(m, "count_true", pred_array, norm="std")
        res_table = pd.concat(
            [
                mard_table,
                pearson_table,
                kendall_table,
                spearman_table,
                ccc_table,
                ccc_table_non_log,
                nrmse_table,
                nrmse_table_std,
            ],
            axis=1,
        )
        res_table = res_table.set_axis(
            [
                "MARD",
                "Pearson ($\\log_{1p}$)",
                "Kendall-$\\tau$",
                "Spearman $\\rho$",
                "CCC",
                "CCC_non_log",
                "NRMSE",
                "NRMSE_std",
            ],
            axis=1,
        ).drop(["count_true"], axis=0)
        # print(res_table.round(decimals=3).to_latex(float_format="{:0.3f}".format))

        print(res_table.round(decimals=3).to_markdown())

        print("\n")
        print(
            f"number of mapped reads\n========\n{100.0 * m.loc[:, key_array].sum() / m.loc[:, 'count_true'].sum()}"
        )
        print("\n")

        # for name in meth_d.keys():
        #    key = f"count_{name}"
        #    pred = m.loc[:, key]
        #    true = [1 if x > 0 else -1 for x in m.loc[:, "count_true"].values]
        #    PrecisionRecallDisplay.from_predictions(true, pred)
        #    plt.savefig(f"{outdir}/pr_curve_{join_strategy}_{name}.pdf")
        #    plt.cla()
        #    plt.clf()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="eval")

    parser.add_argument("--truth", required=True)
    parser.add_argument("--oarfish")
    parser.add_argument("--oarfish-nocov")
    parser.add_argument("--oarfish-prev")
    parser.add_argument("--oarfish-prev-nocov")
    parser.add_argument("--nanocount")
    parser.add_argument("--nanocount-nofilt")
    parser.add_argument("--bambu")
    parser.add_argument("--transigner")
    parser.add_argument("--kallisto")
    parser.add_argument("--out", required=True)

    args = parser.parse_args()
    main(args)
