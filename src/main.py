import requests
import urllib.parse
import json
import time

valid_types = [
    ["knife", [
        "karambit",
        "bayonet",
        "m9 bayonet",
        "butterfly knife",
        "kukri knife",
        "skeleton knife",
        "stiletto knife"
    ]],
]

'''
["rifles", []],
["sniper rifles", []]
'''
if len(valid_types) == 1:
    selected_type = 0
else:
    for asset_type in enumerate(valid_types):
        print(f"[{asset_type[0]}]: {asset_type[1][0]}")

    selected_type = -1

    while selected_type < 0 or selected_type >= len(valid_types):
        selected_type = input("select which knife you want to find ")
        try:
            selected_type = int(selected_type)
        except:
            pass
    print()

selected_path = ""

for asset in enumerate(valid_types[selected_type][1]):
    print(f"[{asset[0]}]: {asset[1]}")

while selected_path not in valid_types[selected_type][1]:
    selected_path = input("select which knife you want to find ")
    try:
        selected_path = valid_types[selected_type][1][int(selected_path)]
    except:
        pass

treeFilters = {
    "color[]": "grey",
    "categoryPath[]": f"knife/{selected_path}",
}

# "color[]="+ treeFilters["color[]"]+
options = urllib.parse.quote("categoryPath[]="+ treeFilters["categoryPath[]"])

results = []
cursor = None
url = "https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=personal&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=" + options + "&gameId=a8db&types=dmarket&cursor={cursor}&limit=100&currency=USD&platform=browser&isLoggedIn=true"
i = 1
while True:
    resp = requests.get(url.format(cursor= "" if cursor is None else cursor)).json()
    print("page " + str(i), end="\r")
    if len(resp["objects"]) == 0:
        if len(results) == 0:
            print("No results found")

        break
    cursor = resp["cursor"]
    results.extend(resp["objects"])
    #time.sleep(0.1)
    i += 1

print("done              ")

for res in results:
    paintIndex = "Vanilla"
    try:
        "not painted"
        if res["extra"]["exterior"] == "not painted":
            #  + f" https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId={res['extra']['offerId']}"
            print(res["title"] + ": " + str(paintIndex) + ", $" + str(float(res["price"]["USD"]) / 100))
    except KeyError:
        print(res)
        pass

# print(json.dumps(results[0], indent=2))
