from __future__ import annotations

import os
import textwrap
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.ticker import MultipleLocator, MaxNLocator

INPUT_FILE = Path("results/benchmark_results.csv")
OUTPUT_FOLDER = Path("results/plots")
PDF_REPORT = Path("results/sorting_graph_report.pdf")
CROSSOVER_FILE = Path("results/crossover_summary.csv")

MINIMUM_CROSSOVER_SIZE = 2
CONSECUTIVE_REQUIRED = 5

DATA_TYPE_ORDER = [
    "random",
    "sorted",
    "reverse",
    "duplicates",
    "nearly_sorted",
    "all_equal",
    "few_unique",
]

ALGORITHM_ORDER = [
    "insertion_sort",
    "selection_sort",
    "merge_sort",
]

COLORS = {
    "background": "#F5F7FB",
    "navy": "#0F172A",
    "text": "#111827",
    "muted": "#667085",
    "border": "#E5E7EB",
    "card": "#FFFFFF",
    "grid": "#DDE3EC",
    "insertion_sort": "#D95F02",
    "selection_sort": "#7570B3",
    "merge_sort": "#1B9E77",
    "crossover": "#64748B",
    "accent": "#1B9E77",
}

MARKERS = { #These are the markers that will be used for each algorithm in the plots. The markers are chosen to be distinct and easily recognizable, so that the different algorithms can be easily distinguished in the plots. The markers are also chosen to be visually appealing and to complement the color scheme of the plots.
    "insertion_sort": "o",
    "selection_sort": "^",
    "merge_sort": "s",
}

CROSSOVER_COMPARISONS = [
    ("insertion_sort", "merge_sort", "Insertion vs Merge"),
    ("selection_sort", "merge_sort", "Selection vs Merge"),
]


def setup_style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "figure.facecolor": COLORS["background"],
        "axes.facecolor": COLORS["card"],
        "axes.edgecolor": "#CBD5E1",
        "axes.labelcolor": COLORS["text"],
        "xtick.color": "#334155",
        "ytick.color": "#334155",
        "text.color": COLORS["text"],
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "legend.fontsize": 8.5,
        "legend.frameon": True, #this means that the legend will have a frame around it. This is to ensure that the legend is easily readable and stands out against the background of the plot. The frame also helps to create a clean and professional look for the plot.
        "legend.facecolor": "white",#this means that the legend will have a white background. This is to ensure that the legend is easily readable and stands out against the background of the plot. The white background also helps to create a clean and professional look for the plot.
        "legend.edgecolor": COLORS["border"], #this means that the legend will have a border color that matches the border color of the plot. This is to ensure that the legend is easily readable and stands out against the background of the plot. The matching border color also helps to create a clean and professional look for the plot.
    })


def clean_column_name(name: str) -> str:
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")#this function is to clean the column names of the dataframe. It takes in a string name and returns a cleaned version of the name. The cleaning process involves stripping any leading or trailing whitespace, converting the name to lowercase, replacing spaces with underscores, and replacing hyphens with underscores. This is done to ensure that the column names are consistent and easy to work with in the code.


def find_column(df: pd.DataFrame, candidates: list[str], required_name: str) -> str:
    for candidate in candidates:#this function is to find the column name in the dataframe that matches one of the candidates. It takes in a dataframe df, a list of candidate column names, and a required name. It iterates through the list of candidates and checks if each candidate is present in the dataframe's columns. If a match is found, it returns the candidate column name. If no match is found after checking all candidates, it raises a ValueError indicating that no valid column was found and lists the available columns in the dataframe. This function is useful for ensuring that the code can work with different variations of column names in the input data.
        if candidate in df.columns:
            return candidate
    raise ValueError(f"Could not find a {required_name} column. Available columns are: {list(df.columns)}")


