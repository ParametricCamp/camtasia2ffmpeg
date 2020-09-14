# This file has been developed by Arastoo Khjehee as an automation tool for the camtasia2ffmpeg.py scritpt
# developed by Ramy Aydarous and Jose Luis Garcia del Castillo for lossless video editting without re-encoding 
# or re-rendering
# 
# https://github.com/Arastookhajehee    
# https://github.com/garciadelcastillo
# https://github.com/RamyAydarous

import os
import glob
import subprocess

print("Would you like to run the camtasia2ffmpeg.py file automatically?")
runMode = input("(y):Automatic Mode   (n):Input file name manually ")

if (runMode == "y"):
    print("")
    print("Make sure none of the .tscproj files have the same name as the .mp4 files!!!")
    print("Due to the replacement of the original file with the same name, This might")
    print("result in unexpected errors, or unwanted trimmings.")
    continueOper = input("Would you like to continue? (y):Yes (n):No ")
    if (continueOper == "y"):
        tscprojFiles = glob.glob("*.tscproj")
        fileCount = len(tscprojFiles)
        for i in range(0,fileCount):
            tscprojFile = str(tscprojFiles[i])
            subprocess.call("python .\camtasia2ffmpeg.py \"" + tscprojFile)
else:
    print("Manual Mode selected.")
    print("What is the name of the .tscproj file that you would like to use?")
    manualtscprojFile = input("(write only name without the .tscproj) ")
    tscprojFile = manualtscprojFile + ".tscproj"
    subprocess.call("python .\camtasia2ffmpeg.py \"" + tscprojFile)