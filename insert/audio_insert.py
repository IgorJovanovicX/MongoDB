import fiftyone as fo
import glob
import os

def insert_audio_data(dataset, audio_dir):
    before_count = len(dataset)
    audio_exts = (".wav", ".mp3", ".flac", ".ogg", ".m4a")
    for file in os.listdir(audio_dir):
        if file.lower().endswith(audio_exts):
            dataset.add_sample(fo.Sample(filepath=os.path.join(audio_dir, file)))
    after_count = len(dataset)
    return after_count - before_count