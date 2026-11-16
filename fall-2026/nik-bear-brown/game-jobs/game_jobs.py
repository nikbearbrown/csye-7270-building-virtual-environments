#!/usr/bin/env python3
"""game_jobs.py: a Lectern-style collector for game, real-time 3D, XR and simulation jobs.

    python3 game_jobs.py collect [--date YYYY-MM-DD] [--no-fetch]   # fetch boards, classify, APPEND to listings.jsonl
    python3 game_jobs.py report  [--date YYYY-MM-DD]                # write reports/summary-<date>.md

collect reads config/sources.json (companies and which job-board API to read), saves each raw response to raw/
(full listing text: never commit it), keeps a posting when the rules in this file say it is a craft role in a game
studio or a game, real-time 3D, XR or simulation role elsewhere, and APPENDS one record per posting to listings.jsonl
(append-only: take the last line per URL). Everything the script derives (family, skills, years, seniority, domain)
is AI-made by rules in this file and config/skill-dictionary.json; family_confirmed_by stays null until the course
designer sets it. Standard library only. Read-only GETs against public posting APIs, 1.1 s apart."""
import argparse, collections, datetime as dt, hashlib, html, json, os, re, sys, time, urllib.request, urllib.error
from urllib.parse import quote, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.normpath(os.path.join(HERE, "..", "..", ".."))          # csye-7270-building-virtual-environments/
ALLOWED = {"boards-api.greenhouse.io", "api.ashbyhq.com", "api.lever.co"}
URLS = {"greenhouse": "https://boards-api.greenhouse.io/v1/boards/{s}/jobs?content=true",
        "ashby": "https://api.ashbyhq.com/posting-api/job-board/{s}?includeCompensation=true",
        "lever": "https://api.lever.co/v0/postings/{s}?mode=json"}
WINDOW_DAYS = 120
TODAY = dt.date.today().isoformat()

# Role families, matched against the TITLE in this order; the first match wins.
EXCLUDE = r"recruit|talent|payroll|account(ant|ing)\b|finance|financial|\blegal\b|counsel|paralegal|compliance|procurement|facilities|executive assistant|people (partner|operations|business)|\bhr\b|human resources|\bsales\b|account (executive|manager|director)|business development|partnership|marketing|brand manager|public relations|communications|investor|\btax\b|treasury|office manager|customer (support|success|service|experience)|trust (&|and) safety|moderat|security analyst|it support|helpdesk|player support|player experience|esports|events? (manager|producer)|licensing|merchandis|\\brf\\b|electrical|mechanical|manufacturing|hardware|industrial design|physical therap|supply chain|sourcing|packaging|bookkeep|audit|strategy|bizops|user acquisition|growth|publishing manager|workplace|policy|safety operations|threat|engagement (manager|representative|team)|technical support|general resume|medical|research advisor|security|\\biam\\b|authentication|fraud|payments?|billing|privacy|identity|enterprise|advertis|\\bads?\\b|reporting|data (architect|tooling)|localization specialist|product specialist|creative strategist|marketing"
FAMILIES = [
    ("design_engineering", r"design engineer|ux engineer|ui engineer|ui programmer|interface (engineer|programmer)|creative technologist|prototyp(er|ing engineer)|front[- ]?end (engineer|developer)|design technologist"),
    ("game_design", r"game designer|systems designer|level designer|combat designer|economy designer|narrative designer|quest designer|content designer|encounter designer|game director|technical designer|designer, (game|systems|level|combat|gameplay)|(game|systems|level|combat|gameplay|monetization|live) design|design lead|world builder|ux (designer|researcher|team)|product ux|ui/?ux|product designer|ui designer|visual designer|motion designer|\\bdesigner\\b|user research"),
    ("technical_art", r"technical artist|tech(nical)? art|technical animator|\brigg(er|ing)\b|vfx (technical|td)|shader artist|look ?dev|pipeline td|technical director.*art"),
    ("art_animation", r"artist|hard surface|outsource lead|game lead|animator|concept|illustrator|modell?er|sculptor|texture|lighting|\bvfx\b|motion graphics|cinematic|art director|character|environment|3d generalist|compositor|storyboard|art lead|animation"),
    ("graphics_engine", r"graphics|rendering|engine (programmer|engineer)|\bshader|\bgpu\b|ray tracing|physics (programmer|engineer)|animation (programmer|engineer)|core (engine|technology)|simulation (engineer|programmer)|systems programmer"),
    ("gameplay_engineering", r"gameplay|game (programmer|engineer|developer)|ai programmer|combat (programmer|engineer)|unreal engineer|unity (developer|engineer)|client (engineer|programmer)|network(ing)? (programmer|engineer)|multiplayer|mobile (engineer|developer)|(ios|android) (engineer|developer)"),
    ("tools_pipeline", r"tools (programmer|engineer|developer)|pipeline|build (engineer|infrastructure)|release engineer|devops|developer (experience|productivity|platform)|automation engineer|technical director"),
    ("online_backend", r"back-?end|server (engineer|programmer)|live ?ops|platform engineer|data engineer|services engineer|cloud engineer|\bsre\b|site reliability|full[- ]?stack|infrastructure"),
    ("xr_spatial", r"\bxr\b|\bvr\b|\bar\b|spatial|headset|mixed reality|\bslam\b|computer vision|perception"),
    ("data_ml_ai", r"machine learning|\bml\b|\bai\b|data scientist|analyst|analytics|research (scientist|engineer)|applied scientist|reinforcement|forward deployed|applied ai"),
    ("audio", r"audio|\bsound\b|composer|\bmusic\b|voice"),
    ("qa_test", r"\bqa\b|quality assurance|test (engineer|lead|analyst|automation)|sdet|tester|compatibility"),
    ("production_product", r"producer|product manager|program manager|project manager|production|scrum|delivery manager|studio head|general manager|\bdirector\b|head of"),
    ("devrel_education", r"developer (relations|advocate|evangelist)|devrel|technical writer|education|instructor|trainer|curriculum|community (manager|lead)"),
    ("software_engineering_general", r"software engineer|developer|programmer|engineer"),
]
EARLY = r"\bintern(ship)?\b|new grad|graduate|early career|university|entry[- ]level|junior|\bjr\.?\b|associate\b|apprentice|trainee|co-?op\b"
SENIOR = (("director", r"director|head of|vp\b|vice president"), ("manager", r"manager"), ("principal", r"principal"), ("staff", r"\bstaff\b"),
          ("senior", r"senior|\bsr\.?\b|lead\b"), ("intern", r"\bintern"), ("junior", EARLY))


