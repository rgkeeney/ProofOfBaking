from huggingface_hub import HfApi
import pprint as pp
import os
import csv
import argparse
import datetime
import json
from tqdm import tqdm
from datetime import datetime
from huggingface_hub.utils import HfHubHTTPError
from huggingface_hub import DiscussionComment
import time


api=HfApi()
global ratelimitcounter
ratelimitcounter=500


def get_repo_posts(repo_name):

    global ratelimitcounter
    if(ratelimitcounter<=4):
        tqdm.write("\n ---------sleeping for ratelimit-------------- \n")
        for i in tqdm(range(300)):
            time.sleep(1)
        ratelimitcounter=500
    postnum=1
    postlist=list()
    while True:
        try:
            fulldiscussion=api.get_discussion_details(repo_name,postnum)
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
                    authordict=commentdict['author'].copy()
                    authordict.pop('type')
                    commentdict.pop('latest')
                    commentdict.update(authordict)
                    commentdict.pop('author')
                    #commentdict.pop('_id')
                    commentdict.pop('avatarUrl')
                    commentdict.pop('_event')
                    commentdict.pop('id')
                    commentdict.pop('editorAvatarUrls')
                    commentdict.pop('data')
                    #will want this back for more detailed analysis
                    if('relatedEventId' in commentdict):
                        commentdict.pop('relatedEventId')
                    commentdict.update(infodict)
                    postlist.append(commentdict)
                    commentnum+=1

                ratelimitcounter-=1

                    
            postnum+=1
        
        except HfHubHTTPError as e:
            ratelimitcounter-=1
            if(e.response.status_code==404):
                if(postnum==1):
                    postlist.append({"repo_id":repo_name,"discussion_id":0,"status":"empty"})
                    #print("no comments")
                #else:
                   #print(f"found end at comment #{postnum-1}")
                break
            if(e.response.status_code==410):
                postlist.append({"repo_id":repo_name,"discussion_id":postnum,"status":"deleted"})
                postnum+=1
            if(e.response.status_code==401):
                postlist.append({"repo_id":repo_name,"discussion_id":-1, "status": "private repository"})
                break
            if(e.response.status_code==429):
                print("hit ratelimit, ")
                print(e)
                time.sleep(20)

            #################TODO Handle 403#######################

            else:
                print("unexpected error: ", e.response)
                break
    return postlist


def main():
    batchstart=time.time()
    current_time=int(datetime.now().timestamp())
    dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","community",f"community_posts_{current_time}.csv"))
    #headers=repo_discussions[0].keys()
    model_path=os.path.abspath(os.path.join(os.getcwd(),"hf_files",args.file))
    with open(model_path, 'r')as f:
        data=dict(json.load(f))
        model_names=list(data.keys())
    all_discussions=list()
    def name_gen():
        for i in range(0, len(model_names),500):
            yield model_names[i:i+500]

    for chunk in tqdm(name_gen(),position=0, total=len(model_names)):
        for model in tqdm(chunk, position=1, leave=False):
            discussions=get_repo_posts(model)
            all_discussions.extend(discussions)





    try:
         with open(dump_path,"a",newline='',encoding='utf-8') as f:
            headers=all_discussions[0].keys()
            writer=csv.DictWriter(f,fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_discussions)
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"Successful write to {dump_path}")


if(__name__=="__main__"):
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str,help="name of model file in hf_files")
    parser.add_argument("-r", "--ratelimit", type=int, default=500, help="huggingface api rate limit per 5 minutes, defaults to 500")
    args=parser.parse_args()
    main()
