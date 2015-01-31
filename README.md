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
