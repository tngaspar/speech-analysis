import os, sys, glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from speech_analysis import speech

# trump 2020 election rally speeches
#yt_urls = [
#    "https://www.youtube.com/watch?v=DKQfAfgWNCg",
#    "https://www.youtube.com/watch?v=6qvB5tHRNOI",
#    "https://www.youtube.com/watch?v=1E8IpeWoYCc",
#    "https://www.youtube.com/watch?v=MEqINP-TuV8",
#     "https://www.youtube.com/watch?v=40X9f4-nyBQ",
#     "https://www.youtube.com/watch?v=n85kv6H19Co"
# ]


v_id = ["DKQfAfgWNCg", "6qvB5tHRNOI", "1E8IpeWoYCc"]
all_speeches = "" 
txt_path = "data/raw_text/"
for file in v_id:
    with open(txt_path + file +".txt", 'r') as f:
        all_speeches += " " + f.read()
    
text = speech(all_speeches)

text.wordcloud()

print(text.ngrams(4, 3))
