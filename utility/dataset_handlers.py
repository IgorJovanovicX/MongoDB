from create.image_loader import create_image_dataset
from create.audio_loader import create_audio_dataset
from create.video_loader import create_video_dataset
from create.specific_file_type_loader import create_annotated_dataset

from insert.image_insert import insert_image_data
from insert.audio_insert import insert_audio_data
from insert.video_insert import insert_video_data
from insert.special_file_type_insert import insert_annotated_data

HANDLERS = {
    "image": (create_image_dataset, insert_image_data),
    "audio": (create_audio_dataset, insert_audio_data),
    "video": (create_video_dataset, insert_video_data),
    "coco":  (create_annotated_dataset, insert_annotated_data),
    "yolo":  (create_annotated_dataset, insert_annotated_data),
    "voc":   (create_annotated_dataset, insert_annotated_data),
}