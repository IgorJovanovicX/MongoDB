import sys
import os
import fiftyone as fo

from create.image_loader import create_image_dataset
from create.audio_loader import create_audio_dataset
from create.vide_loader import create_video_dataset
from create.specific_file_type_loader import create_annotated_dataset
from utility.dataset_logger import log_dataset_event
from utility.dataset_type_detector import detect_dataset_type
from utility.dataset_metadata import add_standard_metadata

def main():
    if len(sys.argv) != 3:
        print("Usage: python create_dataset.py <dataset_name> <data_dir>")
        sys.exit(1)

    dataset_name = sys.argv[1]
    data_dir = sys.argv[2]

    if not os.path.isdir(data_dir):
        print(f"Directory not found: {data_dir}")
        sys.exit(1)

    dtype = detect_dataset_type(data_dir)
    if not dtype:
        print("Could not detect dataset type. Supported: images, audio, video, COCO, YOLO, VOC")
        sys.exit(1)

    print(f"Detected dataset type: {dtype}")

    try:
        if dtype == "image":
            ds = create_image_dataset(dataset_name, data_dir)
        elif dtype == "audio":
            ds = create_audio_dataset(dataset_name, data_dir)
        elif dtype == "video":
            ds = create_video_dataset(dataset_name, data_dir)
        elif dtype in ("coco", "yolo", "voc"):
            ds = create_annotated_dataset(dataset_name, data_dir, dtype)
        else:
            print(f"Unsupported dataset type: {dtype}")
            sys.exit(1)

        ds.persistent = True
        ds.save()

        add_standard_metadata(ds, data_dir, dtype)

        dataset_id = str(ds._doc.id)

        log_dataset_event(dataset_name, dtype, data_dir, len(ds), update_type="create", dataset_id=dataset_id, status="success")

        print(f"Dataset '{dataset_name}' created, persisted, and stored in MongoDB with metadata.")
        fo.launch_app(ds).wait()

    except Exception as e:
        log_dataset_event(dataset_name, dtype, data_dir, 0, update_type="create", dataset_id=None, status=f"failed: {e}")
        print(f"Dataset creation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()