from copy import deepcopy

from utils import closest_value_in_array


def make_ascii_barplot(
    value: int | float,
    max_value: int | float | None = None,
    width: int | None = None,
    block_elements: dict[int | float, str] | None = None,
    blank: str = " ",
) -> str:
    if (max_value is None) is not (width is None):
        raise ValueError(
            "If `max_value` is specified, so must `width`, and vice versa."
        )
    if max_value is not None:
        # Normalize to `width` using `max_value`:
        value = deepcopy(value / max_value * width)
    if block_elements is None:
        block_elements = {
            1 / 8: "▏",
            2 / 8: "▎",
            3 / 8: "▍",
            4 / 8: "▌",
            5 / 8: "▋",
            6 / 8: "▊",
            7 / 8: "▉",
            8 / 8: "█",
        }
    base_part = int(value // 1) * block_elements[1]
    fractional_part = block_elements[
        closest_value_in_array(value % 1, list(block_elements.keys()))
    ]
    if width is not None:
        remaining_part = (width - len(base_part) - 1) * blank
    else:
        remaining_part = ""
    return base_part + fractional_part + remaining_part


def make_ascii_barplot_with_marker(
    value: int | float,
    marker: int | float,
    max_value: int | float,
    width: int,
    block_elements: dict[int | float, str] | None = None,
    blank: str = " ",
) -> str:
    ascii_barplot = make_ascii_barplot(value, max_value, width, block_elements, blank)
    assert marker <= max_value
    # Normalize to `width` using `max_value`:
    marker = deepcopy(marker / max_value * width)
    marker_position = int(marker // 1)
    if marker_position == width:
        marker_position = width - 1
    ascii_barplot = (
        ascii_barplot[:marker_position] + "|" + ascii_barplot[marker_position + 1 :]
    )
    return ascii_barplot
