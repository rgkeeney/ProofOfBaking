from reporoulette import IDSampler
from dotenv import load_dotenv
import os
import argparse
load_dotenv() # Load variables from .env file

gh_token = os.getenv("GH_TOKEN")
# Initialize the sampler
sampler = IDSampler(token=gh_token)

# Get 50 random repositories
repos = sampler.sample(n_samples=50)

# Print basic stats
print(f"Success rate: {sampler.success_rate:.2f}%")
print(f"Samples collected: {len(repos)}")