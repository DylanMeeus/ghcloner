import os
import getpass
from github import Github


# I probably don't really need to use a custom class for this
class user_repository:
    def __init__(self, name, language, url):
        self.name = name
        self.language = language
        self.url = url

def fetch_repositories(g):
    language_repo = {}
    for repo in g.get_user().get_repos():
        if repo.fork:
            continue
        user_repo = user_repository(repo.name, repo.language, repo.clone_url)
        if repo.language in language_repo:
            language_repo[repo.language].append(user_repo)
        elif repo.language == None:
            if "Unknown" in language_repo:
                language_repo["Unknown"].append(user_repo)
            else:
                language_repo["Unknown"] = [user_repo]
        else:
            language_repo[repo.language] = [user_repo]
    return language_repo

def clone_repositories(username, password, repos):
    os.mkdir("Code/")
    failed_repos = []
    for language in repos.keys():
        print("Cloning repositories for " + language)
        os.mkdir("Code/" + language)
        repositories = repos[language]
        for repository in repositories:
            try: 
                print("Cloning repository: " + repository.name)
                os.mkdir("Code/"+language+"/"+repository.name)
                auth_url = "https://" + username + ":" + password + repository.url[len("https://"):]
                os.system("git clone " + repository.url + " ./Code/" + language + "/" + repository.name)
            except: 
                failed_repos.append(repository.url)
    for ex in failed_repos:
        print("failed to clone: " + ex)

if __name__ == '__main__':
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    g = Github(username, password)
    repositories = fetch_repositories(g)
    clone_repositories(username, password, repositories)
    print("done!")


    

