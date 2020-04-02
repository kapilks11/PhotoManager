#!/usr/bin/python3
import errno
import sqlite3
import os
import hashlib
import exifread
from shutil import copyfile
# from PIL import Image
# from PIL.ExifTags import TAGS
# from PIL import Image

# return the date and time of the image taken


def get_exif(fn):
    # Open image file for reading (binary mode)
    f = open(fn, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag in ('EXIF DateTimeOriginal'):
            return (tags[tag])


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
    dtime = get_exif(fpath)
    if dtime is not None:
        year = str(dtime)[0:4]
        month = str(dtime)[5:7]
        #       print(str(dtime))
        #       print(str(year)+' ' + str(month))
        path = 'import/'+year+'/'+month
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
    else:
        #       print('Invalid Exif data')
        path = 'import/misc'
        # Copy the files if required
#        cmd = ("cp  --backup='numbered' " + '"' + fpath + '" "' +
#               path + '/' + name + '"')
#        os.system(cmd)
    CopyCount = 0
    FileWritten = False
    while not FileWritten:
        dstfpath = os.path.join(path, name)
        exists = os.path.isfile(dstfpath)
        if exists:
            CopyCount = CopyCount + 1
            copyname, copyext = os.path.splitext(name)
            name = copyname+'_pmcopy_'+str(CopyCount)+copyext
        else:
            copyfile(fpath, dstfpath)
            FileWritten = True


# Main code starts here
# os.system("rm -rf import")
folder2scan = input(' Please Enter the folder name to scan : ')
print(folder2scan)
try:
    os.makedirs('import/misc')
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass
    print('import folder already exists')
con = sqlite3.connect('import/image.db')
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
        if file_extension.lower() in ('.jpg', '.jpeg', '.heic'):
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

count = count + 1
con.commit()
con.close()
