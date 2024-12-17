import os
import sys
from collections import defaultdict
import matplotlib.pyplot as plt

def analyze_partition(partition_path):
    if not os.path.exists(partition_path):
        print(f"Path {partition_path} does not exist.")
        return

    total_directories = 0
    total_files = 0
    file_extensions_count = defaultdict(int)
    file_extensions_size = defaultdict(int)

    for root, dirs, files in os.walk(partition_path):
        total_directories += len(dirs)
        total_files += len(files)

        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[-1].lower() or "no extension"

            try:
                file_extensions_count[ext] += 1
                file_extensions_size[ext] += os.path.getsize(file_path)
            except (FileNotFoundError, PermissionError): # files that are inaccessible or deleted
                continue


    # pie chart data
    top_10_by_count = sorted(file_extensions_count.items(), key=lambda x: x[1], reverse=True)[:10]
    other_count = sum(file_extensions_count[ext] for ext in file_extensions_count if ext not in dict(top_10_by_count))
    top_extensions_count = [ext for ext, _ in top_10_by_count] + ["other"]
    top_counts = [count for _, count in top_10_by_count] + [other_count]

    # pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(top_counts, labels=top_extensions_count, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
    plt.title("File Count Distribution (Top 10 + Other)")
    plt.tight_layout()
    plt.show()

    # bar chart data
    top_10_by_size = sorted(file_extensions_size.items(), key=lambda x: x[1], reverse=True)[:10]
    top_extensions_size = [ext for ext, _ in top_10_by_size]
    top_sizes = [size for _, size in top_10_by_size]

    # bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_extensions_size, top_sizes, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title("Top 10 File Extensions by Size")
    plt.ylabel("Total Size (bytes)")

    for bar, size in zip(bars, top_sizes):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{size:,}", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    #terminal output
    print(f"Number of directories: {total_directories}")
    print(f"Number of files: {total_files}")
    print("\nFile Extensions Summary:")
    print("{:<15} {:<15} {:<15}".format("Extension", "Count", "Total Size (bytes)"))
    print("-" * 45)

    for ext in sorted(file_extensions_count.keys(), key=lambda x: file_extensions_size[x], reverse=True):
        print(f"{ext:<15} {file_extensions_count[ext]:<15} {file_extensions_size[ext]:<15}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_partition.py <partition>")
    else:
        partition = sys.argv[1]
        analyze_partition(partition)
