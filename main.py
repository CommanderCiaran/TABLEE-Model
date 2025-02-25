import speech_recognition as sr
import wave
import pyaudio
import pyttsx3
import libraries.tablee_funcs as tab_f
import sounddevice as sd

keyphrase = "hello lee"
keyphrases = [
            "lee", "tab","tub", "tab lee", "tabbly", "tabby",
              "table", "tay bee", "tablet", "tabble", "Hayley",
              "bot", "lee bot", "tubby", "robot"
            ]
for i in range(0, len(keyphrases)):
    if keyphrases[i]=="Hayley":
        pass
    else:
        keyphrases[i]="hey "+keyphrases[i]

#FUNCTIONS#

def start_info():
    print("""\rv0.1\n\n* Please note: This is the console log
and any transcripts are recorded here for testing purposes only.\n\n""")



def speak(text):
    engine = pyttsx3.init()
    voice_list = engine.getProperty('voices')
    engine.setProperty('voice', voice_list[1].id)
    engine.say(text)
    engine.runAndWait()



def get_next_wav_number():
    with open("test_outputs\\prompt_list.txt", "r") as file:
        file.seek(0, 2)
        pos = file.tell()
        while pos>0 and file.read(1) != "\n":
            pos-=1
            file.seek(pos, 0)
        last_line = file.readline().strip()
        file.close()
    return last_line



def transcribe():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio_data = recognizer.listen(source)

    try:
        # Perform speech recognition using Google Web Speech API
        text = recognizer.recognize_google(audio_data)
        print("You: \""+text+"\"")

        # Test if Tab-Lee's summoned
        for substring in keyphrases:
            if substring.lower() in text.lower():
                record_prompt_and_transcribe()

    except sr.UnknownValueError:
        #print("Google Web Speech API could not understand audio")
        pass
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")



def record_prompt_and_transcribe(save_path="prompt.wav") -> None:

    print("\nTAB-LEE: \"What can i help with?\"\n")
    speak("What can i help with?")

    while True:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            audio_data = recognizer.listen(source)

        try:
            # Perform speech recognition using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            print("You: \""+text+"\"")
            # Save audio data to a WAV file
            file_num = get_next_wav_number()
            with wave.open(f"test_outputs\\num_{file_num}_{save_path}", 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(audio_data.sample_width)
                wav_file.setframerate(audio_data.sample_rate)
                wav_file.writeframes(audio_data.frame_data)
            with open("test_outputs\prompt_list.txt", "a") as file:
                appended = f"\n{str(int(file_num)+1)}"
                file.write(appended)
                file.close()
            print(f"""\n===================================
    Audio saved to {save_path}
    ===================================\n""")
            
            
        #response
            speak(tab_f.bot_response(text))
            print("\nTAB-LEE: \""+tab_f.bot_response(text)+"\"")
            return None

        except sr.UnknownValueError:
            print("You: ???\n")
            print("TAB-LEE: \"I did not understand!  Could you repeat that?\"\n")
            speak("I did not understand! Could you repeat that?")
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")



if __name__ == "__main__":
    start_info()
    while True:
        #try:
        transcribe()
        #except:
         #   speak("Something went wrong!")
