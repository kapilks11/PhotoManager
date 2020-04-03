import errno
import sqlite3
import os
import hashlib
from shutil import copyfile




# Main code starts here
# os.system("rm -rf import")
folder2scan = input(' Please Enter the folder name to scan : ')
confirm = input(' All files are erased please enter "Erased OK" To proceed')
print(folder2scan)
for root, dirs, files in os.walk(folder2scan, topdown=False):
    for name in files:
        fpath = os.path.join(root, name)
        # check file extension
        filename, file_extension = os.path.splitext(name)
        if file_extension.lower() in ('.pdf', '.zip', '.rar', '.gz', '.7z',
                                      '.doc', '.docx', '.ppt', '.pptx',
                                      'xls', '.xlsx', '.kdbx', '.key',
                                      '.txt', '.epub', '.mobi', '.py','.dat','.iso'):
              os.remove(fpath)



