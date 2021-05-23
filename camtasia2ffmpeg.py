
import json
import time
import os
import argparse

# Parse the arguments
# See https://docs.python.org/3.3/library/argparse.html
parser = argparse.ArgumentParser(description='Apply lossless trimming/editing to a .mp4 file using a Camtasia project file. NOTE: all original assets must be on the same path they were when creating the Camtasia edits.')
parser.add_argument('file', type=argparse.FileType('r'),
                   help='the source Camtasia file to read')
args = parser.parse_args()


# Load Camtasia project file
# Read the file into a json object
fileName = os.path.splitext(args.file.name)[0]
file = args.file
data = json.load(file)

# Save a copy of the Camtasia project in v18
data['version'] = "2.0"
data['authoringClientName']['version'] = "18.0"
with open(fileName + '_v18.tscproj', 'w') as outfile:
    json.dump(data, outfile)

# Extract video framerate from Project file
# TODO: framerate should actually be fetched from each clip individually,
# however since concat will fail anyway if videos don't have the exact same props,
# let's assume the Camtasia project file has the FPS matching the input videos
FPS = data["editRate"]

# Extract Start and Duration frames from .tscproj data
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

# Get Timestamps of segments start from durations and write to file

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

ffmpegCommands = ['ffmpeg -ss ' + str(m) + ' -i ' + '"' + str(n) + '.mp4"' + ' -t ' + str(o) + ' -avoid_negative_ts make_zero -c copy -y "' + str(p) + '"'       
                  for m,n,o,p in zip(startSeconds,rawFile,durationSeconds,playList)]

ffmpegCommands.append ('ffmpeg -f concat -safe 0 -i "' + playlistFile + '" -c copy "' + fileName + '.mp4"')
                
ffmpegCommands.append ('del "' + fileName + '-*.mp4"')

ffmpegCommands.append ('del "' + playlistFile + '"')

f= open(fileName+"-ffmpeg.txt","w+")

for i in range(len(ffmpegCommands)):
    f.write(ffmpegCommands[i]+'\n')

f.close()

for i in range(len(ffmpegCommands)):
    os.system(str(ffmpegCommands[i]))
