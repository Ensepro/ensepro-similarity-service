import json
import pandas


def load_json(file):
    return json.loads(open(file=file, mode="r", encoding="utf-8").read())


def save_as_json(value, filename, indent=2, sort_keys=False):
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


google_sheets_max_precision = 10
analyses = load_json("analyses/analysis.json")
rt = {}
tt = {}
ca = {}
ls1 = {}


ls2 = {}





sizes = ['base', '10', '50', '75', '100', '150', '200', '300', '400', '500', '600', '750', '1000']

for index1 in analyses:
    for column in analyses[index1]:
        rt[column] = rt.get(column, [])
        tt[column] = tt.get(column, [])
        ca[column] = ca.get(column, [])
        ls1[column] = ls1.get(column, [])
        ls2[column] = ls2.get(column, [])

for index in analyses:
    analysis = analyses[index]
    print(analysis)
    rt["frase"].append(analysis["frase"])
    tt["frase"].append(analysis["frase"])
    ca["frase"].append(analysis["frase"])
    ls1["frase"].append(analysis["frase"])
    ls2["frase"].append(analysis["frase"])

    for size in sizes:
        ranking_time = round(analysis[size].get("ranking_time", -1), google_sheets_max_precision)
        total_time = round(analysis[size].get("total_time", -1), google_sheets_max_precision)
        has_answer = analysis[size].get("has_answer", None)
        l1size = analysis[size].get("l1size", "-1")
        l2size = analysis[size].get("l2size", "-1")

        rt[size].append(ranking_time)
        tt[size].append(total_time)
        ca[size].append(has_answer)
        ls1[size].append(l1size)
        ls2[size].append(l2size)

tables = [
    {"name": "rt", "table": rt},
    {"name": "tt", "table": tt},
    {"name": "ca", "table": ca},
    {"name": "ls1", "table": ls1},
    {"name": "ls2", "table": ls2},
]

for table in tables:
    table_name = "analyses/table_{table}".format(table=table["name"])
    pandas.DataFrame(table["table"]).to_csv(table_name + ".csv", index=False)
    save_as_json(table["table"], table_name + ".json")
