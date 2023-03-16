#! /bin/python3

import asyncio
import aioping
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

speedport = "192.168.2.1"
google = "8.8.8.8"

async def do_ping(host, list_index):
    try:
        delay = await aioping.ping(host) * 50
    except TimeoutError:
        print("timeout")
        delay = 50

    latency_list [list_index]= [time.time(), delay, host]

async def main():
    for i in range(DATA_POINTS):
        target = google
        asyncio.create_task(do_ping(target, list_index=i*2))
        target = speedport
        asyncio.create_task(do_ping(target, list_index=i))
        await asyncio.sleep(0.1)


DATA_POINTS = 10000

latency_list = [[]] * (DATA_POINTS * 2)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


columns = ["time", "ping", "target"]
df = pd.DataFrame.from_records(latency_list, columns=columns)

df["time"] = pd.to_datetime(df["time"], unit="s")
df = df.set_index("time")

drops = df[df.ping == 50].groupby("target").count()

total = df.groupby("target").count()

print(drops, drops/total*100)



#df.plot(linestyle="", marker=".", label="google")
sns.lineplot(x="time", y="ping", hue="target", data=df, linestyle="", marker="o", alpha=0.7)

src = "homeoffice LAN, new router, test"
dst = "speedport"
plt.savefig(f"ping from {src} to {dst}.png")
plt.show()


