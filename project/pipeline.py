import os
import subprocess
import zipfile

def download_kaggle_competition_data(competition_name, output_directory):
    competition_command = f"kaggle competitions download -c {competition_name} -p {output_directory}"
    subprocess.run(competition_command, shell=True)

def extract_zip(zip_path, output_directory):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_directory)

def delete_zip(zip_path):
    os.remove(zip_path)

if __name__ == "__main__":
    kaggle_competition_name = "microsoft-malware-prediction"
    output_directory = "../data/"
    
    print("Output directory before downloading:", os.path.abspath(output_directory))
    
    os.environ["KAGGLE_CONFIG_DIR"] = os.path.expanduser("~/.kaggle/")
    download_kaggle_competition_data(kaggle_competition_name, output_directory)
    
    zip_filename = os.path.join(output_directory, f"{kaggle_competition_name}.zip")
    extract_zip(zip_filename, output_directory)
    
    print("Output directory after extracting:", os.path.abspath(output_directory))
    
    delete_zip(zip_filename)
    print("Competition data downloaded and extracted successfully.")
