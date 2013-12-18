#!/usr/bin/python
# Copyright (c) 2013 Qubell Inc., http://qubell.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import shutil

from os.path import join
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 0.1")
    parser.add_option("-d", "--dir", dest="dir",
                      action="store",
                      type="string",
                      help="component folder")
    parser.add_option("-n", "--new", dest="new",
                      action="store_true",
                      default=False,
                      help="generate new skeleton for component")

    (options, args) = parser.parse_args()

    if options.new:
        new(options.dir)
    else:
        parser.print_help(sys.stderr)
        parser.exit(2, "\n%s: error: %s\n" % (parser.get_prog_name(), "please enter options"))


def new(component_dir):
    skeleton_dir = os.path.dirname(__file__)

    if not component_dir:
        component_dir = join(skeleton_dir, "../")
    else:
        component_dir = os.path.realpath(component_dir)

    test_dir = join(component_dir, "test")

    mkdir_p(test_dir)

    build_sh_path = join(component_dir, 'build.sh')

    write(build_sh_path, build_sh(test_dir))
    write(join(component_dir, ".travis.yml"), travis_template(test_dir))
    write(join(test_dir, "test_example.py"), template_test())

    copy(join(skeleton_dir, "test_runner.py"), join(test_dir, "test_runner.py"))
    copy(join(skeleton_dir, "requirements.txt"), join(test_dir, "requirements.txt"))

    chmod_x(build_sh_path)


def chmod_x(path):
    import stat

    file_stat = os.stat(path)
    os.chmod(path, file_stat.st_mode | stat.S_IEXEC)


def copy(path, target):
    if not os.path.exists(target):
        shutil.copy2(path, target)
    else:
        print '%s already exist' % path


def write(path, content):
    if not os.path.exists(path):
        with open(path, 'a') as file:
            file.write(content)
    else:
        print '%s already exist' % path


def mkdir_p(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


def travis_template(test_dir):
    return """env:
 global:
    - "QUBELL_TENANT=https://express.qubell.com"
    ## fill environment variables:
    ## QUBELL_USER, QUBELL_PASS, QUBELL_TENANT, PROVIDER_NAME, PROVIDER_TYPE, PROVIDER_IDENTITY, PROVIDER_CREDENTIAL, PROVIDER_REGION
    ## ARTIFACTS_AWS_REGION, ARTIFACTS_S3_BUCKET, ARTIFACTS_AWS_ACCESS_KEY_ID, ARTIFACTS_AWS_SECRET_ACCESS_KEY

language: python
python:
  - "2.7"

install: "pip install -r %(test_dir)s/requirements.txt"

before_script:
   - gem install travis-artifacts --no-ri --no-rdoc
   - git submodule update --init --recursive

script: ./build.sh
""" % {"test_dir": os.path.basename(test_dir)}


def build_sh(test_dir):
    return """#!/bin/bash

REPO_NAME=$(echo ${TRAVIS_REPO_SLUG} | cut -d/ -f2)
OWNER_NAME=$(echo ${TRAVIS_REPO_SLUG} | cut -d/ -f1)

function check {
    "$@"
    status=$?
    if [ $status -ne 0 ]; then
        echo "error run $@"
        exit $status
    fi
    return $status
}

function package {
    local REVISION=$1

    tar -czf ${REPO_NAME}-cookbooks-${REVISION}.tar.gz cookbooks
}

function publish {
    local REVISION=$1

    package $REVISION

    travis-artifacts upload --path ${REPO_NAME}-cookbooks-${REVISION}.tar.gz --target-path ${OWNER_NAME}/
}

function replace {
    check sed -i.bak -e 's/'${REPO_NAME}'-cookbooks-stable/'${REPO_NAME}'-cookbooks-dev/g' ${REPO_NAME}.yml
    cat ${REPO_NAME}.yml
}


publish dev
replace

pushd %(test_dir)s

check python test_runner.py

popd

publish stable
""" % {"test_dir": os.path.basename(test_dir)}


def template_test():
    return """import os

from test_runner import BaseComponentTestCase
from qubell.api.private.testing import instance, workflow, values


class ComponentTestCase(BaseComponentTestCase):
    name = "name-component"
    apps = [{
        "name": name,
        "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name))
    }]
"""


if __name__ == "__main__":
    main()
