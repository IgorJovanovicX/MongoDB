import fiftyone as fo
from utility.dataset_handlers import HANDLERS

def handle_dataset_by_type(dataset_or_name, data_dir, dtype):
    if dtype not in HANDLERS:
        raise ValueError(f"Unsupported dataset type: {dtype}")

    create_fn, insert_fn = HANDLERS[dtype]

    if isinstance(dataset_or_name, str):
        return create_fn(dataset_or_name, data_dir)
    elif isinstance(dataset_or_name, fo.Dataset):
        return insert_fn(dataset_or_name, data_dir)
    else:
        raise TypeError("dataset_or_name must be a str or object of type fiftyone.Dataset")
