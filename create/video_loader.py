import fiftyone as fo
import os

def create_video_dataset(dataset_name, video_dir):
    if not os.path.isdir(video_dir):
        raise FileNotFoundError(f"Video directory not found: {video_dir}")

    dataset = fo.Dataset.from_videos_dir(video_dir, name=dataset_name)
    print(f"Video dataset '{dataset_name}' created with {len(dataset)} samples.")
    return dataset

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_video_dataset.py <dataset_name> <video_dir>")
        sys.exit(1)

    ds_name = sys.argv[1]
    vid_dir = sys.argv[2]
    ds = create_video_dataset(ds_name, vid_dir)
    fo.launch_app(ds).wait()
