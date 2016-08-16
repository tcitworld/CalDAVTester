#!/usr/bin/env python
#
##
# Copyright (c) 2006-2015 Apple Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
#
# Runs the CalDAVTester test suite ensuring that required packages are available.
#

import getopt
import os
import subprocess
import sys

cwd = os.getcwd()
top = cwd[:cwd.rfind("/")]
add_paths = []
git = "/usr/bin/git"
uri_base = "https://github.com/apple"

packages = [
    ("pycalendar", "ccs-pycalendar", uri_base + "/ccs-pycalendar", "ccs-pycalendar/src"),
]

def usage():
    print ("""Usage: run.py [options]
Options:
    -h       Print this help and exit
    -s       Do setup only - do not run any tests
    -r       Run tests only - do not do setup
    -p       Print PYTHONPATH
""")



def setup():
    for package in packages:
        ppath = "%s/%s" % (top, package[1],)
        if not os.path.exists(ppath):
            print("%s package is not present." % (package[0],))
            os.system("%s clone %s %s" % (git, package[2], ppath))
        else:
            print ("%s package is present." % (package[0],))
            os.system("%s fetch origin" % (git))
            reslog=os.popen("%s log HEAD..origin/master --oneline" % (git)).read()
            if reslog != "":
              os.system("%s merge origin/master" % (git))

        add_paths.append("%s/%s" % (top, package[3],))



def pythonpath():
    for package in packages:
        add_paths.append("%s/%s" % (top, package[1],))
    pypaths = sys.path
    pypaths.extend(add_paths)
    return ":".join(pypaths)



def runit():
    pythonpath = ":".join(add_paths)
    return subprocess.Popen(["./testcaldav.py", "--all"], env={"PYTHONPATH": pythonpath}).wait()



if __name__ == "__main__":

    try:
        do_setup = True
        do_run = True

        options, args = getopt.getopt(sys.argv[1:], "hprs")

        for option, value in options:
            if option == "-h":
                usage()
                sys.exit(0)
            elif option == "-p":
                print(pythonpath())
                sys.exit(0)
            elif option == "-r":
                do_setup = False
            elif option == "-s":
                do_run = False
            else:
                print("Unrecognized option: %s" % (option,))
                usage()
                raise ValueError

        # Process arguments
        if len(args) != 0:
            print("No arguments allowed.")
            usage()
            raise ValueError

        if (do_setup):
            setup()
        else:
            pythonpath()
        if (do_run):
            sys.exit(runit())
        else:
            sys.exit(0)
    except SystemExit as e:
        pass
    except Exception as e:
        sys.exit(str(e))
