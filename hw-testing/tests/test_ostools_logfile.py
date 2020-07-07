import os

import pytest

from ostools import LogFile


@pytest.fixture(scope='module')
def remove_temporary():
    """ Just simple cleanup """

    yield
    os.remove('aww_some.log')


def test_logfile_is_context_manager():
    assert "__enter__" in LogFile.__dict__ and "__exit__" in LogFile.__dict__


def test_logfile_create(tmp_path, remove_temporary):
    os.chdir(tmp_path)

    @LogFile('aww_some.log')
    def func_for_testing():
        import time
        time.sleep(1)
        return 0

    func_for_testing()

    assert 'aww_some.log' in os.listdir()


def test_logfile_contains_exception_info(tmp_path, remove_temporary):
    os.chdir(tmp_path)

    @LogFile('aww_some.log')
    def func_for_testing():
        return 1 / 0

    with pytest.raises(Exception) as e:
        func_for_testing()
        assert isinstance(e, ZeroDivisionError)

    with open('aww_some.log') as log_file:
        assert 'division by zero' in log_file.read()
