import csv, re, os

STOP = {"inc","llc","corp","corporation","co","company","the","and","systems","system",
        "services","service","group","ltd","lp","llp","plc","incorporated","pc"}

def norm_name(s):
    if not s: return ""
    s = s.lower()
    s = s.replace("&"," and ")
    s = re.sub(r"[^a-z0-9]+"," ", s)
    toks = [t for t in s.split() if t and t not in STOP]
    return "".join(toks)

def norm_domain(d):
    if not d: return ""
    d = d.strip().lower()
    d = re.sub(r"^https?://","",d)
    d = re.sub(r"^www\.","",d)
    d = d.split("/")[0].split("?")[0].strip()
    if not d or "." not in d: return ""
    return d

def read(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

D="data/"

FOOT={"ME","NH","VT","MA","RI","CT","NY","NJ","PA","DE","MD","DC","VA"}
_SMAP={"maine":"ME","new hampshire":"NH","vermont":"VT","massachusetts":"MA","rhode island":"RI",
"connecticut":"CT","new york":"NY","new jersey":"NJ","pennsylvania":"PA","delaware":"DE",
"maryland":"MD","district of columbia":"DC","disctrict of columbia":"DC","washington dc":"DC",
"virginia":"VA","west virginia":"WV","new york city":"NY"}
def norm_state(s):
    if not s: return ""
    t=s.strip()
    if len(t)==2: return t.upper()
    return _SMAP.get(t.lower(), t.upper() if len(t)==2 else t)

# Strict normalizer: only legal-form suffixes and punctuation. Keeps systems/services/group,
# so "Excel Security Systems" does NOT collide with "Excel Security".
STOP_LIGHT = {"inc","llc","corp","corporation","co","company","the","ltd","lp","llp","incorporated","pc"}
def norm_name_strict(s):
    if not s: return ""
    s = s.lower().replace("&"," and ")
    s = re.sub(r"[^a-z0-9]+"," ", s)
    return "".join(t for t in s.split() if t and t not in STOP_LIGHT)
