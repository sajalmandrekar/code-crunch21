import os
import requests


'''
Task 3: Get List of Github Issues filtered by labels
Write an API endpoint with the below signature, which will get all github issues linked to a repository and having specific label.

GET /github/issues/:author/:repo/:labels

where :author name of the person to whom the issue is assigned to
where :repo name of the repository
where :labels label associated with the issue

'''

'''
Task 4: Get List of Github Commits For a Repo within date range
Write an API endpoint with the below signature, get the list of commits on a repository within the specified date range.

GET /github/commits/:dates/:repo

where :dates date range separated by comma.YYYY-MM-DD,YYYY-MM-DD
where :repo_ is the name of the repository
Example:

GET http://localhost:3000/github/commits/2021-07-01,2021-08-30/microsoft%2Fvscode
'''

error_code = {
    "status": 404,
    "message": "resource not found",
}

base_url = "https://api.github.com"
#ACCESS_TOKEN = os.environ.get("GITHUB_TOKEN")


## checks if label in json matches passed parameter
def labelMatches(label,set_of_labels):

    for label_data in set_of_labels:
        if(label == label_data["name"]):
            return True
    return False

## https://api.github.com/repos/microsoft/vscode/issues?creator=OldStarchy
## endpoint: /repos/{owner}/{repo}/issues
## query: label, creator
## input as {owner}%2F{repo} (47)

def get_issues(repo,creator,label):
    split_list = repo.split("/")
    owner = split_list[0]
    repo = split_list[1]        #! could get index out of bound error
    endpoint = f"{base_url}/repos/{owner}/{repo}/issues"
    query = {"creator":creator,}

    resp = requests.get(endpoint,params=query)

    if resp.status_code in (200,202):

        output = []
        issues_data = resp.json()
        for issue in issues_data:

            if labelMatches(label,issue["labels"]) == True:

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

        return output
    else:
        return error_code,404