#!/usr/bin/env python3
"""Validate XML sitemaps and sitemap indexes locally."""
import argparse,json,re
from datetime import date,datetime
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
def local(tag):return tag.rsplit("}",1)[-1]
def valid_lastmod(value):
    try:datetime.fromisoformat(value.replace("Z","+00:00"));return True
    except ValueError:
        try:date.fromisoformat(value);return True
        except ValueError:return False
def validate(data):
    root=ET.fromstring(data);kind=local(root.tag)
    if kind not in ("urlset","sitemapindex"):raise ValueError("root must be urlset or sitemapindex")
    entries=[];issues=[];seen=set()
    wanted="url" if kind=="urlset" else "sitemap"
    for idx,node in enumerate(x for x in root if local(x.tag)==wanted,1):
        fields={local(c.tag):((c.text or "").strip()) for c in node}
        loc=fields.get("loc","")
        parsed=urlparse(loc)
        if parsed.scheme not in ("http","https") or not parsed.netloc:issues.append({"level":"error","item":idx,"message":"loc must be an absolute HTTP(S) URL"})
        if loc in seen:issues.append({"level":"warning","item":idx,"message":"duplicate loc"})
        seen.add(loc)
        if "lastmod" in fields and not valid_lastmod(fields["lastmod"]):issues.append({"level":"warning","item":idx,"message":"invalid lastmod"})
        entries.append({"loc":loc,"lastmod":fields.get("lastmod"),"changefreq":fields.get("changefreq"),"priority":fields.get("priority")})
    if not entries:issues.append({"level":"warning","item":0,"message":"no sitemap entries found"})
    return {"kind":kind,"count":len(entries),"entries":entries,"issues":issues}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("file",type=Path);p.add_argument("--json",action="store_true");a=p.parse_args()
    try:r=validate(a.file.read_bytes())
    except (OSError,ET.ParseError,ValueError) as e:p.error(str(e))
    if a.json:print(json.dumps(r,indent=2));return
    print(f"{r['kind']}: {r['count']} entries")
    for x in r["issues"]:print(f"{x['level'].upper()} item {x['item']}: {x['message']}")
    if not r["issues"]:print("No structural issues found.")
if __name__=="__main__":main()
