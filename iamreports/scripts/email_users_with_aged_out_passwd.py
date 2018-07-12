#!/usr/bin/env python

"""
email all users for whom IAM passwd is due for reset

Usage:
  email_users_with_aged_out_passwd  [report]
                                [--config FILE]
                                [--spec-dir PATH] 
                                [--master-account-id ID]
                                [--auth-account-id ID]
                                [--org-access-role ROLE]
                                [--exec] [-q] [-d|-dd]

Options:
  -h, --help                Show this help message and exit.
  -V, --version             Display version info and exit.
  --config FILE             AWS Org config file in yaml format.
  --spec-dir PATH           Location of AWS Org specification file directory.
  --master-account-id ID    AWS account Id of the Org master account.
  --auth-account-id ID      AWS account Id of the authentication account.
  --org-access-role ROLE    IAM role for traversing accounts in the Org.
  --exec                    Execute proposed changes to AWS Org.
  -q, --quiet               Repress log output.
  -d, --debug               Increase log level to 'DEBUG'.
  -dd                       Include botocore and boto3 logs in log stream.

"""

import smtplib
from email.message import EmailMessage

from docopt import docopt

import awsorgs
import awsorgs.utils
from awsorgs.utils import *
from awsorgs.spec import *

from iamreports.credentials import CredentialReporter
from iamreports.utils import yamlfmt

message = """Hello Dear User,

This is a courtesy email to let you know...

We are implementing a password expiration policy in our AWS
central authetication account.  Since your current AWS password
is over 180 day old, you will be requisted to reset it the next
time you log in to https://seg-auth.signin.aws.amazon.com/console.

Thanks, and have a lot of fun!

"""

def send_email(email):
    print(email)
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'password policy for ucop AWS seg-auth account'
    msg['From'] = 'agould@ucop.edu'
    msg['To'] = email
    msg['Cc'] = 'agould@ucop.edu'
    s = smtplib.SMTP('smtp.ucop.edu')
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':

    args = docopt(__doc__, version=awsorgs.__version__)
    log = get_logger(args)
    args = load_config(log, args)
    log.debug(args)
    spec = validate_spec(log, args)
    log.debug(yamlfmt(spec['users']))

    credential_report = CredentialReporter()
    credential_report.load()
    users = credential_report.list_users_with_aged_out_passwords(180)
    log.debug(yamlfmt(users))
    for user in users:
        email = lookup(spec['users'], 'Name', user, 'Email')
        send_email(email)


##### Notes #####

## sent on July 11, 2018

# (python3.6) agould@horus:~/git-repos/github/ashleygould/aws-orgs/awsorgs/cli> ./email_users_with_aged_out_passwd.py
# Abhisekh.Banerjee@ucop.edu
# agould@ucop.edu
# Amanpreet.Kaur@ucop.edu
# Cynthia.foos@ucop.edu
# Chris.Miller@ucop.edu
# daniel.adeniji@ucop.edu
# dbrunet@dlzpgroup.com
# deborah.samarov@ucop.edu
# None
# Dean.Petterson@ucop.edu
# eodell@ucop.edu
# justin.tipton@ucop.edu
# ken.lumnaokrut@ucop.edu
# Kiran.Sirimalla@ucop.edu
# Louis.Zeoli@ucop.edu
# mark.boyce@ucop.edu
# mark.cruz@ucop.edu
# Mukund.Gidadhubli@ucop.edu
# mahtaj.khamneian@ucop.edu
# Madhavi.Kondamadugula@ucop.edu
# mnakane@ucop.edu
# mkakkera@ucop.edu
# nick.sefiddashti@dlzpgroup.com
# patrick.rogers@ucop.edu
# rohit.doddavarapu@ucop.edu
# rick.kehret@ucop.edu
# rohit.kumar@ucop.edu
# robert.mijango@ucop.edu
# Rajesh.Sharma@ucop.edu
# richard.silva@dlzpgroup.com
# steven.hunter@ucop.edu
# Sundar.Potti@ucop.edu
# sushant.prasad@ucop.edu
# thanson@ucop.edu
# William.Hoke@ucop.edu

