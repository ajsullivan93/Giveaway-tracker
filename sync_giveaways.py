import json,re,datetime
from urllib.request import Request,urlopen
from html.parser import HTMLParser
from pathlib import Path

SOURCES=[
 ("Sweepstakes Radar","https://www.sweepstakesradar.com/texas-sweepstakes"),
 ("Sweepstakes Radar","https://www.sweepstakesradar.com/daily-entry-sweepstakes"),
 ("Sweepstakes Fanatics","https://sweepstakesfanatics.com/"),
 ("Sweepstakes Bible","https://www.sweepstakesbible.com/")
]
# The directories publish structured listing text. This sync intentionally only adds records
# that can be parsed conservatively; existing curated records remain in data.json.
today=datetime.date.today().isoformat()
data=json.loads(Path("data.json").read_text())
byid={x["id"]:x for x in data}

def get(url):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 GiveawayTracker/1.0"})
    return urlopen(req,timeout=20).read().decode("utf-8","ignore")

# Conservative discovery: collect visible anchors and nearby text, then keep only likely sweepstakes.
for source,url in SOURCES:
    try: html=get(url)
    except Exception: continue
    text=re.sub(r"<[^>]+>"," ",html)
    text=re.sub(r"\s+"," ",text)
    # This sync is intentionally non-destructive. It creates a review queue for new candidates.
    candidates=re.findall(r"([^.!?]{0,100}(?:Sweepstakes|Giveaway|Contest)[^.!?]{0,220})",text,re.I)
    for c in candidates[:80]:
        if not re.search(r"(win|prize|cash|truck|car|trip|gift)",c,re.I): continue
        slug=re.sub(r"[^a-z0-9]+","-",c.lower()).strip("-")[:60]
        cid="auto-"+slug
        if cid in byid: continue
        byid[cid]={
            "id":cid,"name":c.strip()[:120],"prize":"Review listing for prize",
            "value":0,"ends":"2099-12-31","frequency":"unknown",
            "eligibility":"Review official rules","category":"review",
            "source":source,"url":url
        }
Path("data.json").write_text(json.dumps(list(byid.values()),indent=2),encoding="utf-8")
