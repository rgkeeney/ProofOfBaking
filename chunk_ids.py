import argparse
import os
from datetime import datetime 
import csv
import json
import math

def csv_chunk():
    model_path=os.path.abspath(os.path.join(os.getcwd(),args.file))
    model_ids=[]
    with open(model_path, 'r', encoding='utf-8')as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                model_ids.append(row[0])
    for i in range(0, len(model_ids), args.size):
        model_subset=model_ids[i:i+args.size]
        dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","model_id_subsets",f"ids_{i}-{i+len(model_subset)}.txt"))
        with open(dump_path, 'a') as f:
            for id in model_subset:
                f.write(f"{id}\n")
    print(f"{math.ceil(len(model_ids)/args.size)} new files cointaining {len(model_ids)} ids")



def txt_chunk():
    model_path=os.path.abspath(os.path.join(os.getcwd(),args.file))
    with open(model_path, 'r', encoding='utf-8')as f:
        model_ids=f.readlines()
    for i in range(0, len(model_ids), args.size):
        model_subset=model_ids[i:i+args.size]
        dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","model_id_subsets",f"ids_{i}-{i+len(model_subset)}.txt"))
        with open(dump_path, 'a') as f:
            for id in model_subset:
                f.write(id)
    print(f"{math.ceil(len(model_ids)/args.size)} new files cointaining {len(model_ids)} ids")

def json_chunk():
    model_path=os.path.abspath(os.path.join(os.getcwd(),args.file))
    with open(model_path, 'r')as f:
        data=dict(json.load(f))
        model_ids=list(data.keys())
    for i in range(0, len(model_ids), args.size):
        model_subset=model_ids[i:i+args.size]
        dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","model_id_subsets",f"ids_{i}-{i+len(model_subset)}.txt"))
        with open(dump_path, 'a') as f:
            for id in model_subset:
                f.write(f"{id}\n")
    print(f"{math.ceil(len(model_ids)/args.size)} new files containing {len(model_ids)} ids")



def main():
    current_time=int(datetime.now().timestamp())
    filename, filetype = os.path.splitext(args.file)
    os.makedirs(os.path.abspath(os.path.join(os.getcwd(),"hf_files","model_id_subsets")), exist_ok=True) 
    if (filetype==".csv"): 
        csv_chunk()
    elif(filetype==".json"):
        json_chunk()
    elif(filetype==".txt"):
        txt_chunk()
    else:
        print("file type unsupported, please enter a json, txt, or csv file")
        exit()




if(__name__=="__main__"):
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str,help="path to model metadata in hf_files")
    parser.add_argument("-s", "--size", type=int, default=100000, help="size of file chunks, defaults to 100,000")
    args=parser.parse_args()
    main()