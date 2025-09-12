import fiftyone as fo
import os

def create_annotated_dataset(dataset_name, dataset_dir, dataset_format):
    format_map = {
        "coco": fo.types.COCODetectionDataset,
        "yolo": fo.types.YOLOv5Dataset,
        "voc": fo.types.VOCDetectionDataset
    }

    if dataset_format not in format_map:
        raise ValueError(f"Unsupported format '{dataset_format}'. Choose from: {list(format_map.keys())}")

    if not os.path.isdir(dataset_dir):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    dataset = fo.Dataset.from_dir(
        dataset_dir=dataset_dir,
        dataset_type=format_map[dataset_format],
        name=dataset_name
    )

    print(f"✅ {dataset_format.upper()} dataset '{dataset_name}' created with {len(dataset)} samples.")
    return dataset

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python create_annotated_dataset.py <dataset_name> <dataset_dir> <format: coco|yolo|voc>")
        sys.exit(1)

    ds_name = sys.argv[1]
    ds_dir = sys.argv[2]
    fmt = sys.argv[3].lower()

    ds = create_annotated_dataset(ds_name, ds_dir, fmt)
    fo.launch_app(ds).wait()
