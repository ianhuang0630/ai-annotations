import os
import json
import pandas as pd

# input_dir =  "Output7"
# output_file = "out6.csv"

def cleanup(input_dir: str,
            output_file: str): 

    files = os.listdir(input_dir)
    files = sorted([os.path.join(input_dir, f) for  f in files])

    dataframe = {
        "sampleID":[],
    }

    counter = 0
    for fi in files:
        with open(fi, "r") as f:
            d = json.load(f)

        dataframe["sampleID"].append(os.path.basename(fi)[:-len(".json")])

        for key in d:
            if isinstance(d[key], dict):
                for subkey in d[key]:
                    columname = key+"_"+subkey
                    # add data
                    if columname not in dataframe:
                        dataframe[columname] = [None] * counter
                    dataframe[columname].append(d[key][subkey])
            else:
                columname = key
                if columname not in dataframe:
                    dataframe[columname] = [None] * counter
                dataframe[columname].append(d[key])
        counter += 1

    df = pd.DataFrame(dataframe)
    df.to_csv(output_file)
    return output_file
