# jira_client.py
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()  # Loads .env variables

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_AUTH = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


# def create_issue(project_key, summary, description, issue_type):
#     url = f"{JIRA_BASE_URL}/rest/api/3/issue"
#     payload = {
#         "fields": {
#             "project": {"key": project_key},
#             "summary": summary,
#             "description": description,
#             "issuetype": {"name": issue_type}
#         }
#     }
#     response = requests.post(url, json=payload, headers=HEADERS, auth=JIRA_AUTH)
#     response.raise_for_status()
#     data = response.json()
#     issue_key = data["key"]
#     return {
#         "issue_key": issue_key,
#         "issue_url": f"{JIRA_BASE_URL}/browse/{issue_key}"
#     }

#. =========================. 

# def create_issue(project_key, summary, description, issue_type):
#     url = f"{JIRA_BASE_URL}/rest/api/3/issue"
#     payload = {
#         "fields": {
#             "project": {"key": project_key},
#             "summary": summary,
#             "description": description,  # ✅ Just a plain string
#             "issuetype": {"name": issue_type}
#         }
#     }

#     response = requests.post(url, json=payload, headers=HEADERS, auth=JIRA_AUTH)
    
#     if not response.ok:
#         print("Jira error:", response.status_code, response.text)  # Keep this for debugging

#     response.raise_for_status()
#     data = response.json()
#     issue_key = data["key"]
#     return {
#         "issue_key": issue_key,
#         "issue_url": f"{JIRA_BASE_URL}/browse/{issue_key}"
#     }


def create_issue(project_key, summary, description_text, issue_type):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"

    description_adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": description_text
                    }
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description_adf,
            "issuetype": {"name": issue_type}
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS, auth=JIRA_AUTH)
    
    if not response.ok:
        print("Jira error:", response.status_code, response.text)

    response.raise_for_status()
    data = response.json()
    return {
        "issue_key": data["key"],
        "issue_url": f"{JIRA_BASE_URL}/browse/{data['key']}"
    }


# jira_client.py (add below create_issue)
def search_issues(jql_query, max_results=5):
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    params = {
        "jql": jql_query,
        "maxResults": max_results,
        "fields": "key,summary,status"
    }
    response = requests.get(url, headers=HEADERS, auth=JIRA_AUTH, params=params)
    response.raise_for_status()
    data = response.json()
    
    results = []
    for issue in data.get("issues", []):
        key = issue["key"]
        summary = issue["fields"]["summary"]
        status = issue["fields"]["status"]["name"]
        results.append(f"{key}: {summary} [Status: {status}]")
    return results


def get_transitions(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    response = requests.get(url, headers=HEADERS, auth=JIRA_AUTH)
    response.raise_for_status()
    return response.json()["transitions"]

def transition_issue(issue_key, target_status):
    transitions = get_transitions(issue_key)
    
    # Match user input status (case-insensitive)
    matching = next((t for t in transitions if t["name"].lower() == target_status.lower()), None)
    
    if not matching:
        raise ValueError(f"No available transition matches status: {target_status}")

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    payload = {
        "transition": {
            "id": matching["id"]
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS, auth=JIRA_AUTH)
    response.raise_for_status()
    return {
        "message": f"Issue {issue_key} successfully transitioned to '{target_status}'"
    }