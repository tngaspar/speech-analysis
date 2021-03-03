import audio_to_text
import youtube_audio_dl
import urllib.parse as urlparse

class speech:
    def __init__(self, text=None):
        if text == None:
            self.text = ''
        else:
            self.text = text
    
    #only taking 1 file 
    @classmethod
    def from_wav(cls, file_path):
        text = audio_to_text.get_text_from_audio(file_path)
        return cls(text)

    #only taking 1 url
    @classmethod
    def from_youtube(cls, url):
        youtube_audio_dl.youtube_audio_download(url)

        #getting video id from link and getting file path
        url_data = urlparse.urlparse(url)
        video_id = urlparse.parse_qs(url_data.query)["v"][0]
        file_path = 'data/raw_audio/'+video_id+'.wav'
        
        #speech recongition
        text = audio_to_text.get_text_from_audio(file_path)
        return cls(text)
