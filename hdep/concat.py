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
    concatFile = "{}/{}.concat.mp4".format(folder, folder)
    fout = open(concatFile, "wb")
    for f in fragments:
        if "mp666Frag" not in f:
            continue
        
        fin = open("{}/{}".format(folder, f), "rb")
        fout.write(fin.read())
        fin.close()
    
    fout.close()

    subprocess.call([
        "ffmpeg", "-i", concatFile,
        "-c:v", "libx264", "-c:a", "libvo_aacenc",
        "{}/{}.mp4".format(folder, folder)
    ])
    