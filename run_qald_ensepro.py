import json
import os
import time
from timeit import default_timer as timer
from pathlib import Path


def save_as_json(value, filename, indent=2, sort_keys=False):
    import json
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






frases = []
frases = carregar_frases("qald7.txt")
frases = carregar_frases("qald7.txt")
frases = carregar_frases("qald7.txt")
frases = carregar_frases("qald7.txt")
frases = carregar_frases("qald7.txt")
frases = carregar_frases("qald7.txt")


print(frases)

primeira_palavra_frases = []

for frase in frases:
    primeira_palavra = frase.split(" ")[0]
    primeira_palavra_frases.append(primeira_palavra)
    # print(primeira_palavra)


print(primeira_palavra_frases)















exit()
jar = "C:\_ensepro\ensepro-answer-generator\ensepro-answer-generator-size-{size}.jar"
configs_file = "C:\\_ensepro\\ensepro-core\\ensepro\\configuracoes\\configs.json"
frases = carregar_frases("qald7.txt")
sizes = [10, 50, 75, 100, "base"]


for size in sizes:
    # update jar
    configs = json.loads(open(file=configs_file, mode="r", encoding="utf-8").read())
    configs["cbc"]["path_answer_generator"] = jar.format(size=size)
    save_as_json(configs, configs_file)
    path = "C:/_ensepro/ensepro-similarity-service/resultados/" + str(size) + "/"
    Path(path).mkdir(parents=True, exist_ok=True)
    i = 90
    for frase in frases:
        filename = "{:0>3d}-v2-s{size}-".format(i, size=size) + frase.replace("?", "")
        base_command = "python C:\_ensepro\ensepro-core\main\ensepro_main.py "
        params_command = "-save-json -filename \"{filename}\" -frase \"{frase}\" -resposta"

        final_command = base_command + params_command.format(frase=frase, filename=path + filename)

        start = time.time()
        os.system(final_command)
        end = time.time()

        try:
            response_file = json.loads(open(file=path + filename + ".json", mode="r", encoding="utf-8").read())

            if not response_file[0]["resposta"]:
                response_file[0]["resposta"] = {}

            response_file[0]["resposta"]["total_time"] = (end - start) * 1000  # converts to ms
            save_as_json(response_file, path + filename + ".json")
        except Exception as e:
            print(e)

        i += 1
