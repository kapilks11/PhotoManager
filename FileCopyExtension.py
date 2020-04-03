#!/usr/bin/python3
import errno
import sqlite3
import os
import hashlib
from shutil import copyfile


# return the SHA-1 hash of the file
def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def WriteFilebyPath(root, name):
    fpath = os.path.join(root, name)
    fname, fext = os.path.splitext(name)
    ftype = fext[1:]
    path = 'Files/'+ftype.lower()
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    CopyCount = 0
    FileWritten = False
    while not FileWritten:
        dstfpath = os.path.join(path, name)
        exists = os.path.isfile(dstfpath)
        if exists:
            CopyCount = CopyCount + 1
            copyname, copyext = os.path.splitext(name)
            name = fname+'_pmcopy_'+str(CopyCount)+copyext
            # print(name)
        else:
            # print(dstfpath)
            copyfile(fpath, dstfpath)
            FileWritten = True


# Main code starts here
# os.system("rm -rf import")
folder2scan = input(' Please Enter the folder name to scan : ')
print(folder2scan)
try:
    os.makedirs('Files')
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass
    print('import folder already exists')
con = sqlite3.connect('Files/storage.db')
cursorObj = con.cursor()
# cursorObj.execute("DROP TABLE images")
cursorObj.execute("CREATE TABLE IF NOT EXISTS images(sha1 text PRIMARY KEY,\
                  path text)")
con.commit()
count = 1
# directory walk over code loopp through each file in dir and sub dir
# for root, dirs, files in os.walk("input", topdown=False):
# for root, dirs, files in os.walk("/media/kapil/My Passport/Data",
# topdown=False):
for root, dirs, files in os.walk(folder2scan, topdown=False):
    for name in files:
        fpath = os.path.join(root, name)
        # check file extension
        filename, file_extension = os.path.splitext(name)
        if file_extension.lower() in ('.pdf', '.zip', '.rar', '.gz', '.7z',
                                      '.doc', '.docx', '.ppt', '.pptx',
                                      'xls', '.xlsx', '.kdbx', '.key',
                                      '.txt', '.epub', '.mobi', '.py','.dat',
                                      '.iso', '.tar'):
            # check yyfile already avaliable
            print('Processing ' + fpath)
            image_SHA1 = str(hash_file(fpath))
            cursorObj.execute("SELECT sha1 FROM images WHERE sha1=?",
                              [image_SHA1])
            rows = cursorObj.fetchall()
            FileAdded = True
            for row in rows:
                FileAdded = False
            if FileAdded:
                cursorObj.execute('''INSERT INTO images(sha1, path)
                                  VALUES(?, ?)''', (image_SHA1, name))
                con.commit()
                print('File added in database')
                # write file in destination folder
                WriteFilebyPath(root, name)
                con.commit()
            else:
                os.remove(fpath)
                pass

count = count + 1
con.commit()
con.close()
