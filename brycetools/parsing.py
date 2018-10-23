import os
import xmltodict
import pandas as pd
import collections
from os import walk

class Parser:
    """
    Dedicated to parsing Adobe XMP files into a pandas dataframe.
    """
    def __init__(self, jpg_dir: str, data_dir: str):
        """
        Args:
            jpg_dir (str): where the user plans to save converted JPEG's.
            data_dir (str): where the user plans to save the pandas DataFrame
        """
        self.jpg_dir = jpg_dir
        self.data_dir = data_dir
        self.folders = []
        self.camera_type = []
        self.files = None
        self.organized = None
        self.parsed = None
        self.xmpExt = (".xmp",".XMP")

    def set_camera_type(self, brand: str):
        """
        Sets the camera type of the instance [only Sony or Canon currently]

        Args:
            brand: brand of camera files user plans to parse
        """
        brand = brand.lower()
        if brand == "canon":
            self.camera_type = (".cr2", ".CR2")
        elif brand == "sony":
            self.camera_type = (".arw",".ARW")

    def addFolder(self, folder: str):
        """
        Adds folder to the parse list

        Args:
            folder: folder path containing files user wishes to parse
        """
        if folder not in self.folders:
            self.folders.append(folder)
        else:
            raise ValueError("Folder already in parser")

    def addFolders(self, folders: list):
        """
        Adds list of foders to the parse list

        Args:
            folders: list of folder paths containing files user wishes to parse
        """
        for folder in folders:
            self.folders.append(folder)

    def clear_folders(self):
        """
        Clears all folders from parse list
        """
        self.folders.clear()

    def parse(self):
        """
        Parses folders within the folder list

        Returns:
            pandas DataFrame
        """
        self._get_files()
        self._organize_files()
        self.parsed = self._parse_xmp()
        return self.parsed

    def save_frame(self, saveName: str):
        self.parsed.to_csv(self.data_dir + "\\" + saveName + ".CSV")

    def _get_files(self):
        """
        Gathers lists of all RAW files and XMP files within folders
        """
        if len(self.camera_type) == 0:
            raise ValueError("must set camera type")
        if len(self.folders) == 0:
            raise ValueError("must add a folder")

        xmpPaths = []
        rawPaths = []
        for path in self.folders:
            for root, dirs, files in walk(path):
                for file in files:
                    if file.endswith(self.xmpExt):
                        xmpPaths.append(os.path.join(root, file))
                    elif file.endswith(self.camera_type):
                        rawPaths.append(os.path.join(root, file))
        self.files = [xmpPaths, rawPaths]

    def _organize_files(self)-> list:
        """
        Organizes files into pairs of RAW and XMP
        """
        xmpPaths = self.files[0]
        rawPaths = self.files[1]
        xmpNames = self._remove_ext(rawPaths)
        rawNames = self._remove_ext(xmpPaths)
        matched = self._file_match(xmpNames, rawNames)
        self.organized = matched

    # helper functions for organize files --> will clean up after
    def _file_match(self, removedXmp: list, removedRaw: list) -> list:
        """
        Removes XMP files or RAW files without a matching partner

        Args:
            removedXmp: a list of XMP paths with the ".XMP" extension removed
            removedRaw: a list of RAW paths with the ".RAW" extension removed

        Returns:
            list containing XMP and RAW files with a partner
        """
        inBothLists = list(set(removedXmp).intersection(removedRaw))
        inBoth = []
        for file in inBothLists:
            xmp = file + ".XMP"
            raw = file + self.camera_type[1]
            inBoth.append([xmp, raw])
        return inBoth

    def _remove_ext(self, paths: list)-> list:
        """
        Removes file extensions of file paths

        Args:
            paths: a list of file paths

        Returns:
            list of removed extensions
        """
        seperated = []
        for path in paths:
            name = path.split(".")[0]
            seperated.append(name)
        return seperated

    def _flattenDict(self, d: dict, parent_key='', sep='_') -> dict:
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self._flattenDict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _parse_xmp(self):
        """
        Parses xmp data ito a pandas DataFrame
        """
        parsedXMPDicts = []
        omitted = 0
        for xmp, raw in self.organized:
            xmp = open(xmp)
            readXmp = xmp.read()
            xmp.close()
            parsed = xmltodict.parse(readXmp)
            needed = parsed["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
            needed["raw_path"] = raw
            needed["jpg_dir"] = self.jpg_dir
            try:
                fileName = needed["@crs:RawFileName"].split(".")[0]
                needed["image_id"] = fileName
            except KeyError:
                omitted += 1
                print("\r{} files have been omitted".format(omitted), end="\r")
                pass
                continue
            finalDict = self._flattenDict(needed, sep=":")
            parsedXMPDicts.append(finalDict)
        master = pd.DataFrame(parsedXMPDicts)
        master.set_index("image_id", inplace=True)
        return master