def get(url, timeout=40):
    p = urlparse(url)
    if p.scheme != "https" or p.hostname not in ALLOWED:
        raise ValueError(f"refusing host {p.hostname!r}")
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    req = urllib.request.Request(url, headers={"User-Agent": "game-jobs (course project)"})
    with urllib.request.build_opener(NoRedirect).open(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def plain(h):
    t = html.unescape(h or "")
    t = re.sub(r"<(br|/p|/li|/h\d|/div)\s*/?>", "\n", t, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", t)).strip()


def iso(ms_or_str):
    if ms_or_str in (None, ""): return None
    if isinstance(ms_or_str, (int, float)): return dt.datetime.fromtimestamp(ms_or_str / 1000, dt.timezone.utc).date().isoformat()
    return str(ms_or_str)[:10]


def normalize(provider, company, slug, raw):
    out = []
    if provider == "greenhouse":
        for j in raw.get("jobs", []):
            out.append(dict(company=company, source=provider, title=j.get("title", ""), location=(j.get("location") or {}).get("name", ""),
                            url=j.get("absolute_url", ""), date_posted=iso(j.get("first_published") or j.get("updated_at")),
                            date_basis="first_published" if j.get("first_published") else "updated_at",
                            dept="; ".join(d.get("name", "") for d in j.get("departments") or []), text=plain(j.get("content")), salary=None))
    elif provider == "ashby":
        for j in raw.get("jobs", []):
            comp = (j.get("compensation") or {}).get("compensationTierSummary")
            out.append(dict(company=company, source=provider, title=j.get("title", ""), location=j.get("location", ""), url=j.get("jobUrl", ""),
                            date_posted=iso(j.get("publishedAt")), date_basis="publishedAt", dept=f"{j.get('department','')}; {j.get('team','')}".strip("; "),
                            text=j.get("descriptionPlain") or plain(j.get("descriptionHtml")), salary=comp, remote=j.get("isRemote")))
    elif provider == "lever":
        for j in raw if isinstance(raw, list) else []:
            c = j.get("categories") or {}
            sr = j.get("salaryRange")
            extra = " ".join(f"{l.get('text','')} {plain(l.get('content'))}" for l in j.get("lists") or [])
            out.append(dict(company=company, source=provider, title=j.get("text", ""), location=c.get("location", ""), url=j.get("hostedUrl", ""),
                            date_posted=iso(j.get("createdAt")), date_basis="createdAt", dept=f"{c.get('department','')}; {c.get('team','')}".strip("; "),
                            text=(j.get("descriptionPlain") or "") + "\n" + extra + "\n" + (j.get("additionalPlain") or ""),
                            salary=(f"{sr.get('currency','')} {sr.get('min')} to {sr.get('max')}" if sr else None), remote=(j.get("workplaceType") == "remote")))
    return out


def years_required(text):
    vals = []
    for m in re.finditer(r"(\d{1,2})\s*\+?\s*(?:-\s*\d{1,2}\s*)?years?", text, re.I):
        ctx = text[max(0, m.start() - 90): m.end() + 90].lower()
        if any(w in ctx for w in ("experience", "working", "building", "developing", "professional", "industry", "shipped", "programming")):
            if int(m.group(1)) <= 20: vals.append(int(m.group(1)))
    return min(vals) if vals else None


def seniority(title, years):
    t = title.lower()
    for name, pat in SENIOR:
        if re.search(pat, t): return name
    return ("mid" if years >= 3 else "entry") if years is not None else "unspecified"


def family_of(title):
    t = title.lower()
    if re.search(EXCLUDE, t): return "excluded_non_craft"
    if re.search(r"(product |rf |mechanical |electrical |manufacturing )?design engineer", t) and not re.search(r"\bui\b|\bux\b|front|web|interface|creative|prototyp|software", t):
        return "excluded_non_craft"      # "design engineer" in the hardware sense
    for name, pat in FAMILIES:
        if re.search(pat, t): return name
    return "other"


def load_dictionary():
    d = json.load(open(os.path.join(HERE, "config", "skill-dictionary.json"), encoding="utf-8"))
    for s in d["skills"]:
        s["_re"] = [re.compile(t, re.I) for t in s["terms"]]
        s["_ex"] = [re.compile(t, re.I) for t in s.get("exclude", [])]
    d["_dom"] = {k: [re.compile(t, re.I) for t in v] for k, v in d["domain_terms"].items() if not k.startswith("_")}
    return d


def tag_skills(d, title, text):
    blob = title + "\n" + text
    hits = []
    for s in d["skills"]:
        if any(r.search(blob) for r in s["_re"]) and not any(r.search(blob) for r in s["_ex"]):
            hits.append(s["name"])
    return hits


def domain_hits(d, title, text):
    t_hit = [k for k, rs in d["_dom"].items() if any(r.search(title) for r in rs)]
    b_hit = [k for k, rs in d["_dom"].items() if any(r.search(text) for r in rs)]
    return t_hit, b_hit


def read_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.exists(p) else []


def collect(date, no_fetch):
    sources = json.load(open(os.path.join(HERE, "config", "sources.json"), encoding="utf-8"))["boards"]
    d = load_dictionary()
    listings_path = os.path.join(HERE, "listings.jsonl")
    prior = read_jsonl(listings_path)
    last = {r["url"]: r for r in prior}
    urls_by_key = {}           # company+title+location -> every URL recorded under it, expired ones too
    for r in last.values():
        urls_by_key.setdefault((r["company"].lower(), r["title"].lower(), (r["location"] or "").lower()), []).append(r["url"])
    cutoff = (dt.date.fromisoformat(date) - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    log = dict(run_id=f"collect-{date}", date=date, sources=[], postings_fetched=0, excluded=collections.Counter(), kept_new=0, kept_updated=0)
    new_lines, live = [], set()     # live = every URL on the boards read so far this run
    for b in sources:
        rawp = os.path.join(HERE, "raw", f"{b['provider']}-{b['slug']}-{date}.json")
        try:
            if no_fetch and os.path.exists(rawp):
                raw = json.load(open(rawp, encoding="utf-8"))
            else:
                time.sleep(1.1)
                raw = get(URLS[b["provider"]].format(s=quote(b["slug"])))
                json.dump(raw, open(rawp, "w", encoding="utf-8"))
        except Exception as e:
            log["sources"].append(dict(company=b["company"], provider=b["provider"], status="error", reason=str(e)[:120])); continue
        posts = normalize(b["provider"], b["company"], b["slug"], raw)
        log["sources"].append(dict(company=b["company"], provider=b["provider"], status="ok", postings=len(posts)))
        log["postings_fetched"] += len(posts)
        live |= {p["url"] for p in posts}
        for p in posts:
            fam = family_of(p["title"])
            t_hit, b_hit = domain_hits(d, p["title"], p["text"])
            reason = None
            if fam in ("excluded_non_craft", "other"): reason = fam
            elif b["domain"] != "games" and not (t_hit or len(b_hit) >= 2): reason = "not_game_or_3d"
            elif p["date_posted"] and p["date_posted"] < cutoff: reason = "outside_window"
            elif not p["url"]: reason = "no_url"
            if reason:
                log["excluded"][reason] += 1; continue
            key = (p["company"].lower(), p["title"].lower(), (p["location"] or "").lower())
            repost_of = None
            if p["url"] not in last and key in urls_by_key:
                # same company+title+location under another URL: a duplicate while that listing is still on its board,
                # a REPOST (employer gave the role a new id) once the old URL is gone from the boards read this run
                if any(u in live for u in urls_by_key[key]):
                    log["excluded"]["duplicate_company_title_location"] += 1; continue
                repost_of = urls_by_key[key][-1]
            yrs = years_required(p["text"])
            rec = dict(
                id=hashlib.sha1(p["url"].encode()).hexdigest()[:12], title=p["title"], company=p["company"], company_domain=b["domain"],
                location=p["location"], remote=p.get("remote"), url=p["url"], source=p["source"], date_posted=p["date_posted"], date_posted_basis=p["date_basis"],
                date_collected=date, run_id=log["run_id"], status="active", department=p["dept"], family=fam,
                domain_hits=sorted(set(t_hit + b_hit)), skills=tag_skills(d, p["title"], p["text"]),
                years_required=yrs, seniority=seniority(p["title"], yrs), early_career_title=bool(re.search(EARLY, p["title"], re.I)),
                salary_listed=p.get("salary") or (re.search(r"\$\s?\d{2,3},\d{3}\s*(?:-|–|to)\s*\$?\s?\d{2,3},\d{3}", p["text"]) or [None])[0],
                family_confirmed_by=None,
                ai_made_fields=["family", "domain_hits", "skills", "years_required", "seniority", "early_career_title", "salary_listed"])
            if repost_of: rec["reposted_from"] = repost_of
            old = last.get(p["url"])
            if old and all(old.get(k) == rec.get(k) for k in ("title", "family", "skills", "years_required", "seniority", "status")):
                continue
            new_lines.append(rec); last[p["url"]] = rec; urls_by_key.setdefault(key, []).append(p["url"])
            log["kept_updated" if old else "kept_new"] += 1
    # postings that were active and are no longer on a board that answered
    answered = {s["company"] for s in log["sources"] if s["status"] == "ok"}
    live_urls = set()
    for b in sources:
        rawp = os.path.join(HERE, "raw", f"{b['provider']}-{b['slug']}-{date}.json")
        if os.path.exists(rawp):
            live_urls |= {p["url"] for p in normalize(b["provider"], b["company"], b["slug"], json.load(open(rawp, encoding="utf-8")))}
    log["expired"] = 0
    for url, r in list(last.items()):
        if r["status"] == "active" and r["company"] in answered and url not in live_urls:
            new_lines.append({**r, "status": "expired", "date_collected": date, "run_id": log["run_id"]}); log["expired"] += 1
    with open(listings_path, "a", encoding="utf-8") as f:
        for r in new_lines: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    log["excluded"] = dict(log["excluded"])
    log_path, n_log = os.path.join(HERE, "logs", f"run-{date}.json"), 1
    while os.path.exists(log_path):          # never overwrite an earlier run's log: a second run the same day gets -2, -3 ...
        n_log += 1; log_path = os.path.join(HERE, "logs", f"run-{date}-{n_log}.json")
    json.dump(log, open(log_path, "w"), indent=1)
    print(f"fetched {log['postings_fetched']} postings from {sum(1 for s in log['sources'] if s['status']=='ok')} boards; "
          f"new {log['kept_new']}, updated {log['kept_updated']}, expired {log['expired']}; excluded {log['excluded']}")


def course_coverage(d):
    text = ""
    for root, _, files in os.walk(os.path.join(COURSE, "modules")):
        for f in files:
            if f.endswith(".md"): text += open(os.path.join(root, f), encoding="utf-8", errors="replace").read().lower() + "\n"
    names = sorted(os.listdir(os.path.join(COURSE, "modules")))
    cov = {}
    for s in d["skills"]:
        ts = s.get("course_terms") or []
        cov[s["name"]] = (sum(text.count(t) for t in ts) if ts else None)
    return cov, [n for n in names if re.match(r"\d\d-", n)]


def report(date, suffix=""):
    d = load_dictionary()
    last = {}
    for r in read_jsonl(os.path.join(HERE, "listings.jsonl")): last[r["url"]] = r
    act = [r for r in last.values() if r["status"] == "active"]
    log = json.load(open(os.path.join(HERE, "logs", f"run-{date}.json")))
    n = len(act)
    fam = collections.Counter(r["family"] for r in act)
    dom = collections.Counter(r["company_domain"] for r in act)
    comp = collections.Counter(r["company"] for r in act)
    sk = collections.Counter(s for r in act for s in r["skills"])
    cov, modules = course_coverage(d)
    pct = lambda a, b: f"{a} ({round(100*a/b)}%)" if b else "0"
    L = []
    A = L.append
    A(f"# Summary report: game, real-time 3D and virtual-environment job listings, {date}")
    A(""); A("## Executive summary"); A("")
    ok = [s for s in log["sources"] if s["status"] == "ok"]
    A(f"**What this is.** A dated summary of {n} active job listings from {len(comp)} companies, collected to show what a master's student interested in games, real-time 3D or virtual environments could apply for, so the CSYE 7270 course (and any follow-on classes) can be designed around real roles. Families, skills, seniority and years are **AI-made proposals** from rules and a word list; {sum(1 for r in act if r['family_confirmed_by'])} of {n} have been confirmed by the course designer.")
    A(""); A(f"**Why read it.** It is a small sample from named company boards, not the market. It shows which kinds of jobs exist, which tools and skills their text names, and which of those the course materials do not mention.")
    A(""); A("**What it found.**")
    A(f"- The run read {log['postings_fetched']:,} postings from {len(ok)} company boards and kept {n} after rules for role family, game or 3D relevance and a {WINDOW_DAYS}-day window.")
    top = ", ".join(f"{k.replace('_',' ')} {v}" for k, v in fam.most_common(5))
    A(f"- Largest role families: {top}.")
    eng = {e: sum(1 for r in act if e in r["skills"]) for e in ("Unity", "Unreal Engine", "Godot")}
    A(f"- Engines named in the text: Unity in {pct(eng['Unity'], n)}, Unreal Engine in {pct(eng['Unreal Engine'], n)}, Godot in {pct(eng['Godot'], n)}.")
    figma = sum(1 for r in act if "Figma or design handoff" in r["skills"])
    figeng = sum(1 for r in act if "Figma or design handoff" in r["skills"] and any(e in r["skills"] for e in ("Unity", "Unreal Engine", "Godot")))
    A(f"- Figma or design handoff appears in {pct(figma, n)} of listings; with a named engine as well in {figeng}.")
    ent = sum(1 for r in act if r["early_career_title"] or (r["years_required"] is not None and r["years_required"] <= 2))
    A(f"- Early-career signal (an intern, new-grad, junior or associate title, or a stated minimum of 2 years or less): {pct(ent, n)}.")
    A(""); A(f"Records: `game-jobs/listings.jsonl` (append-only; take the last line per URL). Mentions mean the listing text uses a term, not that the role requires it.")
    A(""); A("## 1. What was read, and what it excluded"); A("")
    A("| Reason excluded | Count |"); A("|---|---:|")
    for k, v in sorted(log["excluded"].items(), key=lambda x: -x[1]): A(f"| {k} | {v} |")
    A(""); bad = [s for s in log["sources"] if s["status"] != "ok"]
    A(f"Boards that did not answer: {', '.join(s['company'] for s in bad) or 'none'}.")
    A(""); A("## 2. Role families (what someone could apply for)"); A("")
    A("| Family | Listings | Early-career signal | Example titles |"); A("|---|---:|---:|---|")
    for f, c in fam.most_common():
        rs = [r for r in act if r["family"] == f]
        e = sum(1 for r in rs if r["early_career_title"] or (r["years_required"] is not None and r["years_required"] <= 2))
        ex = "; ".join(sorted({r["title"] for r in rs})[:3])
        A(f"| {f.replace('_',' ')} | {c} | {e} | {ex[:110]} |")
    A(""); A("## 3. By kind of employer"); A("")
    A("| Employer type | Listings |"); A("|---|---:|")
    for k, v in dom.most_common(): A(f"| {k} | {v} |")
    A(""); A("Top companies: " + ", ".join(f"{k} {v}" for k, v in comp.most_common(10)) + ".")
    A(""); A("## 4. Skills named in the listings, with the course's coverage"); A("")
    A("Coverage is a keyword check of `modules/` in this course folder: the number of times the skill's terms appear in the module lessons. Zero means the lessons never use the term. It says nothing about quality.")
    A(""); A("| Skill | Group | Listings | Course modules mention |"); A("|---|---|---:|---:|")
    grp = {s["name"]: s["group"] for s in d["skills"]}
    for s, c in sk.most_common():
        cv = cov.get(s)
        A(f"| {s} | {grp[s]} | {pct(c, n)} | {'n/a' if cv is None else cv} |")
    zero = [s["name"] for s in d["skills"] if sk[s["name"]] == 0]
    if zero: A(""); A("Dictionary skills that matched no listing: " + ", ".join(zero) + ".")
    A(""); A("## 5. Gaps: skills in at least 15% of listings that the course materials never mention"); A("")
    gaps = [(s, c) for s, c in sk.most_common() if c / n >= 0.15 and cov.get(s) == 0]
    A("| Skill | Listings |"); A("|---|---:|")
    for s, c in gaps: A(f"| {s} | {pct(c, n)} |")
    if not gaps: A("| none | |")
    A(""); A("## 6. Skills by role family (top 8 each)"); A("")
    for f, _ in fam.most_common():
        rs = [r for r in act if r["family"] == f]
        c = collections.Counter(s for r in rs for s in r["skills"])
        A(f"**{f.replace('_', ' ')}** (n={len(rs)}): " + "; ".join(f"{s} {k}" for s, k in c.most_common(8)) + ".")
        A("")
    A("## 7. Seniority, years and pay where listed"); A("")
    sen = collections.Counter(r["seniority"] for r in act)
    A("Seniority (from title and years): " + ", ".join(f"{k} {v}" for k, v in sen.most_common()) + ".")
    ys = sorted(r["years_required"] for r in act if r["years_required"] is not None)
    A(f"Stated minimum years: {len(ys)} of {n} state one" + (f"; median {ys[len(ys)//2]}, range {ys[0]} to {ys[-1]}." if ys else "."))
    A(f"Pay is listed in {sum(1 for r in act if r['salary_listed'])} of {n}, in each posting's own currency and location tier, so ranges are not comparable one to one.")
    A(""); A("## 8. Fully remote or location"); A("")
    A("Remote flag set: " + str(sum(1 for r in act if r.get("remote"))) + f" of {n}. Most common locations: " + ", ".join(f"{k or 'unlisted'} {v}" for k, v in collections.Counter(r['location'] for r in act).most_common(6)) + ".")
    A(""); A("## What limits these results"); A("")
    for t in ("**Coverage.** Only boards on Greenhouse, Ashby and Lever that this tool can read. Many studios use their own career sites, Workday or other systems and are not seen: the large console and PC publishers are mostly missing.",
              "**Title rules.** Roles are classified by title patterns. A title that does not say what the job is (\"Engineer II\") is classified from its words alone and may be wrong.",
              "**Windows.** Only postings from the last %d days." % WINDOW_DAYS,
              "**AI-made fields.** Family, skills, years, seniority and salary come from rules and word lists and can miss or over-match.",
              "**Not pushed or sent.** Files are local. `raw/` holds full listing text and stays out of version control."):
        A(f"- {t}")
    out_path = os.path.join(HERE, "reports", f"summary-{date}{suffix}.md")
    if os.path.exists(out_path): sys.exit(f"refusing to overwrite {out_path}")     # a corrected report is a NEW file: use --suffix=-b
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote reports/summary-%s%s.md: %d active listings" % (date, suffix, n))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["collect", "report"])
    ap.add_argument("--date", default=TODAY)
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--suffix", default="")
    a = ap.parse_args()
    collect(a.date, a.no_fetch) if a.cmd == "collect" else report(a.date, a.suffix)
