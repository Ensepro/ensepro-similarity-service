import json


qald_file = "C:\\_ensepro\\datasets\\phases\\qald7.json"

qald = json.loads(open(
    file=qald_file,
    mode="r",
    encoding="utf-8"
).read())

# print(qald)


for question in qald["questions"]:
    for q in question["question"]:
        if q["language"] == "pt_BR":
            print(q["string"])

