import os
import datetime
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
def test_initialize_credential_reporter():
    credential_report = CredentialReporter()
    assert isinstance(credential_report, CredentialReporter)

@mock_iam
def test_load_empty_report():
    """
    The moto generate_credential_report model returns a report
    dict with no 'Content' key
    """
    credential_report = CredentialReporter()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        credential_report.load()
    assert pytest_wrapped_e.type == SystemExit
    assert isinstance(credential_report.raw_report, dict)
    assert isinstance(credential_report.timestamp, datetime.datetime)
    #assert hasattr(credential_report,'decoded_csv_report_object') == False
    assert not hasattr(credential_report,'decoded_csv_report_object')
    #print(yamlfmt(credential_report.raw_report))
    #print(credential_report.timestamp)
 
@mock_iam
def test_load_report_from_file():
    credential_report_fixture = get_fixture_file('credential_report.json')
    assert os.path.exists(credential_report_fixture)
    credential_report = CredentialReporter()
    credential_report.load(source_file=credential_report_fixture)
    #print(yamlfmt(credential_report.raw_report))
    assert isinstance(credential_report.raw_report, dict)
    #assert isinstance(credential_report.timestamp, datetime.datetime)
    #assert credential_report.decoded_csv_report_object == None
    ##print(yamlfmt(credential_report.raw_report))
    ##print(credential_report.timestamp)
    ##assert False   #assert False
