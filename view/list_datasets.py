import fiftyone as fo

def list_datasets(print_output=True):

    datasets = fo.list_datasets()

    if not datasets:
        if print_output:
            print("No datasets found in the connected MongoDB 'fiftyone' database.")
        return []

    if print_output:
        print("Available datasets:")
        for idx, name in enumerate(datasets, start=1):
            print(f" {idx}. {name}")

    return datasets

if __name__ == "__main__":
    list_datasets(print_output=True)