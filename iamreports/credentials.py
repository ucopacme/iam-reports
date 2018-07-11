#/usr/bin/env python

import os
import sys
import io
import csv
import json
import time
from datetime import datetime, timedelta
import pickle

import boto3
import yaml

from iamreports.utils import yamlfmt


def get_datetime_object_from_date_string(date_string):
    # strip off tz suffix:
    # '2017-11-17T00:50:20+00:00' => '2017-11-17T00:50:20'
    date_string = date_string.partition('+')[0]
    datetime_pattern = "%Y-%m-%dT%H:%M:%S"
    return datetime.strptime(date_string, datetime_pattern)


class CredentialReporter(object):

    def __init__(self,
        timeout=30,
        retries=0,
    ):
        self.timeout=timeout
        self.retries=retries


    def load(self, source_file=None, s3_bucket=None):
        if source_file:
            self.raw_report = self._read_raw_credentials_report_from_file(source_file)
        else:
            self.raw_report = self._get_raw_credential_report_from_aws()
        self.timestamp = self.raw_report['GeneratedTime']
        self.user_data = self._extract_content()


    def save_to_file(self, output_file=None):
        try:
            with open(output_file, 'wb') as fd:
                pickle.dump(self.raw_report, fd)
        except Exception as e:
            sys.exit('could not write report file {}: {}'.format(output_file, e))
        

    def save_to_s3(self, s3_bucket, s3_key):
        pass


    def _read_raw_credentials_report_from_file(self, source_file):
        try:
            with open(source_file, 'rb') as fd:
                return pickle.load(fd)
        except Exception as e:
            sys.exit('could not open report file {}: {}'.format(source_file, e))


    def _get_raw_credential_report_from_aws(self):
        client = boto3.client('iam')
        try:
            return client.get_credential_report()
        except client.exceptions.CredentialReportNotPresentException as e:
            client.generate_credential_report()
            report_ready = False
            count = 0
            interval = 5
            maxcount = self.timeout // interval
            while count < maxcount and not report_ready:
                time.sleep(interval)
                try:
                    return client.get_credential_report()
                except client.exceptions.CredentialReportNotPresentException as e:
                    count += 1
            if not report_ready:
                sys.exit('could not :generate credentials report {}'.format(e))


    def _extract_content(self):
        # raw report 'Content' is a base64 encoded csv blob
        try:
            content = io.StringIO(self.raw_report['Content'].decode())
        except KeyError as e:
            sys.exit('credentials report has no content: {}'.format(e))
        reader = csv.DictReader(content)
        user_data = []
        for row in reader:
            user = dict()
            for key in reader.fieldnames:
                user[key] = row[key]
            user_data.append(user)
        return user_data

    def list_aged_out_users(self, date_field, age_in_days):
        aged_out_users = []
        now = datetime.utcnow()
        user_date_map = {x['user']: x[date_field] for x in self.user_data}
        for user, date_string in user_date_map.items():
            try:
                then = get_datetime_object_from_date_string(date_string)
                if now - then > timedelta(days=age_in_days):
                    aged_out_users.append(user)
            except ValueError:
                pass
        return aged_out_users

    def list_users_with_aged_out_passwords(self, age_in_days):
        return self.list_aged_out_users('password_last_changed', age_in_days)



if __name__ == '__main__':
    credential_report = CredentialReporter()
    credential_report.load()
    #print(yamlfmt(credential_report.raw_report))
    #print(type(credential_report.raw_report['Content']))
    #print(yamlfmt(credential_report.user_data))
    credential_report.save_to_file('/tmp/credential_report.pkl')




#def list_aged_out_users(credentials_report, date_field, age_in_days):
#    aged_out_users = []
#    now = datetime.utcnow()
#    user_date_map = {x['user']: x[date_field] for x in credentials_report}
#    for user, date_string in user_date_map.items():
#        try:
#            then = get_datetime_object_from_date_string(date_string)
#            if now - then > timedelta(days=age_in_days):
#                aged_out_users.append(user)
#        except ValueError:
#            pass
#    return aged_out_users
#
#def list_users_in_group(group_name):
#    group = boto3.resource('iam').Group(group_name)
#    return [user.name for user in group.users.all()]
#
#def get_report_for_user(credentials_report, user_name):
#    return [x for x in credentials_report if x['user'] == user_name][0]
#
#def get_report_for_users(credentials_report, user_list):
#    report = []
#    for user_name in user_list:
#        report.append(get_report_for_user(credentials_report, user_name))
#    return report
#
#def list_users_with_aged_out_passwords(credentials_report, age_in_days):
#    return list_aged_out_users(credentials_report, 'password_last_changed', age_in_days)
#
#def list_users_with_aged_out_last_login(credentials_report, age_in_days):
#    return list_aged_out_users(credentials_report, 'password_last_used', age_in_days)
#
#def list_users_who_never_changed_their_password(credentials_report):
#    return [x['user'] for x in credentials_report if x['password_last_changed'] == 'N/A']
#
#def list_users_with_no_mfa_device(credentials_report):
#    return [x['user'] for x in credentials_report if x['mfa_active'] == 'false']
#
#def get_report_for_users_in_group(credentials_report, group_name):
#    return get_report_for_users(credentials_report, list_users_in_group(group_name))
#
#if __name__ == '__main__':
#
#    csv_report_file_object = get_iam_credential_report()
#    credentials_report = read_iam_credential_report(csv_report_file_object)
#    #print(yamlfmt(credentials_report))
#    #response = list_users_with_aged_out_passwords(credentials_report, 180)
#    #print(response)
#    #response = list_users_with_aged_out_last_login(credentials_report, 60)
#    #print(response)
#    #response = list_users_who_never_changed_their_password(credentials_report)
#    #print(yamlfmt(response))
#    #response = list_users_with_no_mfa_device(credentials_report)
#    #print(yamlfmt(response))
#    #response = get_report_for_user(credentials_report, 'ashely')
#    #print(yamlfmt(response))
#    #print(response)
#    response = list_users_in_group('admins')
#    print(response)
#    #response = get_report_for_users_in_group(credentials_report, 'admins')
#    #print(yamlfmt(response))
    
