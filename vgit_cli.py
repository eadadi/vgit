#!/usr/bin/env python3
import typer
import vgit_api as api
import yaml
from yaml import CLoader as Loader, CDumper as Dumper

app = typer.Typer()

@app.command()
def init():
    """
    Create yaml file for the current super repo
    """
    return api.init_versions_file_for_curr_super_repo()


@app.command()
def ls():
    """
    Display all existing versions
    """
    try:
        versions = api.get_versions()
    except FileNotFoundError:
        print("Current repository was not initialized. run init command")
        return
    print(yaml.dump(versions))

@app.command()
def load(key: str):
    """
    Load the version corresponding to the argument (can be either the hash value or version name)
    """
    try:
        version = api.get_version_by_hash(key)
    except KeyError:
        version = api.get_version_by_name(key)
    except FileNotFoundError:
        print("Current repository was not initialized. run init command")
        return
    if version:
        print(yaml.dump(version))
    api.operation_load(version)

@app.command()
def unload(key: str):
    """
    Unload the version corresponding to the argument (can be either the hash value or version name)
    """
    try:
        version = api.get_version_by_hash(key)
    except KeyError:
        version = api.get_version_by_name(key)
    if version:
        print(yaml.dump(version))
    api.operation_unload(version)

@app.command()
def pull(key: str):
    """
    Pull rebase for version corresponding to the argument (can be either the hash value or version name)
    """
    try:
        version = api.get_version_by_hash(key)
    except KeyError:
        version = api.get_version_by_name(key)
    if version:
        print(yaml.dump(version))
    api.operation_pull(version)

@app.command()
def review(key: str):
    """
    Uploads patch to gerrit review system, The behaviour is to upload all commits of the version under a topic that holds the version name (i.e. "git review -t {version_name}")
    """
    try:
        version = api.get_version_by_hash(key)
    except KeyError:
        version = api.get_version_by_name(key)
    if version:
        print(yaml.dump(version))
    api.operation_review(version)

@app.command()
def add(name: str, load: str="", unload: str="", description: str="", identifier: str="", init: bool=False):
    """
    Adds a new version. add --help to see detailed example

    For example:

    add my_patch --description quick patch --load [action repo repo_branch..] --unload [branch branch..]

    --init will create those branches too
    --unload should be followed by list of branches to checkout in the same order as in --load
    """
    versions = api.get_versions()
    tmp = load.split()
    if len(tmp) % 3 != 0:
        print("repo/branch/action are missing")
        return

    action_repo_branch = [(tmp[i], tmp[i+1], tmp[i+2]) for i in range(0, len(tmp), 3)]
    unload_branches = unload.split()
    if len(unload_branches) != len(action_repo_branch):
        print("Number of branches on unload does not match number of repositories on load")
        return

    try:
        if identifier == "":
            new_version, identifier = make_version_and_hash(versions, name, description, action_repo_branch, unload_branches)
        else:
            new_version, identifier = make_version_and_hash(versions, name, description, action_repo_branch, identifier, unload_branches)
    except KeyError:
            print("There is an entry that already holds that version hash value. Consider using custom identifier")
            return

    add_version_to_super_repo(versions, new_version, identifier)
    if init:
        operation_load(new_version, init_flag = True)

if __name__ == "__main__":
    app()
