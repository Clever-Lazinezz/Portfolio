import os
import sys
from pytube import YouTube


def main():
    # This part launches a script which takes a file url as a parameter
    custom_url = ""
    try:
        custom_url = sys.argv[1]
    except:
        None
    run_program = 'Python "URL File Downloader Script.py" ' + custom_url
    # 0 = EXIT_SUCCESS
    x = os.system(run_program)
    # Program exits if an error occured in the above system call
    exit() if x != 0 else None
    
    
    # Download the video using pytube
    # changing the url requires a modification to path
    url = 'https://www.youtube.com/watch?v=xvFZjo5PgG0'
    yt = YouTube(url)
    x = yt.streams.first().download()
    
    
    # Path needs to be updated if url changes or the video title changes
    path = os.path.join(os.getcwd(), '"Rick Roll (Different link + no ads).3gpp"')
    print("\n", path, "\n")
    path_plus = 'open ' + path
    os.system(path_plus)


if __name__ == '__main__':
    main()