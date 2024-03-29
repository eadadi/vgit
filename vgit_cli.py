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
def ls(name: str="", minimal: bool=True, oneline: bool=True):
    """
    Display some/all versions

    --name: specify to show specific versions, can be partial name too
    --minimal: print only name and branches
    --oneline: each version output spans on one line (ignored if --no-minimal)
    """
    try:
        versions = api.get_versions()
    except FileNotFoundError:
        print("Current repository was not initialized. run init command")
        return
    
    if name!="":
        try:
            version = api.get_version_by_hash(name)
            versions = {name: version}
        except KeyError:
            try:
                version = api.get_version_by_name(name)
                versions = {"default_identifier": version}
            except KeyError as e:
                print(e)
                if name in e.args[0]:
                    versions = api.get_versions()
                    filtered = {}
                    for key in versions:
                        if name in versions[key]["Name"]:
                            filtered[key] = versions[key]
                    versions = filtered
                else:
                    return


    if not minimal:
        print(yaml.dump(versions))
        return
    for key in versions:
        version = versions[key]
        if not oneline:
            print("{}:".format(version["Name"]))
            for step in version["load"]:
                print("\t{}:{}".format(step["repo"],step["branch"]))
        else:
            branch_repos = ", ".join(["{}({})".format(step["repo"], step["branch"]) for step in version["load"]])
            print ("{}: {}".format(version["Name"], branch_repos))


@app.command()
def load(key: str, quiet: bool=False):
    """
    Loads a version (can be either hash value or version name)
    """
    try:
        version = api.get_version_by_hash(key)
    except KeyError:
        try:
            version = api.get_version_by_name(key)
        except KeyError as e:
            print(e)
            return
    except FileNotFoundError as e:
        print(e)
        return
    if version and not quiet:
        print(yaml.dump(version))
        api.operation_load(version)


@app.command()
def unload(key: str):
    """
    Unload version corresponding to the argument. It is not assert that the specified version was loaded.
    """
    try:
        version = api.get_version_by_hash(key)
    except KeyError:
        try:
            version = api.get_version_by_name(key)
        except KeyError as e:
            print(e)
    if version:
        print(yaml.dump(version))
    try:
        api.operation_unload(version)
    except KeyError as e:
        print(e)

@app.command()
def pull(key: str):
    """
    Pull rebase a version (can be either hash value or version name)
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
    Uploads patch to gerrit review system, with the version name as a topic name (i.e. "git review -t {version_name}")

    Note that this commands assume that all repositories in this version supposed to be upload to gerrit.
    For better granularity, update upload_cmd for each component, and use --upload cmd (not supported yet)
    """
    try:
        version = api.get_version_by_hash(key)
    except KeyError:
        version = api.get_version_by_name(key)
    if version:
        print(yaml.dump(version))
    api.operation_review(version)

@app.command()
def add(name: str, load: str=typer.Argument(...), unload: str="", description: str="", identifier: str="", init: bool=False):
    """
    Adds a new version. --help to see detailed example

    For example:

    add my_patch "action repo repo_branch.." --description quick patch  --unload [branch branch..]

    --init will create those branches too
    --unload should be followed by list of branches to checkout in the same order as in --load
    """
    versions = api.get_versions()
    tmp = load.split()
    if len(tmp) % 3 != 0:
        print("repo/branch/action are missing")
        return

    action_repo_branch = [(tmp[i], tmp[i+1], tmp[i+2]) for i in range(0, len(tmp), 3)]

    if unload != "":
        unload  = unload.split()
        if len(unload) != len(action_repo_branch):
            print("Number of branches on unload does not match number of repositories on load")
            return

    try:
        if identifier == "":
            new_version, identifier = api.make_version_and_hash(versions, name, description, action_repo_branch, unload)
        else:
            new_version, identifier = api.make_version_and_hash(versions, name, description, action_repo_branch, identifier, unload)
    except KeyError:
            print("There is an entry that already holds that version hash value. Consider using custom identifier")
            return

    api.add_version_to_super_repo(versions, new_version, identifier)
    if init:
        api.operation_load(new_version, init_flag = True)

@app.command()
def clone(name: str, clone_name: str, clone_suffix: str="_clone"):
    """
    Clones a new version out of a given one, for example, for debug purposes.

    Note that the branches of the cloned version should be exists before cloning

    If --clone_suffix is not given, the cloned branches names is {name}_clone.
    """

    versions = api.get_versions()
    try:
        version = api.get_version_by_name(name)
    except KeyError:
        print("No version with this name")
        return
    for stage in version["load"]:
        clone_branch_name = stage["branch"] + clone_suffix

        api.do_checkout(stage, init_flag=False)
        stage["branch"] = clone_branch_name
        api.do_checkout(stage, init_flag=True)

    import hashlib
    identifier = hashlib.sha1(yaml.dump(version).encode('utf-8')).hexdigest()

    version["Name"] = clone_name
    api.add_version_to_super_repo(versions, version, identifier)
    print("clone done")


if __name__ == "__main__":
    app()
