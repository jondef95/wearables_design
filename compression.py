from os.path import getsize, isfile, isdir, join
from PIL import Image, ImageFile
from sys import exit, stderr
from os import remove, rename, walk, stat
from stat import S_IWRITE
import shutil, datetime
from argparse import ArgumentParser
from abc import ABCMeta, abstractmethod
import zipfile, os, sys

class ProcessBase:
    """Abstract base class for file processors."""
    __metaclass__ = ABCMeta
 
    def __init__(self):
        self.extensions = []
        self.backupextension = 'before-compression'
 
    @abstractmethod
    def processfile(self, filename):
        """Abstract method which carries out the process on the specified file.
        Returns True if successful, False otherwise."""
        pass
 
    def processdir(self, path):
        """Recursively processes files in the specified directory matching
        the self.extensions list (case-insensitively)."""
 
        filecount = 0 # Number of files successfully updated
 
        for root, dirs, files in os.walk(path):
            for file in files:
                # Check file extensions against allowed list
                lowercasefile = file.lower()
                matches = False
                for ext in self.extensions:
                    if lowercasefile.endswith('.' + ext):
                        matches = True
                        break
                if matches:
                    # File has eligible extension, so process
                    fullpath = os.join(root, file)
                    if self.processfile(fullpath):
                        filecount = filecount + 1
        return filecount
 
class CompressImage(ProcessBase):
    """Processor which attempts to reduce image file size."""
    def __init__(self):
        ProcessBase.__init__(self)
        self.extensions = ['jpg', 'jpeg', 'png']
 
    def processfile(self, filename):
 
        try:
            # Open the image
            with open(filename, 'rb') as file:
                img = Image.open(file)

                # Check that it's a supported format
                format = str(img.format)
                if format != 'PNG' and format != 'JPEG':
                    print ('Ignoring file "' + filename + '" with unsupported format ' + format)
                    return False
 
                # This line avoids problems that can arise saving larger JPEG files with PIL
                ImageFile.MAXBLOCK = img.size[0] * img.size[1]
                
                # The 'quality' option is ignored for PNG files
                img.save(filename, quality=65, optimize=True)
 
            # Successful compression
            return True

        except Exception as e:
            stderr.write('Failure whilst processing "' + filename + '": ' + str(e) + '\n')
            return False

class CompressDirectory(ProcessBase):

    def __init__(self):
        ProcessBase.__init__(self)
        self.extensions = []

    def processdir(self, path, name):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.jpg', 'jpeg', '.png')):
                    ci = CompressImage()
                    ci.processfile(os.path.join(root, file))

        shutil.make_archive(name, 'gztar', path)
        archive_name = name + ".tar.gz"
        tmp_name = "/tmp/" + name + "/" + archive_name
        print("made it to move")
        print(archive_name)
        print(tmp_name)
        print(shutil.move(archive_name, tmp_name))

def ExtractFolder(tarname):
    filename = str.split(tarname, '.')[0]
    dirname = filename + '_' + datetime.datetime.now().strftime("%d-%m-%y_%H%M%S") 
    try:
        os.mkdir(dirname)
    except FileExistsError as e:
        pwd = os.getcwd()
        stderr.write("Directory already exists with the name: %s\n" % dirname)
        return
 
    shutil.unpack_archive(tarname, dirname)


if __name__ == "__main__":
    
    cd = CompressDirectory()
    cd.processdir(sys.argv[1], sys.argv[2]) 