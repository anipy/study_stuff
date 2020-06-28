import os

import pytest

import ostools
from ostools import LogFile
from ostools import TempDir


def test_logfile_is_context_manager():
    assert "__enter__" in LogFile.__dict__ and "__exit__" in LogFile.__dict__


def test_logfile_create(tmp_path):
    os.chdir(tmp_path)

    @LogFile('aww_some.log')
    def func_for_testing():
        import time
        time.sleep(1)
        return 0

    func_for_testing()

    try:
        assert 'aww_some.log' in os.listdir()
    finally:
        os.remove('aww_some.log')


def test_logfile_contains_exception_info(tmp_path):
    os.chdir(tmp_path)

    @LogFile('aww_some.log')
    def func_for_testing():
        return 1/0

    try:
        with pytest.raises(Exception) as e:
            func_for_testing()
            assert isinstance(e, ZeroDivisionError)

        with open('aww_some.log') as log_file:
            assert 'division by zero' in log_file.read()

    finally:
        os.remove('aww_some.log')


def test_tempdir_is_context_manager():
    assert "__enter__" in TempDir.__dict__ and "__exit__" in TempDir.__dict__


def test_tempdir_create(tmp_path):
    starting_path = tmp_path
    os.chdir(str(tmp_path))

    with TempDir() as tmp:
        assert isinstance(tmp, TempDir)
        assert len(list(tmp_path.iterdir())) == 1
        assert tmp.name != starting_path

    assert starting_path == tmp_path


def test_tempdir_create_if_exists(tmp_path):
    from unittest.mock import Mock

    uuid = Mock()
    gen_uuid = (
        fake_uuid
        for fake_uuid in [
            "11111111-1111-1111-1111-111111111111",
            "11111111-1111-1111-1111-111111111111",
            "ffffffff-ffff-ffff-ffff-ffffffffffff",
        ]
    )

    uuid.uuid1 = Mock(side_effect=lambda: next(gen_uuid))

    ostools.uuid = uuid

    starting_path = tmp_path
    os.chdir(str(tmp_path))
    os.mkdir("11111111-1111-1111-1111-111111111111")

    with TempDir() as tmp:
        assert uuid.uuid1.call_count == 3
        assert tmp.name.endswith("ffffffff-ffff-ffff-ffff-ffffffffffff")
        assert tmp.name != starting_path

    assert starting_path == tmp_path
    os.rmdir("11111111-1111-1111-1111-111111111111")
