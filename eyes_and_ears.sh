#Runs a youtube video with omxplayer
#Usage: youtube url retry
#where url is the string url of the video
#where set retry=1 if it plays silent video the first time
youtube() {
	url=$1
	retry=${2:-unset}
	vurls=$(youtube-dl -g $url)
	set -f 
	#Splits the urls by the space - both video and seperate sound URLs
	#are given
	array=($vurls)
	if [ $retry == 'unset' ] 
	then
		omxplayer "${array[1]}"
	else	
		omxplayer "${array[0]}"
	fi
}

video() {
    # Capture 20 seconds of raw video at 640x480 and 150kB/s bit rate into a
	# pivideo.h264 file:
	raspivid -t 20000 -w 640 -h 480 -fps 25 -b 1200000 -p 0,0,640,480 -o pivideo.h264 
	# Wrap the raw video with an MP4 container: 
	MP4Box -add pivideo.h264 $1
	# Remove the source raw file, leaving the remaining pivideo.mp4 file to play
	rm pivideo.h264
}
