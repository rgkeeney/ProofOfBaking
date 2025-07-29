from huggingface_hub import HfApi
import pprint as pp
import os
import json
import datetime
from datetime import datetime
from dotenv import load_dotenv

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
def get_all_models():
    models=api.list_models(sort="created_at",direction=1,full=True,cardData=False,fetch_config=False)
    model_data=dict()
    for dummy in models: 
        model=next(models).__dict__
        #this is a way to get accurate creation dates, since huggingface didn't always track it themselves.
        if(str(model["created_at"])=="2022-03-02 23:29:04+00:00"):
            #might not be perfectly accurate but close enough
            real_created_at=api.list_repo_commits(model["id"])[-1].__dict__
            model["created_at"]=real_created_at["created_at"]
        
        model_data[model["id"]]=model
    #for recordkeeping and minimizing redundant future scrapes
    current_time=datetime.now().strftime("%y-%m-%d")
    dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files",f"model_metadata_{current_time}.json"))
    try:
        with open(dump_path,"w") as f:
            json.dump(model_data,f,indent=4,default=str)
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




#if(__name__=="__main__"):
#    get_all_models()