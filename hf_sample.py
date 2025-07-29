from huggingface_hub import HfApi
from itertools import islice
import pprint as pp
import os
from dotenv import load_dotenv

load_dotenv()
#api=HfApi(token=os.getenv("HF_TOKEN"))
api=HfApi()
#m=list(iter(models))
def get_models(num_models=5):
    models=api.list_models()
    return_data=list(islice(models,num_models))
    model_data=list()
    for i in return_data:
        model_data.append(i.__dict__)
    return model_data

def get_all_models(num_models=5):
    models=api.list_models(sort="created_at",direction=1,full=True,cardData=False,fetch_config=False)
    return_data=list(islice(models,num_models))
    model_data=list()
    for i in return_data:
        if(i["created_at"]=="datetime.datetime(2022, 3, 2, 23, 29, 4, tzinfo=datetime.timezone.utc)"):
            i["created_at"]=api.list_repo_commits(i["id"])[-1]
        model_data.append(i.__dict__)
    return model_data

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
    r=get_all_models(5)
    pp.pprint(r[4])
    #pp.pprint(api.list_repo_commits("google-bert/bert-base-uncased")[-1])