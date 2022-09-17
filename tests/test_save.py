import os
import shutil
from unittest import mock
from pshouse_schedule.storage import Storage, save_to_storage

STORAGE_ROOT_DIR_PATH = "./tests/data/storage_root"
STORAGE_BUCKET_DIRNAME = "storage_bucket_dir"


@mock.patch("pshouse_schedule.config.STORAGE_TYPE", "LOCAL")
@mock.patch("pshouse_schedule.config.STORAGE_KEY", STORAGE_ROOT_DIR_PATH)
@mock.patch("pshouse_schedule.config.STORAGE_SECRET", "storage_secret")
def mock_storage_cls(dirname):
    return Storage(STORAGE_BUCKET_DIRNAME)


@mock.patch("pshouse_schedule.storage.Storage", mock_storage_cls)
def test_save_to_storage():
    _set_up()

    fake_dirname = "dirname_for_test"
    tmp_file_path = "./tests/data/a.txt"
    tmp_file_content = "No"
    expected_file_path = f"{STORAGE_ROOT_DIR_PATH}/{STORAGE_BUCKET_DIRNAME}/a.txt"

    save_to_storage(fake_dirname, tmp_file_path, tmp_file_content)

    assert os.path.exists(expected_file_path)

    with open(expected_file_path, "r", encoding="utf-8-sig") as f:
        saved_text = f.read()

    assert saved_text == tmp_file_content

    _tear_down(tmp_file_path)


def _set_up():
    try:
        shutil.rmtree(STORAGE_ROOT_DIR_PATH)
    except FileNotFoundError:
        pass


def _tear_down(tmp_file_path):
    shutil.rmtree(STORAGE_ROOT_DIR_PATH)
    os.remove(tmp_file_path)
