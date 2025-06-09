import gdown
import os

def download_model():
    # File ID from the Google Drive link
    file_id = "1kIs-Dk3R2QnsL082LboyO_WnrUpAiMPI"
    
    # Generate the download URL
    url = f"https://drive.google.com/uc?id={file_id}"
    
    # Download the file
    output_path = "model.pkl"
    try:
        gdown.download(url, output_path, quiet=False)
        print(f"Model downloaded successfully to {output_path}")
    except Exception as e:
        print(f"Error downloading model: {str(e)}")

if __name__ == "__main__":
    download_model() 