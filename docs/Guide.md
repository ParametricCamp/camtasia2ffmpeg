## Prerequisites

- You will need 🐍 Python 3+ on your system. Whether if you install it raw or use Anaconda environments (recommended) is up to you! 

- You will also need to have [ffmpeg](https://ffmpeg.org/download.html) in your system. If you have never used it, it is among the coolest tools ever! Find some [tricks here](https://github.com/garciadelcastillo/ffmpeg-cheatsheet).
 
- Download and install 🎥 [Camtasia](https://www.techsmith.com/download/camtasia) version Since you will not be using it to render video, I belive you can work with the trial version endlessly! 🕺

## Usage

- Open Camtasia and create a new project. Save it as `projectname.tscproj` somewhere on your system. 

- Make sure the videos you will be editing are in the same folder as the `tscproj` file. Import them into Camtasia's media library.  

- Use Camtasia's timeline feature to edit the video. Remember that this is just for simple cut and paste of video trims, so 1 track, no transitions, overlays, audio effects or fancy stuff...! 🎞✂️📺✔️

- When done, save the file and exit Camtasia. 

- Now, take the `camtasia2ffmpeg.py` file on this project, and copy it to the camtasia project folder.

- Open a terminal (or Anaconda shell) and go to that project folder. From there, type:

    python .\camtasia2ffmpeg.py '.\projectname.tscproj'

- The script will read the trimming info from the Camtasia file, and use `ffmpeg` under the hood to trim chunks of the original video/s and stitch them together without any reencoding. The video will lose no quality at all, and the process will take only a few seconds. As a by-product, the script also generates some `txt` files with additional information. 

## Recommendations

- If you are recording video that you intend to edit with this tool, make sure your keyframing is as low as possible (1 second is recommended). Trims using this method can only start on keyframes, so if your keyframes are every 10 seconds, the beginning of a video trim will not start where you want it, but second before, wherever the earlier previous keyframe is available... 

- If you are editing [ParametricCamp](https://www.youtube.com/parametriccamp) livestream videos with [@garciadelcastillo](https://github.com/garciadelcastillo), he usually leaves a long audio pauses before and after he starts recording a trim, so that it easier to see the audio histogram and find them :)