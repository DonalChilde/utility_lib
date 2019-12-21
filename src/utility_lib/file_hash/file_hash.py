"""[summary]

https://stackoverflow.com/a/3431835/105844

Returns:
    [type] -- [description]

Yields:
    [type] -- [description]
"""
import hashlib
from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    ByteString,
    Callable,
    Dict,
    Generator,
    Iterator,
    NamedTuple,
    Optional,
    Sequence,
)

VERSION = "0.1.0"


def hash_a_byte_str_iterator(
    bytes_iterator: Iterator[ByteString], hasher: Any, as_hex_str: bool = False
):
    # https://stackoverflow.com/a/3431835/105844
    for block in bytes_iterator:
        hasher.update(block)
    return hasher.hexdigest() if as_hex_str else hasher.digest()


def file_as_block_iterator(
    file_handle: BinaryIO, block_size: int = 65536
) -> Iterator[ByteString]:
    # https://stackoverflow.com/a/3431835/105844
    with file_handle:
        block = file_handle.read(block_size)
        while len(block) > 0:
            yield block
            block = file_handle.read(block_size)


def calculate_file_hash(
    file_path: Path, hasher: Any, block_size: int = 65536, as_hex_str: bool = True
):
    """[summary]
    
    https://stackoverflow.com/a/21565932/105844

    Arguments:
        file_path {Path} -- [description]
        hasher {Any} -- [description]
    
    Keyword Arguments:
        block_size {int} -- [description] (default: {65536})
        as_hex_str {bool} -- [description] (default: {True})
    
    Raises:
        ValueError: [description]
    
    Returns:
        [type] -- [description]
    """
    if not file_path.exists() or not file_path.is_file():
        raise ValueError(f"{file_path} is not a file or does not exist")

    # with open(file_path, "rb") as file_in:
    #     for block in iter(lambda: file_in.read(block_size), b""):
    #         hasher.update(block)
    # if as_hex_str:
    #     return hasher.hexdigest()
    # return hasher.digest()

    with open(file_path, "rb") as file_in:
        result = hash_a_byte_str_iterator(
            bytes_iterator=file_as_block_iterator(
                file_handle=file_in, block_size=block_size
            ),
            hasher=hasher,
            as_hex_str=as_hex_str,
        )
        return result
    return None


HASH_METHODS: Dict[str, Callable] = {
    "blake2b": hashlib.blake2b,
    "blake2s": hashlib.blake2s,
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    # "shake_128": hashlib.shake_128,
    # "shake_256": hashlib.shake_256,
    "sha3_224": hashlib.sha3_224,
    "sha3_256": hashlib.sha3_256,
    "sha3_384": hashlib.sha3_384,
    "sha3_512": hashlib.sha3_512,
}


def get_hasher(hasher_name: str):
    lc_hasher_name = hasher_name.lower()
    hasher: Optional[Callable] = HASH_METHODS.get(lc_hasher_name, None)
    if hasher is None:
        raise ValueError(
            f"Hasher {hasher_name} not found. Must be one of {HASH_METHODS.keys()}"
        )
    return hasher()


class FileHash(NamedTuple):
    file_path: Path
    file_hash: str
    hash_method: str

    def __repr__(self):
        return f"<FileHash(file_path={self.file_path}, file_hash={self.file_hash}, hash_method={self.hash_method})>"


def get_file_hash(file_path: Path, hash_method: str) -> FileHash:
    hasher = get_hasher(hash_method)

    file_hash_str = calculate_file_hash(file_path, hasher)
    return FileHash(file_path, file_hash_str, hash_method)


def get_file_hash_generator(
    file_paths: Sequence[Path], hash_method: str
) -> Generator[FileHash, None, None]:
    generator = (
        get_file_hash(file_path, hash_method)
        for file_path in file_paths
        if file_path.is_file()
    )
    return generator
