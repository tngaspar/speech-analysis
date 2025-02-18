import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil


def get_text_from_audio(path):
    """Returns speech in str format from an inputh of a path to a .wav audio file

    Args:
        path (str): string of a path to a .wav audio file

    Returns:
        str: Full text of speech from audio file
    """

    # initialize speech recon engine
    r = sr.Recognizer()
    audio = AudioSegment.from_wav(path)  
    
    # split audio into small sparts for good handelling by google speech recognition
    audio_parts = split_on_silence(audio,
        min_silence_len = 500,
        silence_thresh = audio.dBFS-14,
        keep_silence=500,
    )
    
    # temporary storage of audio parts
    folder_name = "tmp_audio_parts"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    full_text = ""
    
    # acessing google seech recognition for each part of speech
    for i, part in enumerate(audio_parts, start=1):

        #temporarily saving part 
        part_file = os.path.join(folder_name, f"part{i}.wav")
        part.export(part_file, format="wav")
        # recognize the audio part
        with sr.AudioFile(part_file) as source:
            audio_listened = r.record(source)
            # store text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error: not recognized", str(e))
            else:
                print(part_file, ":", text)
                full_text += text
    
    # remove temporary directory and its contents    
    try:
        shutil.rmtree(folder_name)
    except OSError as e:
        
        print(f"Error: {folder_name}: {e.strerror}")
        
    # write video full text to txt
    txt_folder = "data/raw_text/"
    txt_filename = os.path.splitext(os.path.basename(path))[0] + ".txt"
    if not os.path.isdir(txt_folder):
        os.mkdir(txt_folder)
    
    with open(txt_folder + txt_filename, "w") as txt:
        txt.write(full_text)

    #return the full speech in a str     
    return full_text
