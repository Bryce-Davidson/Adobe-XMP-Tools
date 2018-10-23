import os
from os import walk
from os.path import isfile, split

class FileOrganize:
    """
    finds out what XMP data needs to be generated for which raw files
    """
    def __init__(self):
        self.xmpExt = (".xmp",".XMP")
        self.folders = []
        self.camera_type = None
        # might have to not store xmp in memory as they could be thousands
        self.xmp_paths = None
        # folders found after checking which xmp's we don't have
        self.missing_folders = None
        self.missing_cats = None

    def set_camera_type(self, brand: str):
        """
        Sets the camera type of the instance [only Sony or Canon currently]

        Args:
            brand: brand of camera files user plans to parse
        """
        brand = brand.lower()
        if brand == "canon":
            self.camera_type = tuple([".cr2", ".CR2"])
        elif brand == "sony":
            self.camera_type = tuple([".arw",".ARW"])

    def addFolder(self, folder: str):
        """
        Adds folder to the folders list

        Args:
            folder: folder path of RAW files
        """
        self.folders.append(folder)

    def addFolders(self, folders: list):
        """
        Adds folders to the folders list

        Args:
            folder: a list of folder paths
        """
        for folder in folders:
            self.folders.append(folder)

    def show_missing(self):
        """
        finds which folders user needs to generate XMP data for

        Returns:
            a dictionary of paths to generate XMP data for
        """
        if len(self.folders) == 0:
            raise ValueError("Must add a folder")
        self.get_raw_files()
        self.find_cats()
        return self.missing_cats

    # helper functions for get_file()
    def remove_raw_add_xmp(self, paths: list)-> list:
        """
        Removes the RAW file extension and adds .XMP

        Args:
            paths: a list of RAW paths

        Returns:
            a list of XMP file paths
        """
        seperated = []
        for path in paths:
            name = path.split(".")[0]
            name += self.xmpExt[1]
            seperated.append(name)
        return seperated

    def find_missing_folders(self, xmpPaths: list):
        """
        Finds all folders with missing XMP data

        Args:
            xmpPaths: paths of XMP files
        """
        missing_folders = []
        for path in xmpPaths:
            if not isfile(path):
                missing_folder_path = split(path)[0]
                missing_folders.append(missing_folder_path)
        missing_folders = list(set(missing_folders))
        self.missing_folders = missing_folders

    def get_raw_files(self):
        """
        Retrives a list of all RAW file paths in folders
        """
        if self.camera_type is None:
            raise ValueError("must set camera type")
        if len(self.folders) == 0:
            raise ValueError("must add a folder")
        rawPaths = []
        for path in self.folders:
            for root, dirs, files in walk(path):
                for file in files:
                    if file.endswith(self.camera_type):
                        rawPaths.append(os.path.join(root, file))
        added_xmp = self.remove_raw_add_xmp(rawPaths)
        self.xmp_paths = added_xmp
        self.find_missing_folders(self.xmp_paths)

    def find_cats(self):
        """
        Checks in all folders missing XMP data and searches for lightroom catalog
        """
        cats = []
        missingFolders = None
        for folder in self.missing_folders:
            for root, dirs, files in walk(folder):
                for file in files:
                    if file.endswith(".lrcat"):
                        cats.append(os.path.join(root, file))
        # if we don't have as many catalogs as we expected
        # find out what folders we need xmps for and get those paths
        if len(cats) < len(self.missing_folders):
            # get the folders of containg catalogs
            catsCompare = [split(split(path)[0])[0] for path in cats]
            # remove the folder paths which contain catalogs
            missingFolders = list(set(self.missing_folders) - set(catsCompare))
        generate_xmp_for = {
                'cats':     cats,
                'folders':  missingFolders
                }
        self.missing_cats = generate_xmp_for
