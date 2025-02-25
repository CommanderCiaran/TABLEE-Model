import json
import speech_recognition as sr
import pyttsx3
from difflib import get_close_matches
import libraries.response_funcs as rfunc


def load_responses_set(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_responses_set(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.75)
    return matches[0] if matches else None


def get_question_answer(question: str, responses_set: dict) -> str | None:
    for qu in responses_set["questions"]:
        if qu["question"] == question:
            return qu["answer"]
    return None

def get_func_return(question: str, responses_set: dict) -> str | None:
    for a in responses_set["questions"]:
        if a["question"] == question:
            if a["function"] != "None":
                to_return = {}
                exec("to_ret=rfunc."+a["function"], globals(), to_return)
                return to_return['to_ret']
    return None

def bot_response(prompt: str) -> str:
     responses_set: dict = load_responses_set("libraries\\responses_set.json")
     best_match: str | None = find_best_match(prompt, [qu["question"] for qu in responses_set["questions"]])

     if best_match:
         answer = get_question_answer(best_match, responses_set)
         func_return = get_func_return(best_match, responses_set)
         return answer if func_return==None else answer+func_return
     else:
         if prompt.lower().find("search") == 0:
             return rfunc.search_web(prompt)
         print("TAB-LEE: \"Not sure I get that one! Could you give me a response for next time?\"")
         queery("Not sure I get that one! Could you give me a response for next time?")
         answer = get_new_answer()
         responses_set["questions"].append({"question":prompt, "answer":answer, "function": "None"})
         save_responses_set("libraries\\responses_set.json", responses_set)
         return "My new response to that is: "+answer
   
    
def get_new_answer() -> str:
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("You: \""+text+"\"")
            return text
        except sr.UnknownValueError:
            queery("Sorry could you repeat that?")
            print("TAB-LEE: \"Sorry could you repeat that?\"\n")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

def queery(text):
    engine = pyttsx3.init()
    voice_list = engine.getProperty('voices')
    engine.setProperty('voice', voice_list[1].id)
    engine.say(text)
    engine.runAndWait()