# [punbup](https://github.com/herrcore/punbup)

Python unbup script for McAfee .bup files - with some additional fun features. Simple usage will extract all files from a .bup to a directory with the same name as the bup file.<br><br> 
What makes this script unique is that it is fully implemented in python it's not just another wrapper around 7zip! This means that you are free to run this with any non-python dependencies. Download, install the dependencies from your favourite python package manager and get un-bupping!


## Dependencies

Before you can use the script you will need to install the [OleFileIO_PL](https://bitbucket.org/decalage/olefileio_pl/overview). You can use a package manager such as easy_install or you can just download and install the library directly from the [project site](https://bitbucket.org/decalage/olefileio_pl/downloads).


## Quick Start

* Extract all files from 7dea15dd393591.bup to folder 7dea15dd393591/
```
./punbup.py 7dea15dd393591.bup
```
<br>
* Extract all files from 7dea15dd393591.bup to folder 7dea15dd393591/ and rename files to their original names (their file names as noted when they were quarantined).
```
./punbup.py -o 7dea15dd393591.bup
```
<br>
* Print the contents of the Details file to stdout. Don't extract any files (disk won't be written to).
```
./punbup.py -d 7dea15dd393591.bup
```

##Usage
```
usage: punbup.py [-h] [-d] [-o] infile

This script can be used to extract quarantined files from a McAfee .bup file.
If run with no additional options the script will extract all files from the
.bup and place them in a folder with the same name as the supplied .bup file.

positional arguments:
  infile          The file that you wish to un-bup.

optional arguments:
  -h, --help      show this help message and exit
  -d, --details   Only print the contents of the Details file. Don't extract
                  any files.
  -o, --original  Rename all quarantine files to their original names as noted
                  in the Details file. Some assumptions have been made for
                  this to feature to work. Use at your own risk.
  -c {md5,sha1,sha256}, --hash {md5,sha1,sha256}
                  Calculates the hash for all of the files in the bup.
```                  
##Features
###Fully Implemented
In addition to extracting files from a .bup file the script has the option to rename the files to their original name (instead of File_0, File_1, etc).<br><br> 
The script also provides an option to just print the Details file and not extract any files. This allows an analyst to quickly investigate a bup file without having to extract anything to disk (very helpful in some environments).<br><br>
The script should be fully platform independent. It has been tested and confirmed on some versions of Linux, Windows, OSX. 


###Future
If you take a look at the script you will see that there is a Details file parser that can be used to extract the .bup Details file into a dictionary. This dictionary is used to implement some features in the script but it has real potential to be extended. Stay tuned! 

##History
Just to set the record straight .bup files have nothing to do with the "7-zip" file format (LZMA). It is a mystery why there are tons of "unbup" scripts that all just wrap 7zip. The .bup file is actually a Compound File Binary File Format file. There is no need to bring 7zip into the picture, CFB/OLE files are well understood and can be parsed by the OleFileIO_PL library. So, hopefully, after many years of 7zip dependency pain we finally have a dependency-less unbup script. 

##Support
For questions, suggestions, collaborations, or if you just want to complain you can hit me up on twitter [@herrcore](https://twitter.com/herrcore).


    
