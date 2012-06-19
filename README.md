pypi2fedora
===========

Automate the migration of pypi packages to fedora packages
The workflow i am trying to automate is:
- create spec from pypi package (pypi2spec)
- Edit and more fully flesh out the spec file
- rpmbuild the spec
- rpmlint the srpm
- upload the spec and srpm to a webserver
- sumbit a bugzilla ticket for a package review
- add a comment with a successfuly koji build

A second script then automates this workflow:
- scm request
- checking in srpms and sources for each branch
- fedpkg build
- fedpkg update

