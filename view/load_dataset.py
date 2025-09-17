import sys
import fiftyone as fo
from list_datasets import list_datasets

def choose_dataset_interactively():
    datasets = list_datasets(print_output=True)
    if not datasets:
        sys.exit(1)

    while True:
        choice = input("\nEnter the number of the dataset to load: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(datasets):
                return datasets[idx - 1]
        print("Invalid selection. Please enter a valid number.")

def main():
    dataset_name = None
    limit = None

    if len(sys.argv) == 1:
        dataset_name = choose_dataset_interactively()

    elif len(sys.argv) == 2:
        dataset_name = sys.argv[1]

    elif len(sys.argv) == 3:
        dataset_name = sys.argv[1]
        try:
            limit = int(sys.argv[2])
            if limit <= 0:
                raise ValueError
        except ValueError:
            print("Limit must be a positive number")
            sys.exit(1)
    else:
        print("Usage: python launch_dataset.py [dataset_name] [limit]")
        sys.exit(1)

    available = list_datasets(print_output=False)

    if not available:
        print("No datasets available to load.")
        sys.exit(1)

    if dataset_name not in available:
        print(f"Dataset '{dataset_name}' not found.\n")
        dataset_name = choose_dataset_interactively()

    ds = fo.load_dataset(dataset_name)

    if limit:
        print(f"Launching FiftyOne with first {limit} samples of '{dataset_name}'...")
        view = ds.limit(limit)
        session = fo.launch_app(view)
    else:
        print(f"Launching FiftyOne with full dataset '{dataset_name}'...")
        session = fo.launch_app(ds)

    session.wait()

if __name__ == "__main__":
    main()
