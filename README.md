# Fingerprint audio files & identify what's playing

- conference [PaceMaker: BackEnd-2016 conference](http://www.pacemaker.in.ua/BackEnd-2016/about)
- slides are on [slideshare.net/rodomansky/ok-shazam-la-lalalaa](http://www.slideshare.net/rodomansky/ok-shazam-la-lalalaa)

![](http://new.tinygrab.com/7020c0e8b010392da4053fa90ab8e0c8419bded864.png)

## How to set up 

1. Run `$ make clean reset` to clean & init database struct
1. Run `$ make tests` to make sure that everything is properly configurated
1. Copy some `.mp3` audio files into `mp3/` directory
1. Run `$ make fingerprint-songs` to analyze audio files & fill your db with hashes
1. Start play any of audio file (from any source) from `mp3/` directory, and run (parallely) `$ make recognize-listen seconds=5`

![](http://new.tinygrab.com/7020c0e8b0393eec4a18c62170458c029577d378c2.png)

## How to
- To remove a specific song & related hash from db

  ```bash
  $ python sql-execute.py -q "DELETE FROM songs WHERE id = 6;"
  $ python sql-execute.py -q "DELETE FROM fingerprints WHERE song_fk = 6;"
  ```

## Thanks to
- [How does Shazam work](http://coding-geek.com/how-shazam-works/)
- [Audio fingerprinting and recognition in Python](https://github.com/worldveil/dejavu) - thanks for fingerprinting login via pynum
- [Audio Fingerprinting with Python and Numpy](http://willdrevo.com/fingerprinting-and-audio-recognition-with-python/)
- [Shazam It! Music Recognition Algorithms, Fingerprinting, and Processing](https://www.toptal.com/algorithms/shazam-it-music-processing-fingerprinting-and-recognition)
- [Creating Shazam in Java](http://royvanrijn.com/blog/2010/06/creating-shazam-in-java/)

## Python3 on Windows (10 pro)
### Packages
I'm using a virtualenv create from Pycharm based on `Python3.6` interpreter (`Python3.7` is not compatible with 
`pyaudio` (cython) package):
```powershell
(venv) C:\Users\latty\PycharmProjects\audio-fingerprint-identifying-python>pip freeze
attrs==19.1.0
certifi==2019.6.16
chardet==3.0.4
cycler==0.10.0
feedparser==5.2.1
idna==2.8
kiwisolver==1.1.0
matplotlib==3.1.1
numpy==1.17.0
PyAudio==0.2.11
pydub==0.23.1
pyparsing==2.4.2
python-dateutil==2.8.0
requests==2.22.0
scipy==1.3.1
six==1.12.0
termcolor==1.1.0
urllib3==1.25.3
Wave==0.0.2
```

### FFMPEG (Chocolatery)
FFMPEG has to be accessible/installed.

You can install it with a package manager like `Chocolatery`:

[FFmpeg 4.2 - https://chocolatey.org/packages/ffmpeg](https://chocolatey.org/packages/ffmpeg)
```powershell
PS C:\WINDOWS\system32> choco install ffmpeg
Chocolatey v0.10.11
Installing the following packages:
ffmpeg
By installing you accept licenses for the packages.
Progress: Downloading ffmpeg 4.2... 100%

ffmpeg v4.2 [Approved]
ffmpeg package files install completed. Performing other installation steps.
The package ffmpeg wants to run 'chocolateyInstall.ps1'.
Note: If you don't run this script, the installation will fail.
Note: To confirm automatically next time, use '-y' or consider:
choco feature enable -n allowGlobalConfirmation
Do you want to run the script?([Y]es/[N]o/[P]rint): y

Extracting 64-bit C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg-4.2-win64-static_x64.zip to C:\ProgramData\chocolatey\lib\ffmpeg\tools...
C:\ProgramData\chocolatey\lib\ffmpeg\tools
 ShimGen has successfully created a shim for ffmpeg.exe
 ShimGen has successfully created a shim for ffplay.exe
 ShimGen has successfully created a shim for ffprobe.exe
 The install of ffmpeg was successful.
  Software installed to 'C:\ProgramData\chocolatey\lib\ffmpeg\tools'

Chocolatey installed 1/1 packages.
 See the log for details (C:\ProgramData\chocolatey\logs\chocolatey.log).
PS C:\WINDOWS\system32> ffmpeg
ffmpeg version 4.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with gcc 9.1.1 (GCC) 20190807
  configuration: --enable-gpl --enable-version3 --enable-sdl2 --enable-fontconfig --enable-gnutls --enable-iconv --enable-libass --enable-libdav1d --enable-libbluray --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libopus --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libtheora --enable-libtwolame --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libzimg --enable-lzma --enable-zlib --enable-gmp --enable-libvidstab --enable-libvorbis --enable-libvo-amrwbenc --enable-libmysofa --enable-libspeex --enable-libxvid --enable-libaom --enable-libmfx --enable-amf --enable-ffnvcodec --enable-cuvid --enable-d3d11va --enable-nvenc --enable-nvdec --enable-dxva2 --enable-avisynth --enable-libopenmpt
  [...]
```

### Running

#### collect-fingerprints-of-songs.py
```log
sqlite - connection opened
 * id=1 channels=2: 01 Javanaise Remake.mp3
   new song, going to analyze..
   fingerprinting channel 1/2
   local_maxima: 6104 of frequency & time pairs
   finished channel 1/2, got 85351 hashes
   fingerprinting channel 2/2
   local_maxima: 6407 of frequency & time pairs
   finished channel 2/2, got 89593 hashes
   storing 168257 hashes in db
 * id=2 channels=2: 02 Aux Armes Et Caetera.mp3
   new song, going to analyze..
[...]
 * id=12 channels=2: 12 Marilou Reggae Dub.mp3
   new song, going to analyze..
   fingerprinting channel 1/2
   local_maxima: 5395 of frequency & time pairs
   finished channel 1/2, got 75425 hashes
   fingerprinting channel 2/2
   local_maxima: 5452 of frequency & time pairs
   finished channel 2/2, got 76223 hashes
   storing 134695 hashes in db
end
sqlite - connection has been closed
```
#### get-database-stat.py
```log
sqlite - connection opened
sqlite - connection opened

 * total: 12 song(s) (1586013 fingerprint(s))
   ** id=9 09 Daisy Temple.mp3: 214451 hashes
   ** id=7 07 Lola Rastaquouere.mp3: 207289 hashes
   ** id=1 01 Javanaise Remake.mp3: 168257 hashes
   ** id=2 02 Aux Armes Et Caetera.mp3: 161109 hashes
   ** id=4 04 Des Laids Des Laids.mp3: 136513 hashes
   ** id=11 11 Pas Long Feu.mp3: 136409 hashes
   ** id=12 12 Marilou Reggae Dub.mp3: 134695 hashes
   ** id=8 08 Relax Baby Be Cool.mp3: 133789 hashes
   ** id=6 06 Vieille Canaille.mp3: 95227 hashes
   ** id=5 05 Brigade Des Stups.mp3: 86766 hashes
   ** id=3 03 Les Locataires.mp3: 80340 hashes
   ** id=10 10 Eau Et Gaz A Tous Les Etages.mp3: 31168 hashes

 * duplications: 0 song(s)

 * collisions: 1546010 hash(es)

done
sqlite - connection has been closed
```