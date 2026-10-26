"""One shared visual style for notebooks and the Quarto report."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from names_project.data import project_root

# Colour-blind-safe (Okabe-Ito). Sex colours are fixed across the report.
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#000000"]
SEX_COLOURS = {"F": "#CC79A7", "M": "#0072B2"}
SEX_LABELS = {"F": "Recorded female", "M": "Recorded male"}


def set_style() -> None:
    """Apply the project's matplotlib defaults."""
    plt.rcParams.update(
        {
            "figure.figsize": (8, 4.5),
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.titleweight": "bold",
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "legend.frameon": False,
            "axes.prop_cycle": plt.cycler(color=PALETTE),
        }
    )


def plot_trajectories(
    df: pd.DataFrame,
    names: Iterable[str],
    sex: str | None = None,
    value: str = "per_million",
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Line plot of popularity over time for selected names."""
    ax = ax or plt.gca()
    sub = df[df["name"].isin(list(names))]
    if sex is not None:
        sub = sub[sub["sex"] == sex]
    for (name, s), grp in sub.groupby(["name", "sex"], observed=True):
        label = name if sex is not None else f"{name} ({s})"
        ax.plot(grp["year"], grp[value], label=label)
    ax.set_xlabel("Year of birth")
    ax.set_ylabel("Births per million" if value == "per_million" else value)
    ax.legend()
    return ax


def save_figure(fig: plt.Figure, filename: str, directory: Path | None = None) -> Path:
    """Save to ``report/figures`` (created if needed) and return the path."""
    directory = directory or project_root() / "report" / "figures"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    fig.savefig(path)
    return path
