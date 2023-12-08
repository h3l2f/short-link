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
parser.add_argument('-rsc', type=str)
args = parser.parse_args()
link = args.l
rsc = args.rsc
if validators.url(link) == True:
    keyword = rankey() if rsc == None else rsc
    try:
        h = d["link"][rsc]
    except KeyError:
        pass
    else:
        print("Scode is not available,try again with another Scode!",end="")
        exit()
    d["link"][keyword] = link
    with open("link.json","w") as f:
        json.dump(d,f,indent=4)

    print(keyword)
else:
    print("URL is invalid")
