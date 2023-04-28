# vgit

## Desctiprion

**vgit is small tool that helps writing commits that span on multi-repositories projects**

vgit holds yaml file for each super repo, that looks like:
~~~
c16cd48b9c67b9f8d510b14fd0c6c858fe57b47e:
  Description: modify failure log when second call is empty
  Name: 2nd_call_failure_log
  load:
  - action: checkout
    branch: next_release
    repo: repo1
  - action: checkout
    branch: developers_branch
    repo: repo2
  unload:
  - master
  - mainline
~~~
this file defines the way vgit loads each version (which is actually a collection of commits that are related to each other)

## Installation

- clone the repository
- invoke `vgit_install.sh`

## Example

Let's look on the following structure
~~~
-SUPER-REPO
	-REPO1
	-REPO2
~~~

In the project super repository initialize yaml file that will hold all versions with:

`vg init`

then, start working on a commit that is relevant both for REPO1 & REPO2 with:

~~~
vg add some_feature "checkout REPO1 BRANCH1 checkout REPO2 BRANCH2"
~~~

In this way, an entry that holds this information will be stored in the yaml file (and can be directly modified there, too). Since the `--init` flag was specified the branches will be created too, and this version will be loaded (meaning that the action specified will take place in the ordder specified)

if --init is specified the branches that indicate in the "load recipe" will be created and applied

To unload this change we can specify `--unload` flag followed by a list of default branches in the order that appears in the "load recipe"
Then, it is possible to do something like:

~~~
vg load some_feature
vg unload some_feature #later...
~~~

On some stage, there might be a need to diverge from the version. For example, there might be a need to make some changes that are needed for debug, or there might be another way to implement the commit that you want to consider. In this case, normally, one would go through all the commits that compound the change and will checkout to a new branches for this debug/tweak. with vgit, you can simply

~~~
vg clone some_feature some_feature_new_api
vg load some_feature_new_api
~~~

so that the cloned version will look like:
~~~
a16cd48b9c64b9f88510914fd0c6c858fe57b473:
  Description: A short description for that feature
  Name: some_feature_new_api
  load:
  - action: checkout
    branch: BRANCH1_clone
    repo: REPO1
  - action: checkout
    branch: BRANCH2_clone
    repo: REPO2
  unload:
  - master
  - mainline
~~~

* Note that load, etc can be done both by hash and by version name. Although, the unique identifier is the hash number

