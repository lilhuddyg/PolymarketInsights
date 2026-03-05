import requests
import json

url = "https://gamma-api.polymarket.com/events"

response = requests.get(
    url,
    params={"slug": "texas-democratic-senate-primary-winner"}
)
event = response.json()[0]

active_markets = [
    m for m in event["markets"] 
    if m["active"] == True and float(m["liquidity"]) > 0
]
active_markets.sort(key = lambda x: float(json.loads(x["outcomePrices"])[0]), reverse = True)

# Print Markets to Terminal
for m in active_markets:
    outcomes = json.loads(m["outcomes"])
    prices = json.loads(m["outcomePrices"])
    print(m['question'])
    print(f"  {outcomes[0]}: {float(prices[0]):.1%}  |  {outcomes[1]}: {float(prices[1]):.1%}")
    print(f"  Spread: {m['spread']}  |  Last trade: {m['lastTradePrice']}")
    print(f"  Volume: ${float(m['volume']):.2f}")
    print()

# Writing the data to a file
writeToFile = False
if writeToFile:
    textData = json.dumps(active_markets, indent=2)

    with open("DemMarket.txt", "w") as f:
        f.write(textData)

    print(f"Found {len(active_markets)} active markets")