from portality.models import Record
import requests

query = {
    "query" : {
        "bool" : {
            "must_not" : {
                "term" : {"bibjson.link.type" : "local_fulltext"}
            }
        }
    },
    "size" : 100
}

results = Record.query(q=query)

for r in results:
    ftls = [f.get("url") for f in r.get("bibjson", {}).get("link", []) if f.get("type") == "fulltext"]
    for ftl in ftls:
        resp = requests.get(ftl)
