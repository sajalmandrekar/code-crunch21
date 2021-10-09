import os
import requests
from datetime import datetime


error_code = {
    "status": 404,
    "message": "resource not found",
}

base_url = "https://api.github.com"
#ACCESS_TOKEN = os.environ.get("GITHUB_TOKEN")


## checks if label in json matches passed parameter
'''
def labelMatches(label,set_of_labels):

    for label_data in set_of_labels:
        if(label == label_data["name"]):
            return True
    return False
'''
## https://api.github.com/repos/microsoft/vscode/issues?creator=OldStarchy
## endpoint: /repos/{owner}/{repo}/issues
## query: label, creator
## input as {owner}%2F{repo} (47)

def get_issues(owner,repo,creator,label):
    
    endpoint = f"{base_url}/repos/{owner}/{repo}/issues"
    query = {"creator":creator,"state":"all","label":label}

    resp = requests.get(endpoint,params=query,verify=False)

    if resp.status_code in (200,202):

        output = []
        issues_data = resp.json()
        for issue in issues_data:

            if issue["assignee"] is not None:
                assignee = issue["assignee"]["login"]
            else:
                assignee = None

            output.append({
                    "id": issue["id"],
                    "title": issue["title"],
                    "state": issue["state"],
                    "comments_count": issue["comments"],
                    "assignee": assignee
            })

        return output,200
    else:
        return error_code,404

###########################################################################
################### TASK 4 ################################################

'''
def inTimeRange(commit_date,start_date,end_date):

    list_commit_date = commit_date.split("-")
    list_start_date = start_date.split("-")
    list_end_date = end_date.split("-")

    try:
        commit_year,commit_month,commit_day = int(list_commit_date[0]),int(list_commit_date[1]),int(list_commit_date[2][0:2])
        start_year,start_month,start_day = int(list_start_date[0]), int(list_start_date[1]), int(list_start_date[2])
        end_year,end_month,end_day = int(list_end_date[0]),int(list_end_date[1]),int(list_end_date[2])

    except:
        return 404

    commit_time = commit_day + commit_month*32+ commit_year*32*32
    start_time = start_day + start_month*32 + start_year*32*32
    end_time = end_day + end_month*32 + end_year*32*32

    #print(start_time,commit_time,end_time)

    if(commit_time>=start_time and commit_time <= end_time):
        #print(True)
        return True
    else:
        #print(False)
        return False
'''
# repos/microsoft/vscode/commits?since=2021-07-01&until=2021-08-30

def get_commits(owner,repo,start_date,end_date):
    
    try:
        date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return error_code,404

    endpoint = f"{base_url}/repos/{owner}/{repo}/commits"
    query = {
        "since":start_date,
        "until":end_date
    }

    resp = requests.get(endpoint,params=query,verify=False)

    if resp.status_code in (200,202):

        repo_data = resp.json()
        output = []
        for repo in repo_data:
                output.append({
                    "node_id": repo["node_id"],
                    "message": repo["commit"]["message"],
                    "commiter_name": repo["commit"]["committer"]["name"],
                    "date": repo["commit"]["committer"]["date"]
                })
        
        return output,200
    else:
        return error_code,404


'''
commit_date = repo["commit"]["committer"]["date"]
            val = inTimeRange(commit_date,start_date,end_date)
            if val == 404:
                print("Invalid date input")
                return error_code,404
            if val == True:

'''