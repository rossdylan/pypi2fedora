from pbs import vim, rpmbuild, pypi2spec, scp, ssh
import os
import os.path
import sys
from rpm import TransactionSet


def getSpecPath(package):
    """
    Return the spec file for a specific pypi package

    :type package: str
    :param package: The package used to find a spec file
    """

    return os.path.expanduser("~/rpmbuild/SPECS/{0}.spec".format(package))

def editSpecFile(package):
    """
    Use pypi2spec to setup a barebones spec for a pypi package

    :type package: str
    :param package: The package to download with pypi2spec
    """

    pypi2spec(package)
    vim(getSpecPath(package), _fg=True)

def listSRPMS():
    """
    Get the list of srpms in ~/rpmbuild/SRPMS
    """

    return os.listdir(os.path.expanduser("~/rpmbuild/SRPMS"))

def getSRPMHead(spec):
    """
    Get the begining of an srpm file name based on a rpm spec

    :type spec: str
    :param spec: Spec file to parse
    """

    ts = TransactionSet()
    spec_obj = ts.parseSpec(spec)
    spec_headers = spec_obj.packages[0].header
    head = "{0}-{1}".format(
            spec_headers.format("%{name}"),
            spec_headers.format("%{version}")
            )
    return head

def getSRPMForPackage(package):
    """
    Retrieve the name of an SRPM based on the python package

    :type package: str
    :param package: The package used to get the srpm name
    """

    srpm_head = getSRPMHead(getSpecPath(package))
    possible_matches = filter(
            lambda srpm: srpm.startswith(srpm_head),
            listSRPMS()
            )
    return possible_matches[0]

def buildRPM(package):
    """
    Run the rpmbuild command

    :type package: str
    :param package: The package used to get the spec file
    """

    rpmbuild("-ba", getSpecPath(package))

def uploadToWebServer(remote_server, remote_path, package, remote_port=22):
    """
    Upload the .spec file, and the srpm to a webserver 

    :type remote_server: str
    :param remote_server: The remote server to connect to

    :type remote_path: str
    :param remote_path: root path to push the files into

    :type package: str
    :param package: The package name, used to get the spec, and srpm

    :type remote_port: int
    :param remote_port: port of the remote server
    """

    spec_path = getSpecPath(package)
    srpm_name = getSRPMForPackage(package)
    srpm_path = os.path.expanduser("~/rpmbuild/SRPMS/{0}".format(srpm_name))
    remote = ssh.bake(remote_server, "-p {0}".format(remote_port))
    remote.mkdir("-p", os.path.join(remote_path, package))
    scp = scp.bake("-P {0}".format(remote_port))

    scp_lambda = lambda f: scp(f,
            "{0}:{1}".format(
                remote_server,
                os.path.join(
                    remote_path,
                    package
                )
            )
    )
    map(scp_lambda, (spec_path, srpm_path))


def main():
    """
    Main function, used to execute all the other helper funcs
    """
    package = sys.argv[1]
    editSpecFile(package)
    buildRPM(package)

if __name__ == "__main__":
    package = sys.argv[1]
    editSpecFile(package)

