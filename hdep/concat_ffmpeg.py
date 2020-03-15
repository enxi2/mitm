import os
import re
import subprocess
import sys

def natural_sort(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python {} <folder>".format(sys.argv[0]))
        sys.exit(1)
    
    folder = sys.argv[1]
    fragments = sorted(os.listdir(folder), key=natural_sort)
    concatFile = "{}/files.txt".format(folder)
    fout = open(concatFile, "w")
    for f in fragments:
        if "mp666Frag" not in f:
            continue
        
        fout.write("file '{}'\n".format(f))
    
    fout.close()
    
    subprocess.call([
        "ffmpeg", "-f", "concat", "-i", concatFile,
        #"-c:v", "libx264", "-c:a", "libvo_aacenc",
        "-err_detect", "ignore_err",
        "-c:v", "copy",
        "-flags", "+global_header", "-fflags", "+genpts",
        "{}/{}.mp4".format(folder, folder)
    ])