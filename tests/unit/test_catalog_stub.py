from services.catalog.stub_mismatch import flag_mismatch


def test_flag_mismatch_nike_vs_sisal_tags():
    assert flag_mismatch("Nike running shoe", ["sisal", "kiondo"]) is True


def test_flag_mismatch_clear_title():
    assert flag_mismatch("Plain ORS sachets", ["ors"]) is False
