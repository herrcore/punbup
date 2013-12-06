#!/usr/bin/env python
import sys
import os
import errno
import argparse
import re
import hashlib
    
try:
    import OleFileIO_PL
except Exception as e:
    print >>sys.stderr, 'Error - Please ensure you install the OleFileIO_PL library before running this script (https://bitbucket.org/decalage/olefileio_pl): %s' % e
    sys.exit(1)

def extract(infile, dirname=None):
    if dirname is None:
        dirname = os.getcwd()
    try:
        if OleFileIO_PL.isOleFile(infile) is not True:
            print >>sys.stderr, 'Error - %s is not a valid OLE file.' % infile
            sys.exit(1)
        
        ole = OleFileIO_PL.OleFileIO(infile)
        filelist = ole.listdir()
        for fname in filelist:
            data = ole.openstream(fname[0]).read()
            fp = open(os.path.join(dirname, fname[0]),'wb')
            fp.write(data)
            fp.close()
        ole.close()
        return filelist
    except Exception as e:
        print >>sys.stderr, 'Error - %s' % e
        sys.exit(1)

def decryptStream(data):
    ptext=''
    for b in data:
        ptext+= chr(ord(b) ^ ord('\x6A'))
    return ptext

def decryptFile(fname):
    try:
        bfile = open(fname, "rb").read()
        ptext=decryptStream(bfile)
        fp  = open(fname, "wb")
        fp.write(ptext)
        fp.close()
    except Exception as e:
        print>>sys.stderr, "Error - %s" % e
        sys.exit(1)

def extractAll(bupname, original=False):
    dirname = bupname.split('.bup')[0]
    #create directory to store extracted files
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    filelist = extract(bupname, dirname)
    for fname in filelist:
        decryptFile(os.path.join(dirname, fname[0]))

    if original:
        #rename all extracted file to their original names as noted in Details file    
        data = getDetails(bupname)
        details = parseDetails(data)
        for fname in filelist:
            if fname[0] == 'Details':
                continue
            try:
                newName = details.get(fname[0]).get("OriginalName").split('\\')[-1].split('/')[-1]
                if newName:
                    os.rename(os.path.join(dirname, fname[0]), os.path.join(dirname, newName))
                else:
                    print>>sys.stderr, "Error - Could not rename %s: original name not found in Details file." % fname
            except Exception as e:
                print>>sys.stderr, "Error - Could not rename %s: %s" % (fname, e)
            
    print>>sys.stdout, "Successfully extracted all files to %s." % dirname

def getDetails(bupname):
    try:
        if OleFileIO_PL.isOleFile(bupname) is not True:
            print >>sys.stderr, 'Error - %s is not a valid OLE file.' % bupname
            sys.exit(1)

        ole = OleFileIO_PL.OleFileIO(bupname)
        #clean this up later by catching exception
        data = ole.openstream("Details").read()
        ptext=decryptStream(data)
        ole.close()
        return ptext
    except Exception as e:
        print >>sys.stderr, 'Error - %s' % e
        sys.exit(1)

def parseDetails(data):
    #stack based parser for McAfee .bup Details file
    #this will fail spectacularly if the file contains keywords that are not accounted for in the keyword list 
    #use at your own risk
    keywords=[re.compile("\[Details\]"), re.compile("\[File_[0-9]+\]"), re.compile("\[Value_[0-9]+\]")]
    arrData = data.split("\r\n")
    details = {}
    tmp={}
    for line in reversed(arrData):
        #if the line is blank skip it
        if line == '':
            continue
        #if the line is a keyword add its dictionary to the details dictionary and reset the tmp dictionary
        keyfound=False
        for parse in keywords:
            if parse.match(line):
                details[line.replace('[','').replace(']','')] = tmp
                tmp={}
                keyfound=True
                continue 
        #if the line is not a keyword assume it is a key value pair and add it to the tmp dictionary
        if not keyfound:
            tmp[line.split('=', 1)[0]] = line.split('=', 1)[1]
    return details
    
def getHashes(bupname,htype):
    #
    #Return a dictionary of stream name and hash. 
    #
    try:
        if OleFileIO_PL.isOleFile(bupname) is not True:
            print >>sys.stderr, 'Error - %s is not a valid OLE file.' % bupname
            sys.exit(1)

        ole = OleFileIO_PL.OleFileIO(bupname)                
        hashes = {}
        for entry in ole.listdir():
            if entry[0] != "Details":
                fdata = ole.openstream(entry[0]).read()
                ptext = decryptStream(fdata)
                if htype == 'md5':
                    m = hashlib.md5() 
                elif htype == 'sha1':
                    m = hashlib.sha1() 
                elif htype == 'sha256':
                    m = hashlib.sha256() 
                m.update(ptext)
                hashes[entry[0]] = m.hexdigest()                    
        ole.close()        
        return hashes
    except Exception as e:
        print >>sys.stderr, 'Error - %s' % e
        sys.exit(1)
        

def main():
    parser = argparse.ArgumentParser(description="This script can be used to extract quarantined files from a McAfee .bup file. If run with no additional options the script will extract all files from the .bup and place them in a folder with the same name as the supplied .bup file.")
    parser.add_argument("infile", help="The file that you wish to un-bup.")
    parser.add_argument('-d','--details',dest="print_details",action='store_true',default=False,help="Only print the contents of the Details file. Don't extract any files.")
    parser.add_argument('-o','--original',dest="rename_original",action='store_true',default=False,help="Rename all quarantine files to their original names as noted in the Details file. Some assumptions have been made for this to feature to work. Use at your own risk.")
    parser.add_argument('-c','--hash',dest="hash",choices=('md5','sha1','sha256'),help="Calculates the hash for all of the files in the bup. ")
    args = parser.parse_args()
    
    bupname = args.infile
    #sanity check make sure .bup exists
    if not os.path.exists(bupname):
        print>>sys.stderr, "Error - the .bup file %s does not exist.\n" % bupname
        parser.print_help()
        sys.exit(1)
    if args.print_details:
        print getDetails(bupname)
    elif args.hash:
        hashes = getHashes(bupname,args.hash)
        for name in hashes:            
            print "%s hash for %s: %s" % (args.hash,name,hashes[name])
    elif args.rename_original:
        extractAll(bupname,original=True)
    else:
        extractAll(bupname)

if __name__ == '__main__':
    main()
