# vgit

## Desctiprion

** vgit is small tool that helps writing commits that span on multi-repositories projects **

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
vg add some_feature --load "checkout REPO1 BRANCH1 checkout REPO2 BRANCH2"\
--unload "master mainline"\
 --description "A short description for that feature"\
--init
~~~

In this way, an entry that holds this information will be stored in the yaml file (and can be directly modified there, too). Since the `--init` flag was specified the branches will be created too, and this version will be loaded (meaning that the action specified will take place in the ordder specified)

To unload this change we specified under the `--unload` flag the list of default branches. Then we can always just do:

~~~
vg load some_feature
~~~

to load this feature so we can work on it.

* Note that load, etc can be done both by hash and by version name. Although, the unique identifier is the hash number

