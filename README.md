# Disclaimer: You can also do this with yt-dlp itself! 
The functionality this script aims to introduce does exist within yt-dlp itself. The below example will reference a list of urls you would like to check on `channels.txt`, reference `archive.txt` to see what's already been downloaded and will save the various downloads in folders named after the channel. Additionally, it also numbers them in chronological order so the most recent video should be the highest number:

`yt-dlp -o "%(uploader)s/%(playlist_count+1-playlist_index)s - %(title)s.%(ext)s" -a channels.txt --download-archive archive.txt`

This naming scheme does fall apart if videos are removed from the playlist so may not be ideal for everyone.

# yt-archive - An archival/organizational wrapper for yt-dlp

This is a very simple script that adds some folder organization to yt-dlp. 

https://github.com/yt-dlp/yt-dlp

yt-dlp allows us to iterate through a list of urls to download with `-a, --batch-file FILE`
and also allows us to specify where to save files with `-P, --paths [TYPES:]PATH` ~~but doesn't give us the ability to to iterate through a batch of urls and save them somewhere specific, i.e. save each URL to a specific folder.~~

This script adds that functionality. 

It depends on three pieces of information

* `--channel-list <csv file>` This is the path to a csv file containing `<url you want to download>, <name of folder to save those files to>`
* `--archive-location <archive file containing previous downloads>` yt-dlp give you the functionality to track what you've downloaded and skip those videos in the future. This flag points to a the file that will contain that history. If the file doesn't already exist, it will be created. The default value is `<current directory>/archive.txt`
* `--save-location <root folder to save in>` This is the folder where the various sub-folders will be saved. The default is the directory you are running the script from.

# Audio Only Option
With some channels, you may only want to download the audio (No Sleep, Creepy Pastas, etc...). In the csv file containing your urls and save folders, you can spedicfy a third field. If the third element is `audio` then that yt-dlp will only download the audio portion of that url.

You can see an example of this in the `example.csv`


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

# Troubleshooting
Depending on where pip placed your version of `yt-dlp` you may need to add `/home/<username>/.local/bin` to your $PATH
