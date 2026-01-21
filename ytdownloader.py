import pytubefix
import ffmpeg
import subprocess
import os

def getposnumberfromstring(stri):
    number = 0
    digit = 0
    for i in range(len(stri),0,-1):
        if ord(stri[i-1]) >= 48 and ord(stri[i-1])<58:
            number += int(stri[i-1])*(10**digit)
            digit+=1
    return number

def downloadm4a(url, directory):
    yt = pytubefix.YouTube(url)
    stream = yt.streams.get_audio_only()
    stream.download(directory)

    print("done")

def downloadmp4(url, directory):
    yt = pytubefix.YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(directory)
    
    print("done")

def main():

    if int(input("1. playlist\n2. video\n")) == 1:
        playlist = pytubefix.Playlist(input("enter url "))
        mode = int(input("1. download all as m4a\n2. download all as mp4\n"))

        title = playlist.title
        if not os.path.isdir(title):
            os.mkdir(title)

        if mode == 1:
            for url in playlist:
                downloadm4a(url, playlist.title)
        else:
            for url in playlist():
                downloadmp4(url, playlist.title)
        print("done downloading playlist")

        

    else:
        downloadmode = int(input("1. search\n2. link\n"))
        url = ''
        if downloadmode == 2:
            url = input("enter url ")
        else:
            whattosearch = input("what to search? ")
            s = pytubefix.Search(whattosearch)

            searchResults = []
            for v in s.results:
                try:
                    searchResults.append([v.title,v.watch_url])
                except:
                    print('error, skipping')

            
            for i, stuff in enumerate(searchResults):
                print(i,stuff[0])

            url = searchResults[int(input("put the index of the one you want to download"))][1]
                
        yt = pytubefix.YouTube(url)
        mode = int(input("1. download best m4a\n2. download best mp4\n3. see all options\n"))

        if mode == 1:
            downloadm4a(url, "")
        elif mode == 2:
            downloadmp4(url, "")
        else:
            streams = yt.streams.all()
            i = 0
            for stream in streams:
                if "audio" in str(stream.mime_type):
                    print(str(i) + " " + str(stream.mime_type) + " " + str(stream.resolution) + " " + str(stream.abr))
                else:
                     print(str(i) + " " + str(stream.mime_type) + " " + str(stream.resolution) + " " + str(stream.fps) + str(stream.abr))
                i+=1

            streams[int(input("which one do you want to download "))].download()
            print("done")

while True:
    main()
    if not input("enter anything to continue "):
        break