def time_to_ms(df: pd.DataFrame, time_col: str) -> pd.Series:
    values = pd.to_numeric(df[time_col], errors="coerce") 
    col = time_col.lower()

    if "nanosecond" in col or col.endswith("_ns") or col == "ns":
        return values / 1_000_000 #we do 1_000_000 because there are 1,000,000 nanoseconds in a millisecond. This is to convert the time values from nanoseconds to milliseconds, which is a more standard unit of time for measuring the performance of algorithms. By converting the time values to milliseconds, we can more easily compare the performance of different algorithms and visualize the results in the plots.
    if "microsecond" in col or col.endswith("_us") or col == "us":
        return values / 1_000
    if "millisecond" in col or col.endswith("_ms") or col == "ms" or "time_ms" in col:
        return values
    if "second" in col or col.endswith("_sec") or col.endswith("_s"):
        return values * 1000

    return values * 1000


def normalize_algorithm_name(name: str) -> str:
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def load_results(input_file: Path = INPUT_FILE) -> pd.DataFrame:
    if not input_file.exists():
        raise FileNotFoundError(f"Could not find {input_file}. Run the benchmark script first.")

    raw = pd.read_csv(input_file)
    raw = raw.rename(columns={column: clean_column_name(column) for column in raw.columns})

    data_type_col = find_column(raw, ["data_type", "input_type", "distribution", "case", "test_case", "dataset"], "data type")
    size_col = find_column(raw, ["size", "n", "input_size", "array_size", "list_size", "length"], "input size")
    algorithm_col = find_column(raw, ["algorithm", "sort", "sort_name", "method", "algorithm_name"], "algorithm")
    time_col = find_column(
        raw,
        [
            "average_time_seconds",
            "avg_time_seconds",
            "mean_time_seconds",
            "time_seconds",
            "runtime_seconds",
            "duration_seconds",
            "execution_time_seconds",
            "elapsed_seconds",
            "average_time_ms",
            "avg_time_ms",
            "mean_time_ms",
            "time_ms",
            "runtime_ms",
            "duration_ms",
            "execution_time_ms",
            "elapsed_ms",
            "time",
            "runtime",
            "duration",
            "execution_time",
            "elapsed_time",
            "time_taken",
        ],
        "time",
    )

    df = pd.DataFrame({
        "data_type": raw[data_type_col].astype(str).str.strip().str.lower(),
        "size": pd.to_numeric(raw[size_col], errors="coerce"),
        "algorithm": raw[algorithm_col].map(normalize_algorithm_name),
        "average_time_ms": time_to_ms(raw, time_col),
    })

    df = df.dropna(subset=["data_type", "size", "algorithm", "average_time_ms"])
    df["size"] = df["size"].astype(int)
    df = df[(df["size"] >= 0) & (df["average_time_ms"] >= 0)]

    if df.empty:
        raise ValueError("The benchmark CSV loaded, but no valid benchmark rows were found.")

    return df


def aggregate_results(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["data_type", "size", "algorithm"], as_index=False)
        .agg(
            average_time_ms=("average_time_ms", "mean"),
            runs=("average_time_ms", "count"),
        )
        .sort_values(["data_type", "algorithm", "size"])
    )


def pretty_algorithm_name(name: str) -> str:
    custom = {
        "insertion_sort": "Insertion Sort",
        "selection_sort": "Selection Sort",
        "merge_sort": "Merge Sort",
    }
    return custom.get(name, " ".join(part.capitalize() for part in str(name).replace("_", " ").split()))


def pretty_data_type(name: str) -> str:
    return " ".join(part.capitalize() for part in str(name).replace("_", " ").split())


def algorithm_sort_key(name: str) -> tuple[int, str]:
    try:
        return (ALGORITHM_ORDER.index(name), name)
    except ValueError:
        return (len(ALGORITHM_ORDER), name)


def data_type_sort_key(name: str) -> tuple[int, str]:
    try:
        return (DATA_TYPE_ORDER.index(name), name)
    except ValueError:
        return (len(DATA_TYPE_ORDER), name)


