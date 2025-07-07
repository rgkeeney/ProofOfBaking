from huggingface_hub import HfApi
from itertools import islice
import pprint as pp
import os
from dotenv import load_dotenv

load_dotenv()
api=HfApi(token=os.getenv("HF_TOKEN"))
models=api.list_models()
#m=list(iter(models))
def get_models(num_models=5):
    return_data=list(islice(models,num_models))
    model_data=list()
    for i in return_data:
        model_data.append(i.__dict__)
    return model_data
#m=get_models()
#pp.pprint(m)

def get_org_members(org):
    members = api.list_organization_members(org)
    member_data=list()
    print(next(members).num_likes)
    for i in members:
        member_data.append(i.__dict__)
    return member_data
#t=get_org_members("THUDM")
#pp.pprint(t)

############ Does NOT have the links to github, what is num_discussions??#####
def get_user_info(user):
    pp.pprint(api.get_user_overview(user))

#get_user_info("Stanislas")

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

get_user_gh("danielhanchen")

