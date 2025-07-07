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
    print(next(members))
    for i in members:
        member_data.append(i.__dict__)
    return member_data
#t=get_org_members("THUDM")
#pp.pprint(t)

import requests
url='https://huggingface.co/api/whoami-v2'
headers= {"authorization": f"Bearer {os.getenv("HF_TOKEN")}"}
r = requests.get(url, headers=headers)
pp.pprint(r.json())
############ accurate way to get followers##############
#print(list(api.list_user_following("akhaliq")))
