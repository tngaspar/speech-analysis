from . import audio_to_text, youtube_audio_dl, text_analysis
import urllib.parse as urlparse
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.util import ngrams as nltk_ngrams
from collections import Counter

class speech:
    def __init__(self, text=None):
        if text == None:
            self.text = ''
        else:
            self.text = text
        
        self.filtered_text = text_analysis.filter_text(text)
                
    @classmethod
    def from_wav(cls, files_paths):
        """Returns speech in string form

        Args:
            files_paths (str or list(str)): paths to .wav files

        Returns:
            str: speech in txt form
        """
        
        # if files_paths is str tranform into list(str)
        if isinstance(files_paths, str):
            files_paths = [files_paths]
        
        # audio to text              
        text = ""
        for path in files_paths:
            text += audio_to_text.get_text_from_audio(path) + " "
        
        return cls(text)

    @classmethod
    def from_youtube(cls, urls):
        """Returns text from youtube videos

        Args:
            urls (str or list(str)): str of the url of a video or list of multiple videos

        Returns:
            str: returns str of speech recognized
        """
        youtube_audio_dl.youtube_audio_download(urls)
        
        # case only 1 video passed as str
        if isinstance(urls, str):
            urls = [urls]
            
        # getting video id from link and getting file path
        files_paths = []
        for url in urls:
            url_data = urlparse.urlparse(url)
            video_id = urlparse.parse_qs(url_data.query)["v"][0]
            files_paths.append('data/raw_audio/'+video_id+'.wav')
        
        # speech recongition
        text = ""
        for path in files_paths:
            text += audio_to_text.get_text_from_audio(path) + " "
        
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
    
    
    def ngrams(self, n, min_repetitions=2):
        """Returns dictionary of ngrams repeated more than 2 times

        Args:
            n (int): n in ngram

        Returns:
            dict: dictionary of ngrams
        """
        
        # get the dict
        ngram_dict = dict(Counter(nltk_ngrams(self.filtered_text.split(), n)))

        # remove ngrams with only one ocurrence
        ngram_dict = {key:value for key, value in ngram_dict.items() if value >= min_repetitions}   
       
        return ngram_dict    