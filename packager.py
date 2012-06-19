from pbs import vim, rpmbuild, pypi2spec, scp
import os
import os.path
import sys
from rpm import TransactionSet


def editSpecFile(package):
    pypi2spec(package)
    vim(os.path.expanduser("~/rpmbuild/SPECS/python-{0}.spec".format(package)), _fg=True)

def listSRPMS():
    return os.listdir(os.path.expanduser("~/rpmbuild/SRPMS"))

def getSRPMHead(spec):
    ts= TransactionSet()
    spec_obj = ts.parseSpec(spec)
    spec_headers = spec_obj.packages[0].header
    
def getSRPMForPackage(package):
    possible_matches = filter(lambda srpm: srpm.startswith(package),listSRPMS())
    return possible_matches

def buildRPM(package):
    rpmbuild("-ba",
            os.path.expanduser("~/rpmbuild/SPECS/python-{0}.spec".format(package)))
if __name__ == "__main__":
    package = sys.argv[1]
    editSpecFile(package)

