from youtube_dl import YoutubeDL


def youtube_audio_download(urls, audio_format='wav'):
    """Downloads a list of youtube videos into audio files

    Args:
        urls (list(str)): List of youtube urls in string format
        audio_format (str, optional): Audio format of output file ('wav' or 'mp3') Defaults to 'wav'.

    Returns:
        file: returns an audio file for each url to ./data/raw_audio/
    """
    
    # Error in case the user inputs unsupported audio format
    if audio_format not in ['mp3', 'wav']:
        print("Audio Format not supported. Only 'wav' and 'mp3' supported.")
        return 1
    
    ytdl_options = {
        'format': 'bestaudio/best',
        'extractaudio':True,
        'audioformat':audio_format,
        'outtmpl':u'data/raw_audio/%(id)s.%(ext)s',
        'noplaylist':True,
        'nockeckcertificate':True,
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '192'
        }]
    }
    ytdl = YoutubeDL(ytdl_options)
    return ytdl.download(urls)
