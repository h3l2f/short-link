import json

with open("link.json","r") as f:
    d = json.load(f)
l = list(d["link"].keys())

#Config can viewer see the original code
#y = show // n= No

is_showing = "y"

print(f'total: {len(l)}<br>')
for i in range(0,len(l)):
    link = d.get("link").get(l[i]).get("url")
    if is_showing == "n":
        link = "Hidden as config!"
    print(f'{l[i]} : {link}<br>')
    i += 1
