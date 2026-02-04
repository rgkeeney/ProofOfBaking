import argparse
repos=[]
def main():
    with open(args.file, "r", encoding="utf-8") as f:
        for line in f:
            temp=line.split("weirdness at model")

            if len(temp)>1:
                repos.append(temp[1])
    repos=list(dict.fromkeys(repos))
    print(len(repos))
    with open("hf_files/model_id_subsets/1100-1200kweird.txt", 'w') as f:
        for repo in repos:
            f.write(repo)



if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str,help="name of model file in hf_files")
    args=parser.parse_args()
    main()