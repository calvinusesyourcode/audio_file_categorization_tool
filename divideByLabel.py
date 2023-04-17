import os
from glob import glob
from re import sub
from datetime import datetime
import audioread

folderOfAudios = "audio-labelling"
audioTypes = ["wav","mp3"]
maxDifferenceInSeconds = 300 # Between audio and txt files
deleteAfterwards = True # Set to False to leave original copies behind

os.chdir(folderOfAudios)

def dateDifference(d1,d2):
    duration = datetime(int(d1[0:4]),int(d1[4:6]),int(d1[6:8]),int(d1[8:10]),int(d1[10:12]),int(d1[12:14]))-datetime(int(d2[0:4]),int(d2[4:6]),int(d2[6:8]),int(d2[8:10]),int(d2[10:12]),int(d2[12:14]))
    difference = duration.total_seconds()
    return abs(difference)

def audioLength(file):
    with audioread.audio_open(file) as f:
        s = f.duration
    hours = int(s // 3600)
    minutes = int((s - (hours * 3600)) // 60)
    seconds = int(s - (hours * 3600) - (minutes * 60))
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)
    if len(str(seconds)) == 1:
        seconds = "0" + str(seconds)
    return f"{hours}:{minutes}:{seconds}"

# first I rename my audio files to format yyyymmddhhmmss.wav/.mp3
audios = []
for fileType in audioTypes:
    audios += glob("*."+fileType)

for fileName in audios:
    try:
        newName = sub("_","",sub("DJI_.._","",fileName))
        os.rename(fileName, newName)
    except OSError as e:
            print("OSError occured: ", e)
    except Exception as e:
            print("Something else happened: ", e)

# and now the rest of the code will work for all common audio file types named properly
audios = []
for fileType in audioTypes:
    audios += glob("*."+fileType)

oldFilesToDelete = []
for fileName in audios:
    try:
        txtFileCandidates = glob(fileName[0:8]+"*.txt")
        for txtFile in txtFileCandidates:
            if dateDifference(fileName[0:14],txtFile[0:14]) <= maxDifferenceInSeconds:
                oldFilesToDelete.append(txtFile)
                oldFilesToDelete.append(fileName)
                agreedTime = txtFile[0:14]
                with open(txtFile) as f:
                    fileLines = f.readlines()
                audioInfo = []
                for line in fileLines:
                    text = sub("\n","",line)
                    if text != "":
                        audioInfo.append(text)
                if audioInfo == []:
                    raise ValueError("The text file must've been blank!.. or something")
                ffmpegInfo = []
                audioTitle = ""
                previous = "00:00:00"
                end = audioLength(fileName)
                for i, item in enumerate(audioInfo):
                    if item[0:1] == ">":
                        audioTitle = item[1:] + " - "
                    if item[0:1] == "$":
                        current = item[1:9]
                        text = item[9:]
                        if text == "dead":
                            text = "__dead__"
                        # ffmpeg -i file.mkv -ss 00:00:20 -to 00:00:40 -c copy file-2.mkv
                        ffmpegInfo.append([fileName,previous,current,'"'+fileName[0:-4]+" "+str(i)+" - "+audioTitle+item[9:]+fileName[-4:]+'"'])
                        previous = current
                        lastIndex = i
                ffmpegInfo.append([fileName,previous,end,'"'+fileName[0:-4]+" "+str(lastIndex+1)+" - "+audioTitle+"uncategorized"+fileName[-4:]+'"'])
                print(ffmpegInfo)
                for item in ffmpegInfo:
                    try:
                        ffmpegString = 'ffmpeg -i '+item[0]+' -ss '+item[1]+' -to '+item[2]+' -c copy '+item[3]
                        os.system(ffmpegString)
                    except Exception as e:
                        print("Something happened: ", e)
                        raise           
    except Exception as e:
            print("Something happened: ", e)
            raise
if deleteAfterwards:
    for fileName in oldFilesToDelete:
        try:
            os.remove(fileName)
        except OSError as e:
            print("Something happened: ", e)