def find_stable_crossover(
    data_for_type: pd.DataFrame,
    slower_algorithm: str,
    faster_algorithm: str,
    minimum_size: int = MINIMUM_CROSSOVER_SIZE,
    consecutive_required: int = CONSECUTIVE_REQUIRED,
) -> Optional[int]:
    slower = data_for_type[data_for_type["algorithm"] == slower_algorithm]
    faster = data_for_type[data_for_type["algorithm"] == faster_algorithm]

    if slower.empty or faster.empty:
        return None

    combined = slower.merge(faster, on=["data_type", "size"], suffixes=("_slow", "_fast")).sort_values("size")

    if combined.empty:
        return None

    for i in range(len(combined) - consecutive_required + 1):
        current_rows = combined.iloc[i:i + consecutive_required]
        first_size = int(current_rows.iloc[0]["size"])

        if first_size < minimum_size:
            continue

        faster_every_time = all(current_rows["average_time_ms_fast"] < current_rows["average_time_ms_slow"])

        if faster_every_time:
            return first_size

    return None


def compute_crossover_summary(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for data_type in sorted(summary["data_type"].unique(), key=data_type_sort_key):
        data_for_type = summary[summary["data_type"] == data_type]
        row = {"data_type": data_type}

        for slower, faster, label in CROSSOVER_COMPARISONS:
            row[label.lower().replace(" ", "_")] = find_stable_crossover(data_for_type, slower, faster)

        rows.append(row)

    return pd.DataFrame(rows)


def add_card(fig: plt.Figure, x: float, y: float, w: float, h: float, radius: float = 0.012) -> None:
    fig.add_artist(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle=f"round,pad=0.012,rounding_size={radius}",
            transform=fig.transFigure,
            linewidth=1,
            edgecolor=COLORS["border"],
            facecolor=COLORS["card"],
            zorder=-1,
        )
    )


def add_footer(fig: plt.Figure, page: int) -> None:
    fig.text(0.055, 0.035, "Source: results/benchmark_results.csv", fontsize=8, color=COLORS["muted"])
    fig.text(0.945, 0.035, f"Page {page}", fontsize=8, color=COLORS["muted"], ha="right")


def add_page_title(fig: plt.Figure, title: str, subtitle: str = "") -> None:
    fig.text(0.06, 0.84, title, fontsize=21.5, weight="bold", color=COLORS["navy"])
    if subtitle:
        fig.text(0.06, 0.795, subtitle, fontsize=11.8, color=COLORS["muted"])


