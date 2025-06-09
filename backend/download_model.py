import gdown
import os

def download_model():
    # File ID from the Google Drive link
    file_id = "1kIs-Dk3R2QnsL082LboyO_WnrUpAiMPI"
    
    # Generate the download URL
    url = f"https://drive.google.com/uc?id={file_id}"
    
    # Create models directory if it doesn't exist
    os.makedirs("backend/models", exist_ok=True)
    
    # Download the file
    output_path = "backend/models/model.pkl"
    try:
        gdown.download(url, output_path, quiet=False)
        print(f"Model downloaded successfully to {output_path}")
    except Exception as e:
        print(f"Error downloading model: {str(e)}")

if __name__ == "__main__":
    download_model() 