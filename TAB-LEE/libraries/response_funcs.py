from datetime import *
import wikipediaapi
wiki_api = wikipediaapi.Wikipedia(user_agent="TAB-LEE v0.01")

def time() -> str:
    full_time = datetime.now()
    return f"The time is {full_time.hour}:{'{:02}'.format(full_time.minute)}"

def date() -> str:
    full_date = datetime.now()
    formatted = full_date.strftime('%A %dth %B %Y')
    return formatted

def search_web(prompt: str) -> str:
    if prompt.find("search for ") == 0:
        prompt=prompt.replace("search for ","",1)
    elif prompt.find("search ") == 0:
        prompt=prompt.replace("search ","",1)
    else:
        pass
    wiki_page = wiki_api.page(prompt)
    if wiki_page.exists():
        return "Here's what I found: "+wiki_page.summary[:100]
    return "I could not find any page like that, maybe check your internet."