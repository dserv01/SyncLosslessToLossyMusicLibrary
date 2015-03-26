# SyncLosslessToLossyMusicLibrary
Synchronizes your lossless music folder to a lossy music folder (e.g. on your mobile device)

I faced the problem that I did not find any tool for converting my whole music library folder of lossless .flac music to lossy .ogg onto my smartphone. All I found had some shortcomings, so I wrote my own script that may also help you to tackle this problem as the used converting commands can be modified very easily.

Features of this script:
* Converts a folder of music to another folder while keeping the structure (e.g. /home/doms/Music -> /mnt/SDCARD0: /home/doms/Music/\*/\*.flac -> /mnt/SDCARD0/\*/\*.ogg) 
* You can define individual commands for different files
* A command may look like 'oggenc -q 8 [INPUT].flac -o [OUTPUT].ogg', where [INPUT] and [OUTPUT] are replaced by the script by the matching file paths without extension.
* Before converting, it checks if the file is already available and skips it if possible.
* It can remove files you deleted from your lossless library also from your lossy library

*My Configuration:*
All my devices have a backup/mirror folder on my Raspberry Pi server. My notebook synchronizes my complete lossless music library to the server with rsync. My android-smartphone on the other hand synchronizes its music library with the server using FolderSync. The Server regulary runs this script to convert the Music from my notebook's backup folder to the mirror folder of my smartphone.

Notebook[lossless] -(rsync)-> Notebook's Backup Folder on Server[lossless] -(this script)-> Smartphone's Mirror Folder on Server[lossy] -(FolderSync)-> sdcard of smartphone[lossy]

##Setup

This script does not need to be installed. You may need to mark as executable by
<pre>chmod +x ./SyncLosslessToLossyMusicLibrary.py</pre> but then it should run by simple <pre>./SyncLosslessToLossyMusicLibrary.py</pre>
or
<pre>python ./SyncLosslessToLossyMusicLibrary.py</pre>

However, you must configurate it first to work as the configuration is done within the script and not as usual with input parameters.
In the script you find something like
<pre>
##### CONFIGURATION ###########################################################################################
#This is the path of your lossless libray, e.g. '/home/YOURNAME/Music/'
from_path = '/mnt/EXT-DISK0/THINKPAD-L412/Music/'
#This is the path of your lossy library, e.g. /mnt/SDCARD0/Music/'
to_path = '/mnt/EXT-DISK0/MOTOROLA-RAZRI/Music/'
#Use [INPUT] and [OUTPUT] to build your commands. Both will be replaced by the full path but without the file extension,
# e.g. /home/doms/Music/Beethoven/FuerElise.flac -> /home/doms/Music/Beethoven/FuerElise
# You need to add the new and old fileextension for checking if the file is already converted and to remove old files
commands = [['flac', 'ogg', 'oggenc -q 8 [INPUT].flac -o [OUTPUT].ogg'],
['mp3', 'mp3', 'cp [INPUT].mp3 [OUTPUT].mp3']
#,['jpg', 'jpg', 'cp [INPUT].jpg [OUTPUT].jpg']
]
SYNC_DELETIONS = True
###############################################################################################################
</pre>
First set up the `from_path` as your folder with the lossless music.
Then set up the `to_path` as your folder where you want the lossy music to be.
Both need to have a '/' at the end. This script will not create further subpaths but a file from `from_path/subfolder123/song1.flac` is converted to `to_path/subfolder123/song1.ogg` (flac and ogg are only exemplary).

Next you need to set up the commands that have to be used for different files. 
<pre>['flac', 'ogg', 'oggenc -q 8 [INPUT].flac -o [OUTPUT].ogg']</pre>
converts a 'flac' into an 'ogg' by the command `oggenc -q 8 [INPUT].flac -o [OUTPUT].ogg'`.
The script will call this command for every file in 'from\_path' with the extension 'flac' where no pendant in 'to\_path' exists.
E.g. for the file `from_path/subfolder123/song1.flac` is is first checked if `to_path/subfolder123/song1.ogg` already exists, and if not the command `oggenc -q 8 from_path/subfolder123/song1.flac -o to_path/subfolder123/song1.ogg'` is executed.
Thus `[INPUT]` is replaced by `from\_path/subfolder123/song1` and `[OUTPUT]` by `to\_path/subfolder123/song1`.
