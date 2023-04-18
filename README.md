# vgit

## Desctiprion
* vgit is small tool to handle commits writing for projects that are composed by many git repositories.
* vgit is an index of versions, where versions are lists of repositories that a commit is relevant for

## Installation (TODO)
clone the repository, activate `vgit_install.sh` and then the variable `$vg` can be used to invoke the script

## Example
In the project super repository
`$vg init`
creates the yaml file that holds all commits associated with that super repo

then,
```
$vg add some_feature --load "checkout REPO1 BRANCH1 checkout REPO2 BRANCH2" --unload "master mainline" --description "A short description for that feature"
```
will create an entry in the yaml file that will allow later to load, unload this version:
```
$vg load some_feature
```

* Note that operation can be done both by the version hash value and by the version name. The reason for having hashes is to allow multiple names but still having unique identifier for a version


## Todo
* support the cherry-pick operation to allow more complex load schemes