def draw_runtime_chart(ax: plt.Axes, summary: pd.DataFrame, data_type: str, crossovers: dict[str, Optional[int]]) -> None:
    data_for_type = summary[summary["data_type"] == data_type]
    algorithms = sorted(data_for_type["algorithm"].unique(), key=algorithm_sort_key)

    for algorithm in algorithms:
        algorithm_data = data_for_type[data_for_type["algorithm"] == algorithm].sort_values("size")
        ax.plot(
            algorithm_data["size"],
            algorithm_data["average_time_ms"],
            label=pretty_algorithm_name(algorithm),
            color=COLORS.get(algorithm, "#2563EB"),
            marker=MARKERS.get(algorithm, "o"),
            markersize=2.8,
            markevery=max(1, len(algorithm_data) // 18),
            linewidth=2,
        )

    used_x = []
    for crossover in crossovers.values():
        if crossover is None or pd.isna(crossover):
            continue

        x = float(crossover)
        offset_count = sum(abs(x - old_x) < 4 for old_x in used_x)
        used_x.append(x)
        ax.axvline(x + offset_count * 2.5, color=COLORS["crossover"], linestyle="--", linewidth=1.2, alpha=0.7)

    max_size = int(data_for_type["size"].max())
    ax.set_xlim(0, max_size)
    ax.set_title(f"{pretty_data_type(data_type)} data", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Input size (n)", labelpad=8)
    ax.set_ylabel("Average time (ms)", labelpad=8)
    ax.grid(True, which="major", color=COLORS["grid"], linewidth=0.8)
    ax.grid(True, which="minor", color=COLORS["grid"], linewidth=0.35, alpha=0.45)
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", framealpha=0.95)


def save_individual_plot(summary: pd.DataFrame, data_type: str, crossovers: dict[str, Optional[int]]) -> Path:
    fig, ax = plt.subplots(figsize=(10.5, 6.2), facecolor="white")
    draw_runtime_chart(ax, summary, data_type, crossovers)
    fig.tight_layout(pad=2)

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_FOLDER / f"{data_type}_results.png"
    fig.savefig(path, dpi=220, facecolor="white")
    plt.close(fig)
    return path


def fastest_at_largest_n(summary: pd.DataFrame, data_type: str) -> tuple[str, int]:
    data_for_type = summary[summary["data_type"] == data_type]
    largest_n = int(data_for_type["size"].max())
    largest_rows = data_for_type[data_for_type["size"] == largest_n]
    fastest_row = largest_rows.loc[largest_rows["average_time_ms"].idxmin()]
    return pretty_algorithm_name(str(fastest_row["algorithm"])), largest_n


def crossover_text(value: object) -> str:
    if pd.isna(value):
        return "No stable crossover"
    return f"n = {int(value)}"


def create_cover_page(pdf: PdfPages, df: pd.DataFrame, page: int) -> None:
    fig = plt.figure(figsize=(11, 8.5), facecolor=COLORS["background"])

    fig.add_artist(Rectangle((0, 0.69), 1, 0.31, transform=fig.transFigure, color=COLORS["navy"], zorder=-2))
    fig.add_artist(Rectangle((0, 0.67), 1, 0.02, transform=fig.transFigure, color=COLORS["accent"], zorder=-1))

    fig.text(0.065, 0.835, "Sorting Algorithm", fontsize=28, weight="bold", color="white")
    fig.text(0.065, 0.78, "Benchmark Report", fontsize=28, weight="bold", color="white")
    fig.text(0.065, 0.725, "Insertion Sort vs Selection Sort vs Merge Sort", fontsize=14, color="#D1D5DB")

    add_card(fig, 0.065, 0.485, 0.87, 0.125)
    summary_text = (
        "This report compares measured running times for three sorting algorithms across multiple input "
        "patterns and input sizes. The graphs show how runtime changes as n grows, and the tables estimate "
        "where merge sort becomes consistently faster."
    )
    fig.text(0.09, 0.547, textwrap.fill(summary_text, 108), fontsize=11.2, color=COLORS["text"], linespacing=1.35, va="center")

    stats = [
        ("Benchmark rows", f"{len(df):,}"),
        ("Input patterns", str(df["data_type"].nunique())),
        ("Algorithms", str(df["algorithm"].nunique())),
        ("Input range", f"{int(df['size'].min())}-{int(df['size'].max())}"),
    ]

    x_positions = [0.065, 0.29, 0.515, 0.74]
    for x, (label, value) in zip(x_positions, stats):
        add_card(fig, x, 0.295, 0.18, 0.12)
        fig.text(x + 0.025, 0.37, label, fontsize=9.5, color=COLORS["muted"])
        fig.text(x + 0.025, 0.32, value, fontsize=19, weight="bold", color=COLORS["navy"])

    add_card(fig, 0.065, 0.13, 0.87, 0.11)
    fig.text(0.09, 0.205, "Report outputs", fontsize=12, weight="bold", color=COLORS["navy"])
    outputs = [
        "Individual PNG graphs saved in results/plots",
        "PDF report saved as results/sorting_graph_report.pdf",
        "Crossover summary saved as results/crossover_summary.csv",
    ]
    for index, output in enumerate(outputs):
        fig.text(0.11, 0.178 - index * 0.026, output, fontsize=9.7, color=COLORS["text"])

    add_footer(fig, page)
    pdf.savefig(fig)
    plt.close(fig)

def draw_summary_table(fig: plt.Figure, crossover_df: pd.DataFrame) -> None:
    x = 0.055
    y = 0.17
    w = 0.89
    h = 0.58
    headers = ["Input type", "Insertion vs Merge", "Selection vs Merge"]
    col_widths = [0.34, 0.33, 0.33]
    row_count = len(crossover_df) + 1
    row_h = h / row_count

    add_card(fig, x, y, w, h, radius=0.01)

    current_x = x
    for col, header in enumerate(headers):
        cw = w * col_widths[col]
        fig.add_artist(Rectangle((current_x, y + h - row_h), cw, row_h, transform=fig.transFigure, color=COLORS["navy"], zorder=0))
        fig.text(current_x + cw / 2, y + h - row_h / 2, header, fontsize=11.4, weight="bold", color="white", ha="center", va="center")
        current_x += cw

    for row_index, (_, row) in enumerate(crossover_df.iterrows(), start=1):
        row_y = y + h - row_h * (row_index + 1)
        fill = "#FFFFFF" if row_index % 2 else "#F8FAFC"
        fig.add_artist(Rectangle((x, row_y), w, row_h, transform=fig.transFigure, color=fill, zorder=-0.5))

        values = [
            pretty_data_type(row["data_type"]),
            crossover_text(row["insertion_vs_merge"]),
            crossover_text(row["selection_vs_merge"]),
        ]

        current_x = x
        for col, value in enumerate(values):
            cw = w * col_widths[col]
            fig.text(current_x + cw / 2, row_y + row_h / 2, value, fontsize=11.2, color=COLORS["text"], ha="center", va="center")
            if col > 0:
                fig.add_artist(Rectangle((current_x, row_y), 0.001, row_h, transform=fig.transFigure, color=COLORS["border"], zorder=1))
            current_x += cw

    for i in range(row_count + 1):
        line_y = y + i * row_h
        fig.add_artist(Rectangle((x, line_y), w, 0.001, transform=fig.transFigure, color=COLORS["border"], zorder=1))


def create_summary_page(pdf: PdfPages, crossover_df: pd.DataFrame, page: int) -> None:
    fig = plt.figure(figsize=(11, 8.5), facecolor=COLORS["background"])
    add_page_title(fig, "Executive summary", "Stable crossover points by input type")
    draw_summary_table(fig, crossover_df)

    add_card(fig, 0.055, 0.075, 0.89, 0.06, radius=0.01)
    fig.text(
        0.08,
        0.105,
        "Stable crossover means merge sort was faster for five consecutive input sizes starting from that value of n.",
        fontsize=9.8,
        color=COLORS["muted"],
        va="center",
    )

    add_footer(fig, page)
    pdf.savefig(fig)
    plt.close(fig)


def create_guide_page(pdf: PdfPages, page: int) -> None:
    fig = plt.figure(figsize=(11, 8.5), facecolor=COLORS["background"])
    add_page_title(fig, "How to read the graphs", "Interpretation guide for the benchmark results")

    guide_items = [
        ("X-axis", "Input size n. Larger n means the algorithm sorted a longer list."),
        ("Y-axis", "Average running time in milliseconds. Lower values mean faster execution."),
        ("Lines", "Each line represents one algorithm. Selection sort appears as its own separate line."),
        ("Crossover markers", "Vertical dashed lines mark where merge sort becomes consistently faster than an O(n^2) algorithm."),
        ("Limitation", "Small benchmark timings are noisy, so the report uses repeated runs and a consecutive-size rule instead of relying on one isolated point."),
    ]

    top = 0.68
    row_h = 0.095
    gap = 0.025
    for index, (title, body) in enumerate(guide_items):
        y = top - index * (row_h + gap)
        add_card(fig, 0.065, y - row_h, 0.87, row_h)
        fig.text(0.105, y - row_h / 2, title, fontsize=11.2, weight="bold", color=COLORS["navy"], va="center")
        fig.add_artist(Rectangle((0.245, y - row_h + 0.018), 0.001, row_h - 0.036, transform=fig.transFigure, color=COLORS["border"], zorder=1))
        fig.text(0.275, y - row_h / 2, textwrap.fill(body, 88), fontsize=10.2, color=COLORS["text"], linespacing=1.2, va="center")

    add_footer(fig, page)
    pdf.savefig(fig)
    plt.close(fig)

def create_graph_page(pdf: PdfPages, summary: pd.DataFrame, data_type: str, crossover_row: pd.Series, page: int) -> None:
    fig = plt.figure(figsize=(11, 8.5), facecolor=COLORS["background"])
    add_page_title(fig, f"{pretty_data_type(data_type)} input", "Average running time by input size")

    add_card(fig, 0.055, 0.105, 0.64, 0.62)
    add_card(fig, 0.72, 0.105, 0.225, 0.62)

    chart_ax = fig.add_axes([0.095, 0.19, 0.54, 0.44])
    crossovers = {
        "Insertion vs Merge": crossover_row["insertion_vs_merge"],
        "Selection vs Merge": crossover_row["selection_vs_merge"],
    }
    draw_runtime_chart(chart_ax, summary, data_type, crossovers)

    side_ax = fig.add_axes([0.75, 0.155, 0.16, 0.485])
    side_ax.axis("off")
    side_ax.text(0, 1.00, "Key results", fontsize=14, weight="bold", color=COLORS["navy"], va="top")

    fastest_name, largest_n = fastest_at_largest_n(summary, data_type)
    side_ax.text(0, 0.82, "Fastest at largest n", fontsize=9.8, weight="bold", color=COLORS["text"], va="top")
    side_ax.text(0, 0.75, f"{fastest_name}\nwhen n = {largest_n}", fontsize=9.2, color=COLORS["text"], va="top", linespacing=1.22)

    side_ax.text(0, 0.55, "Stable crossovers", fontsize=9.8, weight="bold", color=COLORS["text"], va="top")
    side_ax.text(0, 0.47, f"Insertion vs Merge\n{crossover_text(crossovers['Insertion vs Merge'])}", fontsize=9.1, color=COLORS["text"], va="top", linespacing=1.22)
    side_ax.text(0, 0.30, f"Selection vs Merge\n{crossover_text(crossovers['Selection vs Merge'])}", fontsize=9.1, color=COLORS["text"], va="top", linespacing=1.22)

    side_ax.text(0, 0.12, "Reading note", fontsize=9.8, weight="bold", color=COLORS["text"], va="top")
    note = "Lower line means faster. Dashed line means stable crossover."
    side_ax.text(0, 0.045, textwrap.fill(note, 28), fontsize=8.8, color=COLORS["text"], va="top", linespacing=1.18)

    add_footer(fig, page)
    pdf.savefig(fig)
    plt.close(fig)

def create_pdf_report(df: pd.DataFrame, summary: pd.DataFrame, crossover_df: pd.DataFrame) -> None:
    PDF_REPORT.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(PDF_REPORT) as pdf:
        page = 1
        create_cover_page(pdf, df, page)
        page += 1
        create_summary_page(pdf, crossover_df, page)
        page += 1
        create_guide_page(pdf, page)
        page += 1

        for data_type in sorted(summary["data_type"].unique(), key=data_type_sort_key):
            row = crossover_df[crossover_df["data_type"] == data_type].iloc[0]
            create_graph_page(pdf, summary, data_type, row, page)
            page += 1

        metadata = pdf.infodict()
        metadata["Title"] = "Sorting Algorithm Benchmark Report"
        metadata["Subject"] = "Insertion sort, selection sort, and merge sort benchmark comparison"
        metadata["Creator"] = "plot_results.py"


def plot_results() -> None:
    setup_style()
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    df = load_results(INPUT_FILE)
    summary = aggregate_results(df)
    crossover_df = compute_crossover_summary(summary)
    crossover_df.to_csv(CROSSOVER_FILE, index=False)

    for data_type in sorted(summary["data_type"].unique(), key=data_type_sort_key):
        row = crossover_df[crossover_df["data_type"] == data_type].iloc[0]
        crossovers = {
            "Insertion vs Merge": row["insertion_vs_merge"],
            "Selection vs Merge": row["selection_vs_merge"],
        }
        save_individual_plot(summary, data_type, crossovers)

        print(f"\n{data_type}:")
        for label, value in crossovers.items():
            if pd.isna(value):
                print(f"  {label}: No stable crossover")
            else:
                print(f"  {label}: n = {int(value)}")

    create_pdf_report(df, summary, crossover_df)

    print(f"\nGraphs saved in {OUTPUT_FOLDER}")
    print(f"Crossover summary saved to {CROSSOVER_FILE}")
    print(f"PDF report saved to {PDF_REPORT}")


if __name__ == "__main__":
    plot_results()
