import fiftyone as fo

def insert_annotated_data(dataset, data_dir, dtype):
    before_count = len(dataset)
    dataset.add_dir(
        dataset_dir=data_dir,
        dataset_type={
            "coco": fo.types.COCODetectionDataset,
            "yolo": fo.types.YOLOv4Dataset,
            "voc": fo.types.VOCDetectionDataset
        }[dtype]
    )
    after_count = len(dataset)
    return after_count - before_count
