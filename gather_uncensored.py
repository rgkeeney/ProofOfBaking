#from hf_posts import get_repo_posts
#JK I need to rewrite the model scraping from scratch to include filters and ratelimiting
from huggingface_hub import HfApi
import pprint as pp
import os
import argparse
import datetime
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
import requests
def get_filtered_models(start:int, filters, limit, sort_method):
    #first model upload timestamp: 1646263744
    models=api.list_models(sort=sort_method,direction=-1, filter=filters, full=True,cardData=False,fetch_config=False)
    model_data=list()
    for m in models: 
        try:
            model=m.__dict__
            if(int(model['created_at'].timestamp())<start):
                break
            model.pop("siblings")
            model.pop("cardData")

            model_data.append(model)
        except Exception as e:
            print(f"Error: {e}")
    
    #for recordkeeping and minimizing redundant future scrapes
    current_time=int(datetime.now().timestamp())
    dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","uncensored",f"uncensored_models_{current_time}.csv"))
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
        








if(__name__=="__main__"):
    api=HfApi()
    parser=argparse.ArgumentParser()
    parser.add_argument("-t", "--timestamp", default=1646263744, help="Unix timestamp that the scraper will stop at. Defaults to first timestamp created at 1646263744")
    parser.add_argument("-r", "--ratelimit", type=int, default=500, help="huggingface api rate limit per 5 minutes, defaults to 500")
    parser.add_argument("-f", "--filters", default="uncensored", help="tags or other information to filter models by, defaults to uncensored")
    #TODO: check if filters are AND or OR
    parser.add_argument("-l", "--limit", default=50, help="limit on number of models to be returned, defaults to 50")
    parser.add_argument("-s", "--sort", default="created_at", help="sort method of models, defaults to creation date")
    #TODO: change file naming scheme to account for different filters

    args=parser.parse_args()
    get_filtered_models(args.timestamp, args.filters, args.limit, args.sort)
