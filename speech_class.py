import audio_to_text
import youtube_audio_dl
import urllib.parse as urlparse
import text_analysis
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class speech:
    def __init__(self, text=None):
        if text == None:
            self.text = ''
        else:
            self.text = text
        
        self.filtered_text = text_analysis.filter_text(text)
                
    #only taking 1 file 
    @classmethod
    def from_wav(cls, file_path):
        text = audio_to_text.get_text_from_audio(file_path)
        return cls(text)

    #only taking 1 url
    @classmethod
    def from_youtube(cls, url):
        youtube_audio_dl.youtube_audio_download(url)

        # getting video id from link and getting file path
        url_data = urlparse.urlparse(url)
        video_id = urlparse.parse_qs(url_data.query)["v"][0]
        file_path = 'data/raw_audio/'+video_id+'.wav'
        
        # speech recongition
        text = audio_to_text.get_text_from_audio(file_path)
        return cls(text)

    
    def to_txt(self, file_name):
        """Returns .txt file of speech

        Args:
            file_name (str): str with name for output file
        """
        # create directory if it does not exist
        if not os.path.isdir("data/txt/"):
            os.mkdir("data/txt/")
        # output str to .txt file
        with open("data/txt/"+ file_name, "w") as txt_file:
            txt_file.write(self.text)
    
    @classmethod
    def from_txt(cls, file_path):
        """gets speech from txt file

        Args:
            file_path (str): path to txt file

        Returns:
            speech: returns instance of speech class
        """
        with open(file_path, 'r') as txt_file:
            text = txt_file.read()
        return cls(text)
    
    def wordcloud(self, show='True'):
        """Returns a wordcloud image representation of the words during the speech

        Args:
            show (str, optional): Choice to show the plot. Defaults to 'True'.

        Returns:
            wordcloud: returns wordcloud from the wordcloud library
        """
        wcloud = WordCloud(background_color='white',
                           min_font_size=10,
                           width=700,
                           height=700).generate(self.filtered_text)
        
        if show == 'True':
            plt.figure()
            plt.imshow(wcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.show()
        
        return wcloud