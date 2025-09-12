import fiftyone as fo
import os

def create_image_dataset(dataset_name, image_dir):
    if not os.path.isdir(image_dir):
        raise FileNotFoundError(f"Image directory not found: {image_dir}")

    dataset = fo.Dataset.from_images_dir(image_dir, name=dataset_name)
    print(f"Image dataset '{dataset_name}' created with {len(dataset)} samples.")
    return dataset

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_image_dataset.py <dataset_name> <image_dir>")
        sys.exit(1)

    ds_name = sys.argv[1]
    img_dir = sys.argv[2]
    ds = create_image_dataset(ds_name, img_dir)
    fo.launch_app(ds).wait()
