#!/usr/bin/env python3
"""probe.py: find which game, real-time 3D, XR and simulation companies have a job board Lectern-style code can read.

    python3 probe.py                 # tries every candidate slug on Greenhouse, Ashby and Lever
Writes config/probe-results.json: one line per (company, provider, slug) that answered, with the posting count.
A candidate that answers nothing is NOT a company with no jobs; it is a company this tool cannot read (it may use
Workday, its own site or another system). Nothing is guessed: a slug counts only if the board's own API answered.
Read-only GETs against the public posting APIs, 1.1 s apart. Standard library only."""
import json, os, sys, time, urllib.request, urllib.error
from urllib.parse import quote, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED = {"boards-api.greenhouse.io", "api.ashbyhq.com", "api.lever.co"}
URLS = {"greenhouse": "https://boards-api.greenhouse.io/v1/boards/{s}/jobs",
        "ashby": "https://api.ashbyhq.com/posting-api/job-board/{s}",
        "lever": "https://api.lever.co/v0/postings/{s}?mode=json"}

# (company, [candidate slugs]). Candidates are guesses to be confirmed by the API, never assumed.
CANDIDATES = [
 ("Epic Games", ["epicgames"]), ("Roblox", ["roblox"]), ("Unity", ["unity3d", "unity", "unitytechnologies"]),
 ("Niantic", ["niantic", "nianticlabs"]), ("Niantic Spatial", ["nianticspatial"]), ("Discord", ["discord"]),
 ("Riot Games", ["riotgames"]), ("Bungie", ["bungie"]), ("Scopely", ["scopely"]), ("Zynga", ["zynga"]),
 ("Playtika", ["playtika"]), ("Playstudios", ["playstudios"]), ("Jam City", ["jamcity"]), ("Kabam", ["kabam"]),
 ("Pocket Gems", ["pocketgems"]), ("Supercell", ["supercell"]), ("Rovio", ["rovio"]), ("Wargaming", ["wargaming"]),
 ("Krafton", ["krafton"]), ("Nexon", ["nexon", "nexonamerica"]), ("Netmarble", ["netmarble"]), ("2K", ["2k", "2kgames"]),
 ("Take-Two", ["taketwo", "take-two"]), ("Gearbox", ["gearboxsoftware", "gearbox"]), ("Cloud Imperium", ["cloudimperiumgames"]),
 ("Sumo Digital", ["sumodigital"]), ("Frontier Developments", ["frontier"]), ("Jagex", ["jagex"]), ("Mythical Games", ["mythicalgames"]),
 ("Immutable", ["immutable"]), ("Animoca", ["animoca", "animocabrands"]), ("Voodoo", ["voodoo"]), ("Miniclip", ["miniclip"]),
 ("Rec Room", ["recroom"]), ("VRChat", ["vrchat"]), ("Spatial", ["spatial"]), ("Snap", ["snap", "snapchat"]),
 ("Meta Reality Labs", ["meta"]), ("Magic Leap", ["magicleap"]), ("Varjo", ["varjo"]), ("Pico", ["pico"]),
 ("Cesium", ["cesium", "cesiumgs"]), ("Matterport", ["matterport"]), ("Improbable", ["improbable"]), ("Hadean", ["hadean"]),
 ("Bentley Systems", ["bentley"]), ("Autodesk", ["autodesk"]), ("Foundry", ["foundry"]), ("SideFX", ["sidefx"]),
 ("Adobe Substance", ["substance"]), ("Anything World", ["anythingworld"]), ("Inworld AI", ["inworld", "inworldai"]),
 ("Convai", ["convai"]), ("Scenario", ["scenario"]), ("Layer AI", ["layerai"]), ("Ready Player Me", ["readyplayerme"]),
 ("Hiro Labs / Hiro", ["hirolabs"]), ("Hypixel", ["hypixel"]), ("Mojang", ["mojang"]), ("Innersloth", ["innersloth"]),
 ("Devolver", ["devolver"]), ("Humble Games", ["humblegames"]), ("Annapurna", ["annapurnainteractive"]), ("Hidden Door", ["hiddendoor"]),
 ("Rockstar", ["rockstargames"]), ("Valve", ["valve"]), ("Blizzard", ["blizzard"]), ("Activision", ["activision"]),
 ("Electronic Arts", ["ea", "electronicarts"]), ("Ubisoft", ["ubisoft"]), ("Zenimax", ["zenimax"]), ("Insomniac", ["insomniac"]),
 ("Naughty Dog", ["naughtydog"]), ("Sony Interactive", ["sie", "sonyinteractive"]), ("Nintendo", ["nintendo"]),
 ("Square Enix", ["squareenix"]), ("Capcom", ["capcom"]), ("Bandai Namco", ["bandainamco"]), ("Sega", ["sega"]),
 ("Amazon Games", ["amazongames"]), ("Netflix Games", ["netflix"]), ("Apple Arcade", ["apple"]), ("Google Stadia", ["stadia"]),
 ("AppLovin", ["applovin"]), ("ironSource", ["ironsource"]), ("Singular", ["singular"]), ("Playco", ["playco"]),
 ("Skillz", ["skillz"]), ("Overwolf", ["overwolf"]), ("Twitch", ["twitch"]), ("Epic Games Store", ["epic"]),
 ("Fortis Games", ["fortisgames"]), ("Moonton", ["moonton"]), ("Lilith", ["lilith", "lilithgames"]), ("Dream Games", ["dreamgames"]),
 ("Peak", ["peak"]), ("Rollic", ["rollic"]), ("Games Workshop", ["gamesworkshop"]), ("Hasbro Digital", ["hasbro"]),
 ("Aurora", ["aurora"]), ("Wildlife Studios", ["wildlifestudios", "wildlife"]), ("Playrix", ["playrix"]), ("Huuuge", ["huuuge", "huuugegames"]),
 ("Big Fish", ["bigfishgames"]), ("Product Madness", ["productmadness"]), ("Aristocrat", ["aristocrat"]), ("Light & Wonder", ["lightandwonder"]),
 ("Bethesda", ["bethesda"]), ("Obsidian", ["obsidian"]), ("Respawn", ["respawn"]), ("Heart Machine", ["heartmachine"]),
 ("Supergiant", ["supergiant"]), ("Mountaintop", ["mountaintop"]), ("Moon Active", ["moonactive"]), ("Playtonic", ["playtonic"]),
 ("Nvidia", ["nvidia"]), ("Unreal Engine partners: Epic", ["epicgames"]), ("Luminar / sim", ["luminar"]), ("Anduril", ["andurilindustries"]),
 ("Applied Intuition", ["appliedintuition"]), ("Waymo", ["waymo"]), ("Scale AI", ["scaleai"]), ("Skydio", ["skydio"]),
 ("Figma", ["figma"]), ("Framer", ["framer"]), ("Linear", ["linear"]),
]


