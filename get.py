import json

with open("link.json","r") as f:
    d = json.load(f)
l = list(d["link"].keys())

print(f'total: {len(l)}<br>')
for i in range(0,len(l)):
    print(f'{l[i]} : {d.get("link").get(l[i]).get("url")}<br>')
    i += 1
