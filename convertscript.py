import os
import io
import pandas as pd
import ijson
import csv
import json
import itertools
import pprint as pp

def convert(path):
    with open(path, 'rb') as jf, open("model_metadata_25-07-30.csv", "w", newline='', encoding='utf-8') as cf:
        writer=csv.writer(cf)
        headers=['id', 'author', 'sha', 'last_modified', 'created_at', 'private', 'gated', 'disabled', 'downloads', 'downloads_all_time', 'likes', 'library_name', 'gguf', 'inference', 'tags', 'pipeline_tag', 'mask_token', 'trending_score', 'transformers_info', 'spaces', 'safetensors', 'security_repo_status', '_id', 'modelId']
        
        writer.writerow(headers)
        for dump, entry in ijson.kvitems(jf, ""):
            row=[entry.get(val) if val is not None else "test" for val in headers ]
            writer.writerow(row)

