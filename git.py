from github import Github
from github import Organization
import json

"""
This script prints everything on the console.

"""
orgs = [] # array of strings

g = Github("user","pass")
for org in orgs:
    orgz = g.get_organization(org)

    repos = orgz.get_repos()
    print ("Repo Org Name, Hook URL")
    for repo in repos:
        repo_name = repo.full_name
        for hook in repo.get_hooks():
            config_raw = hook._config.__dict__
            config_raw = json.dumps(config_raw)
            parsed_config = json.loads(config_raw)
            if 'value' in parsed_config:
                val = parsed_config['value']
                if 'url' in val:
                    url = parsed_config['value']['url']
                    print(repo_name + ", " + url)
