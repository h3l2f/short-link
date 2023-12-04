import argparse
import json
import random
import validators

with open("link.json","r") as f:
    d = json.load(f)

letter = ["ABCDEFGHIJKLMNOPWRSTUYWXYZ","abcdefghijklmnopqrstuvwxyz","abcdefghijklmnopqrstuvwxyz"]

def rankey():
    while True:
        keyword = ""
        for i in range(0,random.randint(4,6)):
            w = random.choice(letter)
            kg = random.choice(w)
            keyword = keyword + kg
            i += 1
        try:
            with open("link.json","r") as f:
                d = json.load(f)
            n = d["link"][keyword]
        except KeyError:
            return keyword
        else:
            pass

parser = argparse.ArgumentParser()
parser.add_argument('-l', type=str)
args = parser.parse_args()
link = args.l
if validators.url(link) == True:
    keyword = rankey()
    d["link"][keyword] = link
    with open("link.json","w") as f:
        json.dump(d,f,indent=4)

    print(keyword)
else:
    print("URL is invalid")
