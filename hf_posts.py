from huggingface_hub import HfApi
import pprint as pp
import os
import json
import argparse
import datetime
from datetime import datetime
from huggingface_hub.utils import HfHubHTTPError

api=HfApi()
def get_all_posts(repo_name):
    postnum=1
    postlist=list()
    while True:
        try:
            fulldisc=api.get_discussion_details(repo_name,postnum)
            postlist.append(fulldisc.__dict__)
            postnum+=1
        
        except HfHubHTTPError as e:
            if(e.response.status_code==404):
                #print(f"found end at comment #{postnum-1}")
                break
            if(e.response.status_code==410):
                postlist.append({"num":postnum,"status":"deleted"})
                postnum+=1
            else:
                print(f"unexpected error: {e}")
                break
    return postlist
   

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("path", help="path to file holding repos")
    args=parser.parse_args()
    model_name="zai-org/GLM-4.5"
    with open(args.path, "r") as m:
        file=m.read()
        ids=json.loads(file).keys()
    repo_discussions=dict()
    for id in ids:
        repo_discussions[id]=get_all_posts(id)
    current_time=datetime.now().strftime("%y-%m-%d")
    dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","community",f"community_posts_{current_time}.json"))
    try:
        with open(dump_path,"w") as f:
            json.dump(repo_discussions,f,indent=4,default=str)
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"Successful write to {dump_path}")
    
if(__name__=="__main__"):
    main()