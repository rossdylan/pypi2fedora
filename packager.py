from pbs import vim, rpmbuild, pypi2spec, scp, ssh
import os
import os.path
import sys
from rpm import TransactionSet


def getSpecPath(package):
    return os.path.expanduser("~/rpmbuild/SPECS/{0}.spec".format(package))

def editSpecFile(package):
    pypi2spec(package)
    vim(getSpecPath(package), _fg=True)

def listSRPMS():
    return os.listdir(os.path.expanduser("~/rpmbuild/SRPMS"))

def getSRPMHead(spec):
    ts = TransactionSet()
    spec_obj = ts.parseSpec(spec)
    spec_headers = spec_obj.packages[0].header
    head = "{0}-{1}".format(
            spec_headers.format("%{name}"),
            spec_headers.format("%{version}")
            )
    return head

def getSRPMForPackage(package):
    srpm_head = getSRPMHead(getSpecPath(package))
    possible_matches = filter(
            lambda srpm: srpm.startswith(srpm_head),
            listSRPMS()
            )
    return possible_matches[0]

def buildRPM(package):
    rpmbuild("-ba", getSpecPath(package))

def uploadToWebServer(remote_server, remote_path, package, remote_port=22):
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
    package = sys.argv[1]
    editSpecFile(package)
    buildRPM(package)

if __name__ == "__main__":
    package = sys.argv[1]
    editSpecFile(package)

