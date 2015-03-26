__author__ = 'Dominik Krupke, dserv01.de'

#
# While you want to listen to lossless music on your computer you may not be able to also listen to it mobile because
# it takes too much space. A 32GB-SDCard does not suffice for your full music library so you only have the options to
# either only hearing to a subset mobile or converting the music to a lossy format. This script is for the second
# option.
# * Of course you don't want the lossy files on your computer because you already have your perfect lossless music there.
# * If you extend your music library you want a simple way to also have them mobile.
# * You don't want to convert already converted music twice
# This script synchronizes a lossless library folder (e.g. your music folder on your computer) to a lossy library
# folder (e.g. the music folder of your mobile device) by checking if for all music files in your lossless folder there
# is a converted version in your lossy folder. If this is not the case the file is converted. On the other side it
# checks if you still have the lossless file for each lossy file in your library, otherwise this file is removed (so
# removing a file from your lossless library also removes it from your lossy library)
#
# You can use your own commands for converting specific files. These commands have to convert a single file (check the
# commands-array).
#
# The configuration is done with the from_path and the to_path, as well as with the commands-array.


import os
import subprocess



##### CONFIGURATION ###########################################################################################

#This is the path of your lossless libray, e.g. '/home/YOURNAME/Music/'
FROM_PATH = '/mnt/EXT-DISK0/THINKPAD-L412/Music/'
#This is the path of your lossy library, e.g. /mnt/SDCARD0/Music/'
TO_PATH = '/mnt/EXT-DISK0/MOTOROLA-RAZRI/Music/'

#Use [INPUT] and [OUTPUT] to build your commands. Both will be replaced by the full path but without the file extension,
#   e.g. /home/doms/Music/Beethoven/FuerElise.flac -> /home/doms/Music/Beethoven/FuerElise
# You need to add the new and old fileextension for checking if the file is already converted and to remove old files
COMMANDS = [['flac', 'ogg', 'oggenc -q 8 [INPUT].flac -o [OUTPUT].ogg'],
            ['mp3', 'mp3', 'cp [INPUT].mp3 [OUTPUT].mp3']
            #,['jpg', 'jpg', 'cp [INPUT].jpg [OUTPUT].jpg']
]

#Remove files that are not in the original library
SYNC_DELETIONS = True
ASK_BEFORE_DELETE = False

###############################################################################################################

#Check if vorbis-tools are installed
output = subprocess.check_output("whereis oggenc", shell=True)
if(len(output)<10):
    print "You need to install vorbis-tools first (Debian/Ubuntu: sudo apt-get install vorbis-tools)"
    print "If you don't use it, remove this check from the code"
    exit(1)



#Check path format
if(FROM_PATH[-1]!='/' or TO_PATH[-1]!='/'):
    print "Paths should end with \'/\'"
    exit(1)

#Create library paths if not existence
try:
    if(not os.path.exists(TO_PATH)):
        os.makedirs(TO_PATH)
    elif(os.path.isfile(TO_PATH)):
        raise Exception("Directory is file?!")
except Exception as e:
    print "Could not create "+TO_PATH+" because "+str(e)
    print "Aborting"
    exit(1)


#Create folders if not existing
def createFolder(subpath):
    if(os.path.exists(TO_PATH+subpath) and os.path.isdir(TO_PATH+subpath)):
        return True
    try:
        os.makedirs(TO_PATH+subpath)
        return True
    except Exception as e:
        print "Could not create directory "+subpath
        return False



#Escape the paths for the os.system
def escapePath(s):
    return s.replace(" ", "\ ").replace(")", "\)").replace("(", "\(").replace("&", "\&").replace("'", "\\\'")


#Go through all files and convert
for root, dirs, files in os.walk(FROM_PATH, topdown=False):
    subpath = root[len(FROM_PATH):]+"/"

    if(createFolder(subpath)):
        for name in files:
            filename_without_extension = os.path.splitext(name)[0]
            file_extension = os.path.splitext(name)[1][1:]

            source_path_without_extension = FROM_PATH+subpath+filename_without_extension
            converted_path_without_extension = TO_PATH+subpath+filename_without_extension

            #Get command tripple - sure you can do this more efficient with a hashmap but there will only be a few entries
            command_tripple = None
            for tripple in COMMANDS:
                if(tripple[0] == file_extension):
                    command_tripple = tripple
                    break

            if(not command_tripple):
                continue

            if(os.path.isfile(source_path_without_extension+"."+command_tripple[0])):
                if(not os.path.exists(converted_path_without_extension+"."+command_tripple[1])):
                    print "Processing "+subpath+name
                    os.system(command_tripple[2].replace("[INPUT]",escapePath(source_path_without_extension)).replace("[OUTPUT]", escapePath(converted_path_without_extension)))
            else:
                print "Could not find "+subpath+name


#Remove old files
if(SYNC_DELETIONS):
    for root, dirs,files in os.walk(TO_PATH, topdown=False):
        subpath = root[len(TO_PATH):]+"/"
        
        for name in files:
            filename_without_extension = os.path.splitext(name)[0]
            file_extension = os.path.splitext(name)[1][1:]

            source_path_without_extension = FROM_PATH+subpath+filename_without_extension
            converted_path_without_extension = TO_PATH+subpath+filename_without_extension
    
            original_exists = False
            for tripple in COMMANDS:
                if(tripple[1] == file_extension and os.path.exists(source_path_without_extension+"."+tripple[0])):
                    original_exists = True
                    break
    
            if(not original_exists):
                os.system("rm "+("-i " if ASK_BEFORE_DELETE else "")+escapePath(converted_path_without_extension)+"."+file_extension)

        #Remove old empty folders
        for folder in dirs:
            if not os.path.exists(FROM_PATH+folder):
                os.system("rmdir "+TO_PATH+folder)

