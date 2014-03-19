component-skeleton
==================

[Qubell Bazaar](https://github.com/qubell-bazaar) quickstart helper.

Quickstart
----------

0. Register in [Travis](http://travis-ci.org) and install travis tool

        gem install travis
        travis login

1. Initialize your repo with skeleton

        python skeleton.py --new --dir ./my-existing-repo

2. Setup your Qubell account, Qubell Cloud Account and S3 publishing settings for build and [GitHub token](https://github.com/settings/applications#personal-access-tokens). Note, bash-special sybmols such as braces, parentheses, backslashes, and pipe symbols should be escaped.

        travis encrypt --add env.global QUBELL_TENANT="https://express.qubell.com" QUBELL_ORGANIZATION="My Pre-Created Travis Organization"
        travis encrypt --add env.global QUBELL_USER="your+account@example.com" QUBELL_PASS="password"

        travis encrypt --add env.global PROVIDER_TYPE="aws-ec2" PROVIDER_REGION="us-east-1"
        travis encrypt --add env.global PROVIDER_IDENTITY="0123456789ABCDEFGHIJ" PROVIDER_CREDENTIAL="0123456789abcdefghijklmnopqrstuvwxyzABCD"

        travis encrypt --add env.global ARTIFACTS_S3_BUCKET="my-project-bucket" ARTIFACTS_AWS_REGION="us-east-1"
        travis encrypt --add env.global ARTIFACTS_AWS_ACCESS_KEY_ID="0123456789ABCDEFGHIJ"
        travis encrypt --add env.global ARTIFACTS_AWS_SECRET_ACCESS_KEY="0123456789abcdefghijklmnopqrstuvwxyzABCD"

        travis encrypt --add env.global GH_TOKEN="1234567890abcdefghijklmopqrstuvwxyz98765"
        travis encrypt --add env.global GIT_NAME='CI Travis' GIT_EMAIL='support@travis-ci.org'

3. By default, manifest should be named as `${REPO_NAME}.yml` and use cookbooks
from `${S3_BACKET_URL}/${REPO_NAME}-cookbooks-stable-${REVISION}.tar.gz`. To use your own custom layout,
edit `build.sh` appropriately.

4. Enable your repo on Travis [Profile](https://travis-ci.org/profile) page

5. Commit and push your changes

        git commit --all --message 'Initial travis integration'
        git push origin