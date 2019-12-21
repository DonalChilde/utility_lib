from pathlib import Path

import pytest

from utility_lib.file_utilities import file_util


def test_delta_path_subdir():
    input_path_base = Path("/home/croaker/projects")
    item_path = Path("/home/croaker/projects/foo/bar.txt")
    output_path_base = Path("/home/croaker/tmp")
    delta_path = file_util.delta_path(input_path_base, item_path, output_path_base)
    assert delta_path == Path("/home/croaker/tmp/foo/bar.txt")


def test_delta_path_no_common():
    input_path_base = Path("/home/croaker/projects")
    item_path = Path("/home2/croaker/projects/foo/bar.txt")
    output_path_base = Path("/home/croaker/tmp")
    with pytest.raises(ValueError):
        delta_path = file_util.delta_path(input_path_base, item_path, output_path_base)
    # assert delta_path == Path("/home/croaker/tmp/foo/bar.txt")


def test_delta_path_no_subdir():
    input_path_base = Path("/home/croaker/projects")
    item_path = Path("/home/croaker/projects/bar.txt")
    output_path_base = Path("/home/croaker/tmp")
    delta_path = file_util.delta_path(input_path_base, item_path, output_path_base)
    assert delta_path == Path("/home/croaker/tmp/bar.txt")


def test_delta_subdirs():
    input_base_path = Path("/home/chad/projects/AAL-PBS-Data/")
    glob_pattern = "**/*.txt"
    output_base_path = Path("/home/chad/tmp")

    def path_filter(path: Path) -> bool:
        if "MIA" in path.name:
            return True
        else:
            return False

    item_list = file_util.delta_subdirs(
        input_base_path=input_base_path,
        glob_pattern=glob_pattern,
        output_base_path=output_base_path,
        content_filter=path_filter,
    )
    print(item_list)


def test_collect_paths():
    input_base_path = Path("/home/chad/projects/AAL-PBS-Data/")
    glob_pattern = "**/*.txt"

    def path_filter(path: Path) -> bool:
        if "MIA" in path.name:
            return True
        else:
            return False

    item_list = file_util.collect_paths(
        input_base_path=input_base_path,
        glob_pattern=glob_pattern,
        content_filter=path_filter,
    )
    print(item_list)
    assert len(item_list) > 0
