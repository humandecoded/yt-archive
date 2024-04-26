import csv 
import subprocess
import os 
import argparse
from datetime import datetime

#this script is a wrapper for yt-dlp that reads a csv of youtube channels and downloads their videos
#it also creates a log file of the downloads and errors


#function that will check content of error and output and return true false
def check_log_output(line):
 
    if ("ERROR:" in line
        and "Private video" not in line 
        and "Premier" not in line 
        and "hidden" not in line):
        return True
    elif "[download] Destination" in line:
        return True
    
    return False


# parse out arguments
parser = argparse.ArgumentParser()
parser.add_argument("--channel-list", required=True, help="path to csv list of youtube channels")
parser.add_argument("--archive-file", default="archive.txt", help="location of yt-dlp archive file")
parser.add_argument("--save-folder", default="", help="folder to save your downloads")
args = vars(parser.parse_args())

#assign arguments to variables
channel_list_path = args["channel_list"]
archive_file = args["archive_file"]
folder_location = args["save_folder"]

file_name_format = "%(upload_date)s - %(title)s.%(ext)s"


# read our channels.csv in to a list
# each entry is two elements: the channel url and the folder name
with open(channel_list_path, "r") as f:
    reader = csv.reader(f)
    channel_list = list(reader)

#set up logfile
log_name = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".log"
if folder_location[-1] != "/":
    folder_location = folder_location + "/"
log_path = folder_location + log_name
print(log_path)
log_file_list = []

# loop through each channel url and its folder name
for channel in channel_list:
    print(channel)
    
    url = channel[0]
    if folder_location == "":
        save_location = f"{channel[1].strip()}"
    else:
        # check for slash at the end of argument
        if folder_location[-1] != "/":
            folder_location = folder_location + "/"
        save_location = f"{folder_location}{channel[1].strip()}"
    
    # if directory doesn't exist, create it
    if not os.path.isdir(save_location):
        os.makedirs(save_location)
    
    # check for audio-only flag
    if channel[-1].strip() == "audio":
        file_name_format = "%(upload_date)s - %(title)s - audio.%(ext)s"
        # run yt_dlp 
        yt_dlp = subprocess.Popen(["yt-dlp", 
            "-P", f"{save_location}", 
            "--download-archive", f"{archive_file}",
            "--match-filters", "availability=public",
            "-o", file_name_format,
            "-f", "ba", 
            f"{url}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
        file_name_format = "%(upload_date)s - %(title)s.%(ext)s"
        yt_dlp = subprocess.Popen(["yt-dlp", 
        "-P", f"{save_location}", 
        "--download-archive", f"{archive_file}",
        "--match-filters", "availability=public",
        "-o", file_name_format,
        f"{url}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    #capture the errors and the output
    output,errorput = yt_dlp.communicate()

    #iterate through the output and write to log
    for line in output.decode("utf-8").split("\n"):
        if check_log_output(line):
            print("Logging: " + line)
            log_file_list.append(line)
    #iterate through the errors and write to log
    for line in errorput.decode("utf-8").split("\n"):
        if check_log_output(line):
            print("Logging: " + line)
            log_file_list.append(channel[2] + " " + line)
        

# get rid of duplicates
log_file_list = list(set(log_file_list))

# rewrite just the logs we parsed out above
with open(log_path, "w") as f:
    for line in log_file_list:
        f.write(f"{line}\n\n")
#delete file if nothing to report
if os.path.getsize(log_path) == 0:
    os.remove(log_path)

# todo:option to build out archive file without downwloading
# todo: add option to pass in additional yt-dlp params
# todo: explore importing yt-dlp as python library

