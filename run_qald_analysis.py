import json


def load_json(file):
    return json.loads(open(file=file, mode="r", encoding="utf-8").read())


def save_as_json(value, filename, indent=2, sort_keys=False):
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


def carregar_frases(arquivo):
    frases = []
    with open(arquivo, mode="r", encoding="UTF-8") as frases_arquivo:
        for frase in frases_arquivo:
            frase = frase.replace("\n", "")
            if not frase:
                continue
            if frase.startswith("#"):
                continue
            frases.append(frase)

    return frases


data = {}
base_path = "C:\\_ensepro\\ensepro-similarity-service\\resultados\\{size}\\{:0>3d}-v2-s{size}-{frase}.json"
frases = carregar_frases("qald7.txt")
sizes = [10, 50, 75, 100, 150, 200, 300, 400, 500, 600, 750, 1000, "base"]

for size in sizes:
    i = 1

    for frase in frases:
        analysis = None
        if i not in data:
            data[i] = {}
        try:
            name = base_path.format(i, frase=frase.replace("?", ""), size=size)
            analysis = load_json(name)
        except Exception as e:
            analysis = [{"resposta": {"ranking_time": -1, "total_time": -1}}]
            print(e)
        print(size, i, frase)
        # print(analysis)
        # print(data)

        lsizes = analysis[0]["resposta"].get("l_sizes", [])
        lsizes_size = len(lsizes)
        data[i]["frase"] = frase
        data[i][size] = {}
        data[i][size]["ranking_time"] = analysis[0]["resposta"].get("ranking_time", -1)
        data[i][size]["total_time"] = analysis[0]["resposta"]["total_time"]
        if lsizes_size > 0:
            data[i][size]["l1size"] = lsizes[0]
            if lsizes_size > 1:
                data[i][size]["l2size"] = lsizes[1]

        correct_answers = analysis[0]["resposta"].get("correct_answer", None)
        data[i][size]["has_answer"] = len(correct_answers) > 0 if correct_answers is not None else "-1"

        i += 1

    save_as_json(data, "analyses/analysis.json")