def get(provider, slug):
    url = URLS[provider].format(s=quote(slug))
    p = urlparse(url)
    assert p.scheme == "https" and p.hostname in ALLOWED
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    req = urllib.request.Request(url, headers={"User-Agent": "game-jobs (course project)"})
    with urllib.request.build_opener(NoRedirect).open(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def count(provider, data):
    if provider == "greenhouse": return len(data.get("jobs", []))
    if provider == "ashby": return len(data.get("jobs", []))
    return len(data) if isinstance(data, list) else None


def main():
    found, errors = [], 0
    seen = set()
    for company, slugs in CANDIDATES:
        for slug in slugs:
            for provider in URLS:
                if (provider, slug) in seen: continue
                seen.add((provider, slug))
                time.sleep(1.1)
                try:
                    n = count(provider, get(provider, slug))
                except urllib.error.HTTPError as e:
                    if e.code not in (404, 301, 302, 403, 400): errors += 1
                    continue
                except Exception:
                    errors += 1; continue
                if n:
                    found.append({"company": company, "provider": provider, "slug": slug, "postings": n})
                    print(f"FOUND {company:28} {provider:11} {slug:22} {n}", flush=True)
    out = {"probed": time.strftime("%Y-%m-%d"), "found": found, "errors": errors, "candidates_tried": len(seen)}
    json.dump(out, open(os.path.join(HERE, "config", "probe-results.json"), "w"), indent=1)
    print("done:", len(found), "boards answered of", len(seen), "(provider, slug) pairs;", errors, "errors")

if __name__ == "__main__":
    main()
