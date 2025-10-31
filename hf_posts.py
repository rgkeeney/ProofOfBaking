from huggingface_hub import HfApi
import pprint as pp
import os
import csv
import argparse
import datetime
import traceback
import re
import sys
import json
from tqdm import tqdm
from datetime import datetime
from huggingface_hub.utils import HfHubHTTPError
from huggingface_hub import DiscussionComment
from dotenv import load_dotenv
import time

load_dotenv()
api=HfApi(token=os.getenv("HF_TOKEN"))
global ratelimitcounter

def get_repo_posts(repo_name, dump_path, weird_path):

    global ratelimitcounter
    if(ratelimitcounter<=5):
        time.sleep(300)
        ratelimitcounter=args.ratelimit
    postnum=1
    postlist=list()
    while True:
        try:
            fulldiscussion=api.get_discussion_details(repo_id=repo_name,repo_type="model", discussion_num=postnum,token=os.getenv("HF_TOKEN"))
            ratelimitcounter-=1
            infodict=dict()
            infodict['repo_id']=fulldiscussion.repo_id
            infodict['title']=fulldiscussion.title
            infodict['status']=fulldiscussion.status
            infodict['discussion_id']=postnum
            infodict['is_pull_request']=fulldiscussion.is_pull_request
            infodict['og_author']=fulldiscussion.author
            infodict['url']=fulldiscussion.url
            #shared info ends here
            #author, comment_id, create time, rawtext, language
            commentnum=1
            for event in fulldiscussion.events:
                if(type(event) is DiscussionComment):
                    commentdict=event.__dict__
                    commentdict['comment_id']=commentnum
                    #the amount of nested dicts is evil
                    commentdict.update(commentdict['_event'])
                    commentdict.update(commentdict['_event']['data'])
                    if(commentdict['author'] == "deleted"):
                        commentdict['name']=commentdict['author']
                    else:
                        authordict=commentdict['author'].copy()
                        authordict.pop('type')
                        commentdict.update(authordict)
                        commentdict.pop('_id')
                        commentdict.pop('avatarUrl')                        
                    commentdict.pop('author')                   
                    commentdict.pop('latest')
                    commentdict.pop('_event')
                    commentdict.pop('id')
                    commentdict.pop('editorAvatarUrls')
                    commentdict.pop('data')
                    #will want this back for more detailed analysis
                    if('relatedEventId' in commentdict):
                        commentdict.pop('relatedEventId')
                    if(commentdict['hidden']==True):
                        commentdict.pop('hiddenBy')
                        commentdict.pop('hiddenReason', None)
                    commentdict.update(infodict)
                    #add header for weird
                    if len(set(commentdict.keys()).difference(headers))>0:
                        with open(weird_path,"a") as f:
                            try:
                                json.dumps(commentdict)
                            except Exception as e:
                                print("error: ", e)
                            finally:
                                break

                    else:
                        with open(dump_path, 'a', newline='',encoding='utf-8') as f:
                            try:
                                writer=csv.DictWriter(f, fieldnames=headers)
                                writer.writerow(commentdict)
                            except Exception as e:
                                print("error: ", e)

                    """if(set(commentdict.keys())!= set(["type","created_at","content","edited","hidden","comment_id","createdAt","numEdits","identifiedLanguage","editors","reactions","isReport","_id","fullname","name","isPro","isHf","isHfAdmin","isMod","followerCount","isOwner","isOrgMember","repo_id","title","status","discussion_id","is_pull_request","og_author","url"])):
                        #write to janky jail file
                        with open(os.path.abspath(os.path.join(os.getcwd(),"hf_files","community",f"community_posts_bad.csv")),"a",newline='',encoding='utf-8') as f:
                            json.dumps(commentdict)"""
                    #postlist.append(commentdict)
                    commentnum+=1

                ratelimitcounter-=1

                    
            postnum+=1
        
        except HfHubHTTPError as e:
            ratelimitcounter-=1
            if e.response.status_code==404:
                if(postnum==1):
                    postlist.append({"repo_id":repo_name,"discussion_id":0,"status":"empty"})
                break
            elif e.response.status_code==410:
                postlist.append({"repo_id":repo_name,"discussion_id":postnum,"status":"deleted"})
                postnum+=1
            elif e.response.status_code==401:
                postlist.append({"repo_id":repo_name,"discussion_id":-1, "status": "private repository"})
                break
            elif e.response.status_code==429:
                print(f"ratelimited at model {repo_name}")
                sys.exit(0)
            elif e.response.status_code==403:
                postlist.append({"repo_id":repo_name,"discussion_id":0,"status":"discussions disabled"})
                break
            elif e.response.status_code==504:
                time.sleep(60)

            else:
                print("unexpected error: ", e.response)
                print(e)
                break
    return postlist


def main():
    global ratelimitcounter
    ratelimitcounter=args.ratelimit
    current_time=int(datetime.now().timestamp())
    filename, filetype = os.path.splitext(args.file)
    i,j=integers = [int(s) for s in re.findall(r'\d+', filename)]
    global dump_path
    dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","community",f"community_posts_{i}-{j}_{current_time}.csv"))
    global weird_path
    weird_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","community",f"community_posts_{i}-{j}_weird.json"))
    global headers
    headers=["type","created_at","content","edited","hidden","comment_id","createdAt","numEdits","identifiedLanguage","editors","reactions","isReport","_id","fullname","name","isPro","isHf","isHfAdmin","isMod","followerCount","isOwner","isOrgMember","repo_id","title","status","discussion_id","is_pull_request","og_author","url"]

    #headers=repo_discussions[0].keys()
    model_path=os.path.abspath(os.path.join(os.getcwd(),args.file))
    with open(model_path, 'r')as f:
        model_names=f.readlines()
        #TODO: should probably handle a json input as well
        #data=dict(json.load(f))
        #model_names=list(data.keys())
    all_discussions=list()
    with open(dump_path,"a",newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
    
    for model in tqdm(model_names, leave=False):
        discussions=get_repo_posts(model.strip(), dump_path, weird_path)
        #all_discussions.extend(discussions)
    print("finished run")


"""
    with open(dump_path,"a",newline='',encoding='utf-8') as f:
        headers=["type","created_at","content","edited","hidden","comment_id","createdAt","numEdits","identifiedLanguage","editors","reactions","isReport","_id","fullname","name","isPro","isHf","isHfAdmin","isMod","followerCount","isOwner","isOrgMember","repo_id","title","status","discussion_id","is_pull_request","og_author","url"]
        writer=csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
        for row in all_discussions:
            try:
                writer.writerow(row)
            except Exception as e:
                print("type: ", type(e))
                print("\n traceback: ")
                traceback.print_exc()
                continue

"""

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str,help="name of model file in hf_files")
    parser.add_argument("-r", "--ratelimit", type=int, default=500, help="huggingface api rate limit per 5 minutes, defaults to 500")
    args=parser.parse_args()
    main()
