"""Utilities for dealing with files.

Version: 1.2
Last_Edit: 2019-10-18T23:18:41Z
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Any,
    Generator,
    Iterable,
)


def save_string(data: str, file_path: Path, parents=False, exist_ok=True) -> bool:
    """
    Save a string. Makes parent directories if they don't exist.

    Does not trap any exceptions.

    Parameters
    ----------
    data : str
        The string to save.
    file_path : Path
        Path to saved file. Existing files will be overwritten.
    parents : bool, optional
        Make parent directories if they don't exist. As used by `Path.mkdir`, by default False
    exist_ok : bool, optional
        Suppress exception if parent directory exists as directory. As used by `Path.mkdir`, by default True

    Returns
    -------
    bool
        True if successful.

    Raises
    ------
    Exception
        Any exception that can be raised from Path.mkdir or Path.open
    """

    if parents:
        file_path.parent.mkdir(parents=parents, exist_ok=exist_ok)
    with file_path.open("w") as file_out:
        file_out.write(data)
    return True


def save_lines(
    data: Sequence[str],
    file_path: Path,
    line_separator: str = "\n",
    parents=False,
    exist_ok=True,
) -> bool:
    """
    Write a sequence of strings as lines to a file.

    

    Parameters
    ----------
    data : Sequence[str]
        Data to save.
    file_path : Path
        Path to saved file. Existing files will be overwritten.
    line_separator : str, optional
        Separate lines with this., by default "\n"
    parents : bool, optional
        Make parent directories if they don't exist. As used by `Path.mkdir`, by default False
    exist_ok : bool, optional
        Suppress exception if parent directory exists as directory. As used by `Path.mkdir`, by default True

    Returns
    -------
    bool
        True if successful.

    Raises
    ------
    Exception
        Any exception that can be raised from Path.mkdir or Path.open
    """
    if parents:
        file_path.parent.mkdir(parents=parents, exist_ok=exist_ok)
    with file_path.open("w") as file_out:
        if line_separator:
            file_out.writelines((x + line_separator for x in data))
        else:
            file_out.writelines(data)
    return True


def delta_path(input_base_path: Path, item_path: Path, output_base_path: Path) -> Path:
    """
    Removes a base path from an item, and appends result to an output path.

    Parameters
    ----------
    input_base_path : Path
        The sub Path to be removed from item_path.
    item_path : Path
        The Path to be deltad
    output_base_path : Path
        The new base Path for item_path.

    Returns
    -------
    Path
        The new combined path.

    Raises
    ------
    ValueError
        If input_base_path is not a sub Path of item_path.
    """
    path_stub = item_path.relative_to(input_base_path)
    output_item_path = output_base_path / path_stub
    return output_item_path


@dataclass
class PathInOut:
    path_in: Path
    path_out: Path


def delta_paths(
    input_base_path: Path,
    glob_pattern: str,
    output_base_path: Path,
    path_filter: Optional[Callable[[Path], bool]] = None,
) -> Generator[Path, None, None]:
    """
    Get a list of files relative to input_base_path, return a list of paths
    to the new location for files and sub dirs.

    Paths have input_base_path removed, and the resulting path fragment is
    appended to output_base_path.

    Parameters
    ----------
    input_base_path : Path
        A starting Path
    glob_pattern : str
        Glob pattern to match. e.g "*" or "**/*"
    output_base_path : Path
        [description]
    path_filter : Optional[Callable[[Path], bool]], optional
        [description], by default None

    Yields
    -------
    Generator[Path, None, None]
        The new Paths.

    Raises
    ------
    ValueError
        input_base_path must exist and be a directory.
    """

    if not input_base_path.is_dir():
        raise ValueError(f"{input_base_path} - Not a directory or does not exist.")
    paths_in = collect_paths(
        input_base_path=input_base_path,
        glob_pattern=glob_pattern,
        path_filter=path_filter,
    )
    for path_in in paths_in:
        path_out = delta_path(input_base_path, path_in, output_base_path)
        yield path_out


def collect_paths(
    input_base_path: Path,
    glob_pattern: str,
    path_filter: Optional[Callable[[Path], bool]] = None,
) -> Generator[Path, None, None]:
    """
    Collect paths, and apply a filter

    Parameters
    ----------
    input_base_path : Path
        A starting Path
    glob_pattern : str
        Glob pattern to match. e.g "*" or "**/*"
    path_filter : Optional[Callable[[Path], bool]], optional
        A custom filter for more complex matching than can be provided by glob, by default None

    Yields
    -------
    Generator[Path, None, None]
        The matched Paths.

    Raises
    ------
    ValueError
        input_base_path must exist and be a directory.
    """

    # default content filter.
    def pass_through(_path_in: Path):
        return True

    if path_filter is None:
        path_filter = pass_through
    if not input_base_path.is_dir():
        raise ValueError(f"{input_base_path} - Not a directory or does not exist.")
    paths_in = input_base_path.glob(glob_pattern)
    for path_in in paths_in:
        if path_filter(path_in):
            yield path_in


def save_stringables(
    iterable_stringable: Iterable[Any],
    file_path: Path,
    line_separator: str = "\n",
    parents=False,
    exist_ok=True,
) -> bool:
    if parents:
        file_path.parent.mkdir(parents=parents, exist_ok=exist_ok)
    with open(file_path, "w") as file_out:
        if line_separator:
            file_out.writelines((str(x) + line_separator for x in iterable_stringable))
        else:
            file_out.writelines((str(x) for x in iterable_stringable))
    return True

