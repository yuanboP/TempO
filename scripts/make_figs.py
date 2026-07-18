#!/usr/bin/env python3
"""Generate the paper figures from data/fig_data.json."""

import json
import math
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "fig_data.json"
OUT_DIR = ROOT / "paper" / "figs"

BG = "#fcfcfb"
TEXT = "#52514e"
SPINE = "#c3c2b7"
GRID = "#e1e0d9"
BLUE = "#2a78d6"
RED = "#e34948"
PURPLE = "#4a3aa7"
HARNESS_COLORS = {
    "Terminus 2": BLUE,
    "Claude Code": "#1baf7a",
    "Gemini CLI": "#eda100",
}


def apply_style(ax, axis="x"):
    """Apply the shared ICLR-friendly visual style to an axes."""
    ax.set_facecolor(BG)
    ax.figure.set_facecolor(BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color(SPINE)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(axis="both", colors=SPINE, labelcolor=TEXT, labelsize=9,
                   width=0.8, length=3)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.xaxis.label.set_size(9)
    ax.yaxis.label.set_size(9)
    ax.set_axisbelow(True)
    if axis:
        ax.grid(axis=axis, color=GRID, linewidth=0.6)


def empirical_quantile(values, q):
    """Nearest-rank empirical quantile."""
    ordered = sorted(values)
    return ordered[max(0, math.ceil(q * len(ordered)) - 1)]


def save_figure(fig, stem, written):
    for suffix, kwargs in (("pdf", {}), ("png", {"dpi": 200})):
        path = OUT_DIR / f"{stem}.{suffix}"
        fig.savefig(path, facecolor=BG, bbox_inches="tight", **kwargs)
        written.append(path)
    plt.close(fig)


def make_cdf(records, written):
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    apply_style(ax, axis="both")

    for name, color in HARNESS_COLORS.items():
        values = sorted(float(r["waste_frac"]) for r in records
                        if r["harness"] == name)
        n = len(values)
        y = [(i + 1) / n for i in range(n)]
        label = f"{name} (n={n})"
        ax.step(values, y, where="post", color=color, linewidth=2, label=label)

        p90 = empirical_quantile(values, 0.90)
        ax.vlines(p90, 0, 0.90, color=color, linewidth=0.8,
                  linestyle=(0, (1.5, 2.2)), alpha=0.65)
        ax.annotate("p90", xy=(p90, 0), xytext=(0, 4),
                    textcoords="offset points", ha="center", va="bottom",
                    color=color, fontsize=7, clip_on=True)

        # Label the visible right-hand portion, with small vertical separation.
        x_label = min(values[-1], 0.765)
        y_label = sum(v <= x_label for v in values) / n
        offsets = {"Terminus 2": -11, "Claude Code": 9, "Gemini CLI": -1}
        ax.annotate(label, xy=(x_label, y_label), xytext=(-4, offsets[name]),
                    textcoords="offset points", ha="right", va="center",
                    color=color, fontsize=8)

    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 1.015)
    ax.set_xlabel("fraction of wall-clock wasted (W1-W5)")
    ax.set_ylabel("fraction of trials")
    ax.legend(frameon=False, fontsize=7.5, loc="lower right",
              handlelength=2.2, labelcolor=TEXT)
    fig.tight_layout()
    save_figure(fig, "fig_cdf", written)


def make_failed_waste(records, written):
    grouped = {}
    for r in records:
        if r["harness"] == "Terminus 2" and int(r["reward"]) == 0:
            grouped.setdefault(r["model"], []).append(float(r["waste_frac"]))
    values = sorted(((model, statistics.median(xs))
                     for model, xs in grouped.items()),
                    key=lambda item: item[1], reverse=True)

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    apply_style(ax, axis="x")
    models = [x[0] for x in values]
    medians = [x[1] for x in values]
    colors = [RED if i < 2 else BLUE for i in range(len(values))]
    bars = ax.barh(models, medians, height=0.55, color=colors)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("median fraction wasted among failed trials")
    ax.margins(x=0.13)
    for bar, value in zip(bars, medians):
        ax.text(value + 0.007, bar.get_y() + bar.get_height() / 2,
                f"{value:.1%}", va="center", ha="left",
                color="#0b0b0b", fontsize=8.5)
    fig.tight_layout()
    save_figure(fig, "fig_failedwaste", written)


def make_prevalence(records, written):
    labels = {
        "w1": "W1 repeat-slow",
        "w2": "W2 over-wait",
        "w3": "W3 under-wait churn",
        "w4": "W4 same-error retry",
        "w5": "W5 redundant env setup",
    }
    n = len(records)
    values = [(key, label, sum(float(r[key]) >= 1 for r in records) / n)
              for key, label in labels.items()]
    values.sort(key=lambda item: item[2], reverse=True)

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    apply_style(ax, axis="x")
    names = [x[1] for x in values]
    shares = [x[2] for x in values]
    colors = [BLUE if x[0] in {"w2", "w3"} else PURPLE for x in values]
    bars = ax.barh(names, shares, height=0.55, color=colors)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("share of all trials with at least one finding")
    ax.margins(x=0.13)
    for bar, value in zip(bars, shares):
        ax.text(value + 0.007, bar.get_y() + bar.get_height() / 2,
                f"{value:.1%}", va="center", ha="left",
                color="#0b0b0b", fontsize=8.5)
    handles = [
        Line2D([0], [0], color=BLUE, linewidth=6,
               label="mechanical (harness-induced)"),
        Line2D([0], [0], color=PURPLE, linewidth=6, label="semantic"),
    ]
    ax.legend(handles=handles, frameon=False, fontsize=8, loc="lower right",
              labelcolor=TEXT, handlelength=1.4)
    fig.tight_layout()
    save_figure(fig, "fig_prevalence", written)


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titleweight": "normal",
        "savefig.facecolor": BG,
        "figure.facecolor": BG,
    })
    with DATA_PATH.open(encoding="utf-8") as f:
        records = json.load(f)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    make_cdf(records, written)
    make_failed_waste(records, written)
    make_prevalence(records, written)
    print("Files written:")
    for path in written:
        print(f"{path.relative_to(ROOT)}\t{path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
