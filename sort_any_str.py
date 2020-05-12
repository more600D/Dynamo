import re
def sort(x): 
    convertText = lambda text: int(text) if text.isdigit() else text.lower() 
    Textkey = lambda key: [ convertText(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(x, key = Textkey)
OUT = sort(IN[0])