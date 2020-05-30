
import json
import time
import os

# Load Camtasia project file

FPS = 30

fileName = input("Camtasia File Name?")
file = open(fileName+".tscproj")
data = json.load(file)

# extract Start and Duration frames from .tscproj data

startFrames = []
durationFrames = []
rawFile = []

for i in data['timeline']['sceneTrack']['scenes'][0]['csml']['tracks'][0]['medias']:
            startFrames.append (i['video']['mediaStart'])
            durationFrames.append (i['video']['mediaDuration'])
            rawFile.append (i['video']['attributes']['ident'])

# Calculate Start/End times & Durations in seconds 
 
startSeconds = []
endSeconds = []
durationSeconds = []

for i in range(len(startFrames)):
    startSeconds.append (startFrames[i] / FPS)
    endSeconds.append ( (durationFrames[i] + startFrames[i]) / FPS )
    durationSeconds.append (durationFrames[i] / FPS)

# Get Timstamps of segments start from durations and write to file

stampFrames = [durationFrames[0]]

for i in range(len(durationFrames)-2):
    stampFrames.append ( durationFrames[i+1] + stampFrames[i] )

stampSeconds = []

for i in range(len(stampFrames)):
    stampSeconds.append (time.strftime('%H:%M:%S', time.gmtime(stampFrames[i]/FPS)))
    

f= open(fileName + "-Timestamps.txt","w+")

for i in range(len(stampSeconds)):
    f.write(stampSeconds[i]+'\n')

f.close()

# Create the Playlist

playList = []

for i in range(len(startSeconds)):
   playList.append (str(fileName) + '-' + str(i+1) + '.mp4')

playlistFile = fileName + "-Playlist.txt"

f= open(playlistFile,"w+")

for i in range(len(playList)):
    f.write("file '" + playList[i] + "'" '\n')

f.close()

# Generate Commands for ffmpeg

ffmpegCommands = ['ffmpeg -ss ' + str(m) + ' -i ' + '"' + str(n) + '.mp4"' + ' -t ' + str(o) + ' -avoid_negative_ts make_zero -c copy -y ' + str(p)       
                  for m,n,o,p in zip(startSeconds,rawFile,durationSeconds,playList)]

ffmpegCommands.append ('ffmpeg -f concat -safe 0 -i ' + playlistFile + ' -c copy ' + fileName + "Edited.mp4")
                
ffmpegCommands.append ('del ' + fileName + "-*.mp4")

ffmpegCommands.append ('del ' + playlistFile)

f= open(fileName+"-ffmpeg.txt","w+")

for i in range(len(ffmpegCommands)):
    f.write(ffmpegCommands[i]+'\n')

f.close()

for i in range(len(ffmpegCommands)):
    os.system(str(ffmpegCommands[i]))
