from os import listdir, rename, path
ROOT_FOLDER = './images'
GOOGLE_SUFFIX = '_ Google_Suche'

def clean_path():
    for folder in listdir(ROOT_FOLDER):
        old_path = path.join(ROOT_FOLDER, folder)
        cleaned_path = folder.replace(GOOGLE_SUFFIX,'').strip().replace(' ', '_').lower()
        new_path = path.join(ROOT_FOLDER, cleaned_path)
        rename(old_path, new_path)

def rename_images():
    for folder in listdir(ROOT_FOLDER):
        for idx, file in enumerate(listdir(path.join(ROOT_FOLDER, folder))):
            old_path = path.join(ROOT_FOLDER, folder, file)
            new_path = path.join(ROOT_FOLDER, folder, str(idx)+'.'+file.split('.')[1])
            rename(old_path, new_path)



if __name__ == "__main__":
    clean_path()
    rename_images()