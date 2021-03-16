# radiostations python script

Simple python tool to grab radio stations from radio-browser.info, put them into a menu, and then use your local installation of mpg123 to play the station for you.

### Requirements:

* Linux (any flavor, but debian based is probably best)
* Python3
* Pipenv
* mpv (or mpg123, or mplayer, if you want to swap it in yourself)


### Install
```shell
pipenv install
```

### Execute
```shell
pipenv run python ./stations.py -h

usage: stations.py [-h] [-n NAME] [-c COUNTRY] [-s STATE] [-t TAGS]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of station
  -c COUNTRY, --country COUNTRY
                        Station country
  -s STATE, --state STATE
                        Station state (if in US)
  -t TAGS, --tags TAGS  search tag or tags (if more than one, comma-separated

```

Example (using mpg123): 
```
> pipenv run python ./stations.py -n "wfmt"                                               

Radio Player Menu
0. Exit menu
1. WFMT MP3 0 http://stream.wfmt.com/main-mp3
2. WFMT 98.7 Chicago -  IL (AAC) AAC 256 http://wowza.wfmt.com/live/smil:wfmt.smil/playlist.m3u8
3. WFMT 98.7 Chicago -  IL (MP3) MP3 0 http://stream.wfmt.com/main-mp3
Select Option: 3
 (+) Audio --aid=1 (mp3 2ch 44100Hz)
AO: [coreaudio] 44100Hz stereo 2ch floatp
A: 00:00:00 / 00:00:04 (22%) Cache: 3.1s/107KB
File tags:
 icy-title: Liszt, Franz - Tasso, lamento e trionfo, Symphonic Poem No. 2 (1849) -  -  - DG
A: 00:00:04 / 00:00:28 (18%) Cache: 22s/804KB
File tags:
 icy-title: ANON 14th c, French - Au jour du bouhourdis -  -  - Calliope
A: 00:00:27 / 00:00:51 (53%) Cache: 23s/833KB
```

When I hit `Q`, mpv exits, and sends me back to my menu:
```
Exiting... (Quit)

Radio Player Menu
0. Exit menu
1. WFMT MP3 0 http://stream.wfmt.com/main-mp3
2. WFMT 98.7 Chicago -  IL (AAC) AAC 256 http://wowza.wfmt.com/live/smil:wfmt.smil/playlist.m3u8
3. WFMT 98.7 Chicago -  IL (MP3) MP3 0 http://stream.wfmt.com/main-mp3
Select Option: 

```

### CAVEATS

1. This is a VERY ROUGH script. If your search criteria are too broad, you'll get hundreds and hundres of menu items. I set the limit to 9999, and it seems to work ok. But don't push your luck; try to be as precise with your searches as possible. 
2. ~~mpg123 and mplayer are primitive at best.~~ `mpv` is a better player than mpg123, and more streams will work out of the box. What's more, via homebrew, `mpv` is available on mac or linux. However, it's still the case that not all the stations on the list will play correctly. This is partly due to the player, but mostly due to problems with the streams themselves. 
3. if you supply multiple tags in a comma-separated list, you may unintentionally filter out results. Unfortunately, the api at radio-info is such that the tag list you search for, has to be in precisely the order it is returned from the host. So, for example, if you search for "classical,chicago", your search will filter out WFMT, because their tags are "chicago,classical". So, best to keep your tags to a minimum (meaning 1 lol)
4. The country search is by country NAME, not CODE. So, "United States" will work, but "US" will not. Likewise for the United Kingdom.
5. It seems many of the stations put their city in the tag list. So, you can reduce the size of your results by doing something like this: `-c "United States" -t "atlanta"`, which makes more sense for radio stations anyway. Eg:
```
> pipenv run python ./stations.py -c "United States" -t "atlanta"                         

Radio Player Menu
0. Exit menu
1. WCLK HD2 Atlanta -  GA MP3 64 http://provisioning.streamtheworld.com/pls/WCLKHD2.pls
2. WRAS 88.5 'Album 88' Atlanta -  GA MP3 128 http://playerservices.streamtheworld.com/pls/WRASFM.pls
3. WREK 91.1 Atlanta -  GA MP3 128 http://streaming.wrek.org:8000/main/128kb.mp3
4. WREK 91.1 Atlanta -  GA  -24 kbps MP3 MP3 24 http://streaming.wrek.org:8000/wrek_live-24kb-mono.m3u
5. WSB 750 & 95.5 Atlanta -  GA AAC+ 49 http://oom-cmg.streamguys1.com/atl750/atl750-iheart.aac
6. WWWQ 99.7 'Q100' Atlanta -  GA MP3 80 http://provisioning.streamtheworld.com/pls/WWWQFM.pls
7. WWWQ-HD2 '99X' Atlanta -  GA MP3 80 http://provisioning.streamtheworld.com/pls/WWWQH2.pls
8. WWWQ-HD3 'OG 979' Atlanta -  GA MP3 80 http://provisioning.streamtheworld.com/pls/WWWQH3.pls
Select Option: 

```
### Potential next steps:

* Searching by tags would be powerful, if it didn't matter how many or which order they were in. So, one approach might be to do some sort of preprocessing on them, after capture. But this requires getting an unfiltered list to begin with. The server code itself is open source on github. So, one could potentially suggest an improvement to the tag searching, via pull request. You can find it here: https://github.com/segler-alex/radiobrowser-api-rust
