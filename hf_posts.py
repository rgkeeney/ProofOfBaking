from huggingface_hub import HfApi
import pprint as pp
import os
import csv
import argparse
import datetime
from datetime import datetime
from huggingface_hub.utils import HfHubHTTPError
from huggingface_hub import DiscussionComment

api=HfApi()

def get_repo_posts(repo_name):
    postnum=1
    postlist=list()
    while True:
        try:
            fulldiscussion=api.get_discussion_details(repo_name,postnum)
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
                    #print(commentdict.keys())
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

                    
            postnum+=1
        
        except HfHubHTTPError as e:
            if(e.response.status_code==404):
                #print(f"found end at comment #{postnum-1}")
                break
            if(e.response.status_code==410):
                postlist.append({"discussion_id":postnum,"status":"deleted"})
                postnum+=1
            else:
                print(f"unexpected error: {e}")
                break
    return postlist
   

def main():
    #parser=argparse.ArgumentParser()
    #parser.add_argument("path", help="path to file holding repos")
    #args=parser.parse_args()
    model_name="zai-org/GLM-4.5"
    #with open(args.path, "r") as m:
    #    file=m.read()
    #    ids=json.loads(file).keys()
    repo_discussions=list()
    repo_discussions=get_repo_posts(model_name)
    current_time=datetime.now().timestamp()
    dump_path = os.path.abspath(os.path.join(os.getcwd(),"hf_files","community",f"community_posts_{current_time}.csv"))
    '''
    for comment in repo_discussions:
        if(comment['status'] !='deleted'):
            #print(comment['type'])
            print(comment.keys())
    '''
    try:
         with open(dump_path,"w",newline='',encoding='utf-8') as f:
            headers=repo_discussions[0].keys()
            writer=csv.DictWriter(f,fieldnames=headers)
            writer.writeheader()
            writer.writerows(repo_discussions)
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"Successful write to {dump_path}")

if(__name__=="__main__"):
    main()