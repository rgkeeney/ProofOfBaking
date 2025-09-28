from huggingface_hub import HfApi
import pprint as pp
import os
import argparse
import datetime
import csv
import time
from datetime import datetime
from dotenv import load_dotenv

parser=argparse.ArgumentParser()
parser.add_argument("-t", "--timestamp", help="Unix timestamp that the scraper will stop at. First model created at 1646263744")

api=HfApi()
#this no longer works, keeping to revamp later
'''
def get_models(num_models=5):
    models=api.list_models()
    return_data=list(islice(models,num_models))
    model_data=list()
    for i in return_data:
        model_data.append(i.__dict__)
    return model_data
'''
def get_models_since(start:int):
    #first model upload timestamp: 1646263744
    models=api.list_models(sort="created_at",direction=-1,full=True,cardData=False,fetch_config=False)
    model_data=list()
    i=0
    for m in models: 
        try:
            model=m.__dict__
            if(int(model['created_at'].timestamp())<start):
                break
            model.pop("siblings")
            model.pop("cardData")
            #this is a way to get accurate creation dates, since huggingface didn't always track it themselves.
            #but also the API hates it currently
            #if(str(model["created_at"])=="2022-03-02 23:29:04+00:00"):
                #might not be perfectly accurate but close enough
            #    real_created_at=api.list_repo_commits(model["id"])[-1].__dict__
            #    model["created_at"]=real_created_at["created_at"]

            model_data.append(model)
            #time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
    
    #for recordkeeping and minimizing redundant future scrapes
    current_time=int(datetime.now().timestamp())
    dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files",f"model_metadata_{current_time}.csv"))
    try:
        with open(dump_path,"w",newline='',encoding='utf-8') as f:
            headers=model_data[0].keys()
            print(headers)
            writer=csv.DictWriter(f,fieldnames=headers)
            writer.writeheader()
            writer.writerows(model_data)
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"Successful write to {dump_path}")
        




def get_org_members(org):
    members = api.list_organization_members(org)
    member_data=list()
    print(next(members).num_likes)
    for i in members:
        member_data.append(i.__dict__)
    return member_data


############ Does NOT have the links to github, what is num_discussions??#####
def get_user_info(user):
    pp.pprint(api.get_user_overview(user))


import requests

def get_user_gh(user):
    from bs4 import BeautifulSoup
    source=requests.get(f"https://huggingface.co/{user}")
    sourcehtml=source.text
    soup = BeautifulSoup(sourcehtml, "html.parser")
    step1= soup.find(class_="SVELTE_HYDRATER", attrs={"data-target":"UserProfile"})
    step2=dict(step1.attrs)
    import json
    finaldict=json.loads(step2['data-props'])
    print(finaldict.keys())
    pp.pprint(finaldict)



if(__name__=="__main__"):
    args=parser.parse_args()
    get_models_since(int(args.timestamp))