from ascii_barplot import make_ascii_barplot


def test_make_ascii_barplot():
    assert make_ascii_barplot(4) == "████▏"
    assert make_ascii_barplot(4.2) == "████▎"
    assert make_ascii_barplot(4.2, max_value=5, width=10) == "████████▍ "
    assert make_ascii_barplot(4.2, max_value=10, width=5) == "██▏  "
