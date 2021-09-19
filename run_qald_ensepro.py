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

base_jar = "C:\_ensepro\ensepro-answer-generator\ensepro-answer-generator-size-{size}.jar"
configs_file = "C:\\_ensepro\\ensepro-core\\ensepro\\configuracoes\\configs.json"
frases = carregar_frases("qald7.txt")
jars_type = ["base", "slm1"]
slm1_only_l1_options = [True, False]
sizes = [10, 50, 75, 100, 150, 200, 300, 400, 500, 750, 1000, 2000, 3000, 4000]

for jar in jars_type:
    for slm1_only_l1 in slm1_only_l1_options:
        for size in sizes:
            # update jar
            configs = json.loads(open(file=configs_file, mode="r", encoding="utf-8").read())

            configs["cbc"]["path_answer_generator"] = base_jar.format(size=jar)
            configs["cbc"]["slm1_factor"] = size
            configs["cbc"]["slm1_factor_only_l1"] = slm1_only_l1

            save_as_json(configs, configs_file)
            path = "C:/_ensepro/ensepro-similarity-service/resultados2/"+str(jar)+ "/"+str(slm1_only_l1)+"/"+str(size)
            Path(path).mkdir(parents=True, exist_ok=True)
            
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
