from __future__ import annotations
from pathlib import Path
from typing import Union

from eb_macro_gen.objects import EasyBuilderTag, EasyBuilderTagList
from eb_macro_gen.plcs.koyo import KoyoTagList, KOYO_EB_TYPE_MAP


PathLike = Union[str, Path]


def load_eb_tags(path: PathLike) -> EasyBuilderTagList:
    """Load an EasyBuilder-exported tag CSV into an :class:`EasyBuilderTagList`.

    Parameters
    ----------
    path:
        Path to the CSV file as exported by EasyBuilder Pro.

    Returns
    -------
    EasyBuilderTagList
    """
    tags = EasyBuilderTagList()
    with Path(path).open("r") as fh:
        tags.read(fh)
    return tags


def save_eb_tags(tags: EasyBuilderTagList, path: PathLike) -> None:
    """Write an :class:`EasyBuilderTagList` to a CSV file importable by EasyBuilder Pro.

    Parameters
    ----------
    tags:
        The tag list to write.
    path:
        Destination file path.  The file is created or overwritten.
    """
    with Path(path).open("w") as fh:
        tags.write(fh)


def load_koyo_tags(path: PathLike, device_name: str) -> EasyBuilderTagList:
    """Load a Koyo PLC nicknames CSV and convert it to an :class:`EasyBuilderTagList`.

    Parameters
    ----------
    path:
        Path to the Koyo-exported nicknames CSV.
    device_name:
        The PLC device name exactly as configured in EasyBuilder Pro's
        device settings (e.g. ``"MyKoyoPLC"``).

    Returns
    -------
    EasyBuilderTagList with each Koyo tag converted to an EasyBuilder tag.
    """
    koyo_tags = KoyoTagList()
    with Path(path).open("r") as fh:
        koyo_tags.read(fh)

    eb_tags = EasyBuilderTagList()
    for _, __, tag in iter(koyo_tags.map):
        register = "".join(filter(str.isalpha, tag.Address))
        address = "".join(filter(str.isnumeric, tag.Address))
        eb_tag = EasyBuilderTag(
            tag.Nickname,
            device_name,
            f"{register},{address}",
            tag.AddressComment,
            KOYO_EB_TYPE_MAP[tag.Data],
        )
        eb_tags.add(eb_tag)

    return eb_tags