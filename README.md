# vgit

## Desctiprion
* vgit is small tool to handle commits writing for projects that are composed by many git repositories.
* vgit is an index of versions, which are lists of repositories that define a commit

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

To unload this change we specified under the `--unload` flag the list of default branches. Then we can do:

~~~
vg load some_feature
~~~

* Note that load, etc can be done both by hash and by version name. The reason is to allow multiple names but still having unique identifier for a version


## Todo
* support the cherry-pick operation to allow more complex load schemes
