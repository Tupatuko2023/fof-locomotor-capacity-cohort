#!/usr/bin/env python3
"""Map public CFF metadata to legacy Zenodo deposition metadata."""
import argparse, datetime as dt, json
from pathlib import Path
import yaml

def map_cff(data, operation_date=None):
    required = ("title", "authors", "abstract", "version", "license", "keywords", "type", "repository-code")
    missing = [key for key in required if not data.get(key)]
    if missing: raise ValueError(f"missing CFF fields: {', '.join(missing)}")
    if data["type"] != "software": raise ValueError("CFF type must be software")
    creators = []
    for author in data["authors"]:
        creator = {"name": f'{author["family-names"]}, {author["given-names"]}'}
        if author.get("affiliation"): creator["affiliation"] = author["affiliation"]
        if author.get("orcid"): creator["orcid"] = author["orcid"].removeprefix("https://orcid.org/")
        creators.append(creator)
    return {"metadata": {
        "upload_type": "software", "publication_date": operation_date or dt.date.today().isoformat(),
        "title": data["title"], "creators": creators, "description": data["abstract"],
        "version": str(data["version"]), "license": "mit" if data["license"] == "MIT" else data["license"], "keywords": data["keywords"],
        "related_identifiers": [{"identifier": data["repository-code"], "relation": "isSupplementTo", "resource_type": "software"}],
    }}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--cff",type=Path,default=Path("CITATION.cff")); p.add_argument("--output",type=Path,required=True); a=p.parse_args()
    result=map_cff(yaml.safe_load(a.cff.read_text(encoding="utf-8")))
    a.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("CFF_MAPPING=PASS")
if __name__ == "__main__": main()
