import fiftyone as fo

def insert_video_data(dataset, video_dir):
    before_count = len(dataset)
    dataset.add_videos_dir(video_dir)
    after_count = len(dataset)
    return after_count - before_count