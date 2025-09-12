import fiftyone as fo
import os

def insert_image_data(dataset, image_dir):
    """Insert new images into an existing FiftyOne dataset."""
    before_count = len(dataset)
    dataset.add_images_dir(image_dir)
    after_count = len(dataset)
    added_count = after_count - before_count
    return added_count