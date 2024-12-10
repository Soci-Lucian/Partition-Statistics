import os
import sys
from collections import defaultdict

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
            ext = os.path.splitext(file)[-1].lower()

            try:
                file_extensions_count[ext] += 1
                file_extensions_size[ext] += os.path.getsize(file_path)
            except (FileNotFoundError, PermissionError):
                # Skip files that are inaccessible or deleted
                continue

    print(f"Number of directories: {total_directories}")
    print(f"Number of files: {total_files}")
    print("\nFile type proportions (by count and size):")
    print("{:<10} {:<10} {:<15}".format("Extension", "Count", "Total Size (bytes)"))
    print("-" * 35)

    for ext, count in sorted(file_extensions_count.items(), key=lambda x: x[0]):
        size = file_extensions_size[ext]
        print(f"{ext:<10} {count:<10} {size:<15}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_partition.py <partition>")
    else:
        partition = sys.argv[1]
        analyze_partition(partition)
