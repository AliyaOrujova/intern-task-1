import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
from matplotlib.ticker import MultipleLocator

INPUT_FILE = "results/benchmark_results.csv"
OUTPUT_FOLDER = "results/plots"
PDF_REPORT = "results/sorting_graph_report.pdf"
CROSSOVER_FILE = "results/crossover_summary.csv"
PLOTS_FOLDER = "results/plots"

def find_crossover(data_for_type, minimum_size=2, consecutive_required=5):
    insertion = data_for_type[data_for_type["algorithm"] == "insertion_sort"]
    merge = data_for_type[data_for_type["algorithm"] == "merge_sort"]

    combined = insertion.merge(
        merge,
        on=["data_type", "size"],
        suffixes=("_insertion", "_merge")
    )

    combined = combined.sort_values("size")

    for i in range(len(combined) - consecutive_required + 1):
        current_rows = combined.iloc[i:i + consecutive_required]

        first_size = int(current_rows.iloc[0]["size"])

        if first_size < minimum_size:
            continue

        merge_is_faster_every_time = all(
            current_rows["average_time_seconds_merge"]
            < current_rows["average_time_seconds_insertion"]
        )

        if merge_is_faster_every_time:
            return first_size

    return None


def plot_results():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    df = pd.read_csv(INPUT_FILE)

    crossover_points = []

    for data_type in df["data_type"].unique():
        data_for_type = df[df["data_type"] == data_type]

        insertion = data_for_type[data_for_type["algorithm"] == "insertion_sort"]
        merge = data_for_type[data_for_type["algorithm"] == "merge_sort"]

        crossover = find_crossover(data_for_type)

        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        ax.xaxis.set_major_locator(MultipleLocator(25))
        ax.xaxis.set_minor_locator(MultipleLocator(5))

        plt.grid(True, which="major")
        plt.grid(True, which="minor", alpha=0.2)
        plt.plot(
            insertion["size"],
            insertion["average_time_seconds"],
            label="Insertion sort"
        )

        plt.plot(
            merge["size"],
            merge["average_time_seconds"],
            label="Merge sort"
        )

        if crossover is not None:
            plt.axvline(
                x=crossover,
                linestyle="--",
                label=f"Crossover around n = {crossover}"
            )
        plt.xlabel("Input size n")
        plt.ylabel("Average time in seconds")

        plt.xticks(range(0, 501, 25))

        plt.legend()
        plt.grid(True)

        output_path = f"{OUTPUT_FOLDER}/{data_type}_results.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        crossover_points.append({
            "data_type": data_type,
            "crossover_point": crossover
        })

        if crossover is None:
            print(f"{data_type}: no crossover found")
        else:
            print(f"{data_type}: crossover around n = {crossover}")

    crossover_df = pd.DataFrame(crossover_points)
    crossover_df.to_csv("results/crossover_summary.csv", index=False)
    
       
    
    
def create_graph_report():
    crossover_df = pd.read_csv(CROSSOVER_FILE)

    with PdfPages(PDF_REPORT) as pdf:
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.axis("off")

        ax.text(
            0.5,
            0.93,
            "Sorting Algorithm Benchmark Report",
            ha="center",
            va="center",
            fontsize=22,
            fontweight="bold"
        )

        ax.text(
            0.5,
            0.87,
            "Insertion Sort vs Merge Sort",
            ha="center",
            va="center",
            fontsize=15
        )

        ax.text(
            0.08,
            0.78,
            "Estimated crossover points from benchmark results:",
            ha="left",
            va="center",
            fontsize=12
        )

        table_data = []

        for _, row in crossover_df.iterrows():
            data_type = row["data_type"].replace("_", " ")
            crossover = row["crossover_point"]

            if pd.isna(crossover):
                crossover_text = "No stable crossover"
            else:
                crossover_text = f"n = {int(crossover)}"

            table_data.append([data_type, crossover_text])

        table = ax.table(
            cellText=table_data,
            colLabels=["Data type", "Crossover point"],
            loc="center",
            cellLoc="center",
            colLoc="center"
        )

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        ax.text(
            0.08,
            0.08,
            "The following pages contain the graphs for each input type.",
            ha="left",
            va="center",
            fontsize=10
        )

        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        for _, row in crossover_df.iterrows():
            data_type = row["data_type"]
            plot_path = os.path.join(PLOTS_FOLDER, f"{data_type}_results.png")

            if not os.path.exists(plot_path):
                print(f"Skipping missing plot: {plot_path}")
                continue

            image = mpimg.imread(plot_path)

            fig, ax = plt.subplots(figsize=(11, 8.5))
            ax.imshow(image)
            ax.axis("off")

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

    print(f"Combined graph report saved to {PDF_REPORT}")


if __name__ == "__main__":
    plot_results()
    create_graph_report()

    print("\nGraphs saved in results/plots")
    print("Crossover summary saved to results/crossover_summary.csv")