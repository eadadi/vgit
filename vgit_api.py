import os
import yaml
from yaml import CLoader as Loader, CDumper as Dumper
import git
import hashlib

HOME_FOLDER = "{}/vgit".format(os.path.expanduser("~"))

def init_versions_file_for_curr_super_repo():
    if not os.path.exists(HOME_FOLDER):
        print("[First invoke]: Create versions folder in {}, all versions yaml file will appear there".format(HOME_FOLDER))
        os.makedirs(HOME_FOLDER)
    cwd = os.path.basename(os.getcwd())
    filename = "{0}/{1}.yaml".format(HOME_FOLDER, cwd)
    versions_file = open(filename, "a").close()
    print("Version file {} created".format(filename))

def load_versions_of_current_super_repo():
    cwd = os.path.basename(os.getcwd())
    try:
        versions_file = open("{0}/{1}.yaml".format(HOME_FOLDER, cwd), "r")
    except FileNotFoundError:
        print("versions file {0}/{1}.yaml was not founded. run init".format(HOME_FOLDER, cwd))
        return
    versions = yaml.load(versions_file.read(), Loader=Loader)
    return versions

def write_super_repo_versions_to_file(versions):
    cwd = os.path.basename(os.getcwd())
    versions_file = open("{0}/{1}.yaml".format(HOME_FOLDER, cwd), "w")
    versions_file.write(yaml.dump(versions))
    versions_file.close()

def get_versions():
    versions = load_versions_of_current_super_repo()
    return versions

def get_version_by_hash(hash_value):
    versions = load_versions_of_current_super_repo()
    return versions[hash_value]

def get_version_by_name(name):
    versions = load_versions_of_current_super_repo()
    names = [(key, versions[key]["Name"]) for key in versions]
    filtered_names = list(filter(lambda t: t[1] == name, names))
    if len(filtered_names) == 0:
        raise KeyError("No version has this name..")
    if len(filtered_names) > 1:
        print(filtered_names)
        raise KeyError("Multiple versions have this name..\n{}".format(filtered_names))
    return versions[filtered_names[0][0]]

def dump_version_by_hash(hash_value):
    return yaml.dump(find_version_by_hash(hash_value))

def do_checkout(stage, init_flag):
    repo = git.Repo(stage["repo"]).git
    if not init_flag:
        return repo.checkout(stage["branch"])
    else:
        return repo.checkout("HEAD", b=stage["branch"])

def do_cherrypick(stage, init_flag):
    g = git.cmd.Git()
    return g.execute(["git","cherry-pick","-n", stage["branch"]])

def do_pull(stage, init_flag=False):
    repo = git.Repo(stage["repo"]).git
    return repo.pull("--rebase")

def do_review(stage, version_name):
    g = git.cmd.Git()
    output = g.execute(["git","review","-t", version_name])
    return output

supported_actions = {
        "checkout": do_checkout,
        "pull": do_pull,
        "review": do_review,
        "cherry-pick": do_cherrypick
        }

def operation_review(version, init_flag = False):
    load_stages = version["load"]
    for stage in load_stages:
        stage_action = stage["action"]
        output = do_review(stage, version["Name"])
        print("On repo {}:".format(stage["repo"]).center(60,"="))
        print(output)

def operation_load(version, init_flag = False):
    load_stages = version["load"]
    for stage in load_stages:
        stage_action = stage["action"]
        output = supported_actions[stage_action](stage, init_flag)
        print("On repo {}:".format(stage["repo"]).center(60,"="))
        print(output)

def operation_unload(version):
    unload_branches = version["unload"]
    for idx, stage in enumerate(version["load"]):
        stage["branch"] = unload_branches[idx]
    return operation_load(version)

def operation_pull(version):
    load_stages = version["load"]
    for stage in load_stages:
        stage_action = stage["action"]
        output = supported_actions["pull"](stage)
        print("On repo {}:".format(stage["repo"]).center(60,"="))
        print(output)

def make_version_and_hash(versions, name, description, action_repo_branch, unload_branches, identifier=None):
    version = {
            "Name": name,
            "Description": description,
            "load": [
                {
                "action": action,
                "repo": repo,
                "branch": branch
                } for action, repo, branch in action_repo_branch],
            "unload": [branch for branch in unload_branches]
            }

    if identifier == None:
        version_string = yaml.dump(version)
        hash_value = hashlib.sha1(version_string.encode('utf-8')).hexdigest()
        if versions != None and hash_value in versions:
            raise KeyError
        identifier = hash_value
    return (version, identifier)

def add_version_to_super_repo(versions, version, identifier):
    if versions == None:
        versions = {}
    versions[identifier] = version
    write_super_repo_versions_to_file(versions)
