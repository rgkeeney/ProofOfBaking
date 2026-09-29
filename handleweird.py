import argparse
import os
from pathlib import Path
from datetime import datetime
def main():
    parentdir=Path(os.path.dirname(os.getcwd()))
    outfiles=list(parentdir.glob('*.out'))
    for file in outfiles:
        print(file)
        repos=[]
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            try:
                for line in f:
                    if "weirdness at model" in line:
                        temp=line.split("weirdness at model")
                        repos.append(temp[1])
            except Exception as e:
                print(line)
                print(e)
        repos=list(dict.fromkeys(repos))
        with open(os.path.abspath(os.path.join(os.getcwd(),"hf_files", "model_id_subsets", f"rerun_models_{int(datetime.now().timestamp())}.txt")), 'a') as f:
            for repo in repos:
                f.write(repo)


main()
"""
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str,help="name of model file in hf_files")
    main()
"""