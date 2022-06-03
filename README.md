# yt-archive - An archival/organizational wrapper for yt-dlp

This is a very simple script that adds some folder organization to yt-dlp. 

yt-dlp allows us to iterate through a list of urls to download with `-a, --batch-file FILE`
and also allows us to specify where to save files with `-P, --paths [TYPES:]PATH` but doesn't give us the ability to to iterate through a batch of urls and save them somewhere specific, i.e. save each URL to a specific folder.

This script adds that functionality. 

It depends on three pieces of information

* `--channel-list <csv file>` This is the path to a csv file containing `<url you want to download>, <name of folder to save those files to>`
* `--archive-location <archive file containing previous downloads>` yt-dlp give you the functionality to track what you've downloaded and skip those videos in the future. This flag points to a the file that will contain that history. If the file doesn't already exist, it will be created. The default value is `<current directory>/archive.txt`
* `--save-location <root folder to save in>` This is the folder where the various sub-folders will be saved. The default is the directory you are running the script from.

# Example
In this example we assume that your are running the script from `/home/username/yt-archive` and you have a seperate folder in your home directory you want to save your downloads to.

  `python yt-archive.py --channel-list ~/yt-downloads/channels.csv --archive-location ~/yt-downloads/archive.txt --save-location ~/yt-downloads/`
  
  This example will look for a csv file in `~/yt-downloads` to know what urls to download and what folders to save them in. It will look in `~/yt-downloads/archive.txt` to see what videos have already been downloaded and skip those and will finally save each url in a folder name specified in `channels.csv`
  
  # What you need to do
  * Start by installing yt-dlp: `pip install -r requirements.txt`
  * Create a csv file containing `<playlist url to download from>, <folder name to save videos in to >`. You can refer to `example.csv` in this repo to see what we're talking about. Your csv file should contain multiple urls to lookup.
  * Run the script with the arguments outlined above

# How to use this script
This script gives you the ability to curate a list of channels you would like to archive and then pull down un-archived content whenever you like. It also adds in the benefit of folder based organization for easier reference later. 
