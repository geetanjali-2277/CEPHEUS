#from speechtotext import Speech_To_Text_Python
import webbrowser
from data.web_data import websites

websites_lower = {k.lower(): v for k, v in websites.items()}

def open_web(webname):
    website_name=webname.lower().split()
    counts={}

    for name in website_name:
        counts[name]=counts.get(name,0)+1

    urls_to_open=[]

    for name,count in counts.items():
        if name in websites_lower:
            url = websites_lower[name]['url']
            urls_to_open.extend([url]*count)
    
    
    if urls_to_open:
        for url in urls_to_open:
            webbrowser.open(url)
        print("opening.....")
    else:
        print("not found")



