import os
import datetime
import tempfile
import pytest
from pkg_resources import resource_filename

import boto3
import moto
from moto import mock_iam

from iamreports.credentials import CredentialReporter
from iamreports.utils import yamlfmt


def get_fixture_file(fixture_file):
    """Returns  path to named fixture file."""
    fixtures_dir = resource_filename(__name__, 'fixtures')
    fixture_file = os.path.join(fixtures_dir, fixture_file)
    return fixture_file


@mock_iam
def test_load_empty_report():
    """
    The moto generate_credential_report model returns a report
    dict with no 'Content' key
    """
    credential_report = CredentialReporter()
    assert isinstance(credential_report, CredentialReporter)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        credential_report.load()
    assert pytest_wrapped_e.type == SystemExit
    assert isinstance(credential_report.raw_report, dict)
    assert isinstance(credential_report.timestamp, datetime.datetime)
    assert not hasattr(credential_report,'decoded_csv_report_object')
    #print(yamlfmt(credential_report.raw_report))
    #print(credential_report.timestamp)
 
@mock_iam
def test_load_report_from_file():
    credential_report_fixture = get_fixture_file('credential_report.pkl')
    assert os.path.exists(credential_report_fixture)
    credential_report = CredentialReporter()
    credential_report.load(source_file=credential_report_fixture)
    assert isinstance(credential_report.raw_report, dict)
    assert isinstance(credential_report.user_data, list)
    #print(yamlfmt(credential_report.user_data))
    #assert False   #assert False
 
@mock_iam
def test_save_report_to_file():
    credential_report_fixture = get_fixture_file('credential_report.pkl')
    credential_report = CredentialReporter()
    credential_report.load(source_file=credential_report_fixture)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        save_report_file = tmp.name
        credential_report.save_to_file(save_report_file)
    assert os.path.exists(save_report_file)
    credential_report2 = CredentialReporter()
    credential_report2.load(source_file=save_report_file)
    assert isinstance(credential_report2.raw_report, dict)
    assert isinstance(credential_report2.user_data, list)
    os.unlink(save_report_file)
    assert not os.path.exists(save_report_file)
    #print(yamlfmt(credential_report.user_data))
    #assert False   #assert False
 
@mock_iam
def test_aged_out_users():
    credential_report_fixture = get_fixture_file('credential_report.pkl')
    assert os.path.exists(credential_report_fixture)
    credential_report = CredentialReporter()
    credential_report.load(source_file=credential_report_fixture)
    assert isinstance(credential_report.raw_report, dict)
    assert isinstance(credential_report.user_data, list)
    users = credential_report.list_users_with_aged_out_passwords(60)
    assert users == ['atayag', 'cbrothers', 'shunter']
    #print(users)
    #assert False

