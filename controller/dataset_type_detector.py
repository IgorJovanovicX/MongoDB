import os

def detect_dataset_type(data_dir):

    exts = set(ext.lower() for ext in [
        os.path.splitext(f)[1] for f in os.listdir(data_dir)
    ])

    img_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"}
    if exts & img_exts:
        return "image"

    audio_exts = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
    if exts & audio_exts:
        return "audio"

    video_exts = {".mp4", ".avi", ".mov", ".mkv"}
    if exts & video_exts:
        return "video"

    if os.path.exists(os.path.join(data_dir, "annotations.json")):
        return "coco"
    if any(f.endswith(".txt") for f in os.listdir(data_dir)) and \
       os.path.exists(os.path.join(data_dir, "images")):
        return "yolo"
    if os.path.exists(os.path.join(data_dir, "Annotations")):
        return "voc"

    return None
