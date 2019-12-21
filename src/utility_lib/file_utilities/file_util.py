"""Utilities for dealing with files.

Version: 1.2
Last_Edit: 2019-10-18T23:18:41Z
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Any


def save_string(data: str, file_path: Path) -> bool:
    """Save a string. Makes parent directories if they don't exist.
    
    Traps all errors and prints them to std out.

    Arguments:
        data {str} -- The string to save
        file_path {Path} -- Path to the saved file.
    
    Returns:
        bool -- True if successful
    """
    try:
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with open(file_path, "w") as out_file:
            out_file.write(data)
    except Exception as e:
        print(e)
        return False
    return True


def save_list_of_dicts(data: Sequence[Dict[str, Any]], file_path: Path) -> bool:
    """Save a list of dicts to csv.
    
    Arguments:
        data {Sequence[Dict[str, any]]} -- list of dicts
        file_path {Path} -- path to saved file
    
    Returns:
        bool -- True if successful.
    """
    try:
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with open(file_path, "w", encoding="utf8", newline="") as out_file:
            writer = csv.DictWriter(out_file, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(e)
        return False
    return True


def save_lines(
    string_list: Sequence[str], file_path: Path, line_separator: str = None
) -> bool:
    try:
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with open(file_path, "w") as file_out:
            if line_separator:
                file_out.writelines([x + line_separator for x in string_list])
            else:
                file_out.writelines(string_list)
    except Exception as e:
        print(e)
        return False
    return True


def delta_path(input_base_path: Path, item_path: Path, output_base_path: Path) -> Path:
    """Removes a base path from an item, and adds result to an output path.


    
    Arguments:
        input_base_path {Path} -- [description]
        item_path {Path} -- [description]
        output_base_path {Path} -- [description]
    
    Returns:
        Path -- [description]
    """
    path_stub = item_path.relative_to(input_base_path)
    output_item_path = output_base_path / path_stub
    return output_item_path


@dataclass
class PathInOut:
    path_in: Path
    path_out: Path


def delta_subdirs(
    input_base_path: Path,
    glob_pattern: str,
    output_base_path: Path,
    content_filter: Optional[Callable[[Path], bool]] = None,
) -> List[PathInOut]:
    """Get a list of files from a source directory, return a list of paths to a new location for files and sub dirs.
    
    Arguments:
        input_base_path {Path} -- [description]
        glob_pattern {str} -- [description]
        output_base_path {Path} -- [description]
    
    Keyword Arguments:
        content_filter {Optional[Callable[[Path], bool]]} -- [description] (default: {None})
    
    Raises:
        ValueError: [description]
    
    Returns:
        List[PathInOut] -- [description]
    """

    paths_in = collect_paths(
        input_base_path=input_base_path,
        glob_pattern=glob_pattern,
        content_filter=content_filter,
    )
    item_list: List[PathInOut] = []
    for path_in in paths_in:
        path_out = delta_path(input_base_path, path_in, output_base_path)
        item_list.append(PathInOut(path_in, path_out))
    return item_list


def collect_paths(
    input_base_path: Path,
    glob_pattern: str,
    content_filter: Optional[Callable[[Path], bool]] = None,
) -> List[Path]:
    def pass_through(path_in: Path):
        return True

    if content_filter is None:
        content_filter = pass_through
    if not input_base_path.is_dir():
        raise ValueError(f"{input_base_path} - Not a directory or does not exist.")
    paths_in = input_base_path.glob(glob_pattern)
    item_list: List[Path] = []
    for path_in in paths_in:
        if content_filter(path_in):
            item_list.append(path_in)
    return item_list


def save_stringable(
    stringable_sequence: Sequence[Any], file_path: Path, line_separator: str = None
) -> bool:
    with open(file_path, "w") as file_out:
        if line_separator:
            file_out.writelines([str(x) + line_separator for x in stringable_sequence])
        else:
            file_out.writelines([str(x) for x in stringable_sequence])
    return True


def load_lines(file_path: Path) -> List[str]:
    with open(file_path, "r") as file_in:
        lines = [line.strip() for line in file_in]
    return lines


def load_string(file_path: Path) -> str:
    with open(file_path, "r") as file_in:
        loaded_string = file_in.read()
    return loaded_string
