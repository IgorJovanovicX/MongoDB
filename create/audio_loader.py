import fiftyone as fo
import os
import glob

def create_audio_dataset(dataset_name, audio_dir):
    if not os.path.isdir(audio_dir):
        raise FileNotFoundError(f"Audio directory not found: {audio_dir}")

    dataset = fo.Dataset(dataset_name)
    for audio_path in glob.glob(os.path.join(audio_dir, "*.wav")) + \
                      glob.glob(os.path.join(audio_dir, "*.mp3")) + \
                      glob.glob(os.path.join(audio_dir, "*.flac")):
        sample = fo.Sample(filepath=audio_path)
        dataset.add_sample(sample)

    print(f"Audio dataset '{dataset_name}' created with {len(dataset)} samples.")
    return dataset

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_audio_dataset.py <dataset_name> <audio_dir>")
        sys.exit(1)

    ds_name = sys.argv[1]
    aud_dir = sys.argv[2]
    ds = create_audio_dataset(ds_name, aud_dir)
