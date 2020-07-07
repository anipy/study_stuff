import os

import ostools
from ostools import TempDir


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
