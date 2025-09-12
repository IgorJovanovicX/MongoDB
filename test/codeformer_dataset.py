import fiftyone as fo
import os

def load_codeformer_data(root_dir, dataset_name="CodeFormer_dataset"):
    """
    Load images from CodeFormer_data directory into a FiftyOne dataset, tagging them with subfolder names.
    
    Args:
        root_dir (str): Path to the CodeFormer_data directory.
        dataset_name (str): Name of the FiftyOne dataset (default: "CodeFormer_dataset").
    
    Returns:
        fo.Dataset: The populated FiftyOne dataset.
    """
    # Create a new FiftyOne dataset
    dataset = fo.Dataset(dataset_name)
    
    # Define valid image extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    
    # Iterate through subfolders in root_dir (e.g., IdentityEnhancer_0.6)
    for subfolder in os.listdir(root_dir):
        subfolder_path = os.path.join(root_dir, subfolder)
        
        # Check if it's a directory
        if os.path.isdir(subfolder_path):
            final_results_path = os.path.join(subfolder_path, "final_results")
            
            # Check if final_results folder exists and is a directory
            if os.path.exists(final_results_path) and os.path.isdir(final_results_path):
                # Iterate through files in final_results
                for file in os.listdir(final_results_path):
                    if file.lower().endswith(image_extensions):
                        filepath = os.path.join(final_results_path, file)
                        
                        # Create a sample with the subfolder name as a tag
                        sample = fo.Sample(filepath=filepath, tags=[subfolder])
                        dataset.add_sample(sample)
    
    # Save the dataset
    dataset.save()
    return dataset

# Example usage
if __name__ == "__main__":
    root_directory = "/home/ijovanovic/Desktop/CodeFormer_data"  # Replace with your actual path
    dataset = load_codeformer_data(root_directory)
    print(f"Dataset '{dataset.name}' created with {len(dataset)} samples.")
    session = fo.launch_app("CodeFormer_dataset")
    
    # Optional: Launch the FiftyOne App to visualize
    # session = fo.launch_app(dataset)