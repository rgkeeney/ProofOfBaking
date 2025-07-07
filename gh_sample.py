from reporoulette import IDSampler
from dotenv import load_dotenv
import os
import argparse
import pprint as pp
import json
load_dotenv() # Load variables from .env file

gh_token = os.getenv("GH_TOKEN")
def spin_the_wheel(n=50):
    # Initialize the sampler
    sampler = IDSampler(token=gh_token)
    # Get 50 random repositories
    repos = sampler.sample(n_samples=n)
    # Print basic stats
    print(f"Success rate: {sampler.success_rate:.2f}%")
    print(f"Samples collected: {len(repos)}")
    print(sampler.results)


import requests
def get_user_info(user):
    url=f"https://api.github.com/users/{user}"
    headers={"Authorization": f"Bearer {gh_token}"}
    r=requests.get(url, headers=headers)
    pp.pprint(r.json())


