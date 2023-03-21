import os

import pandas as pd
import pytest


# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin.
pytest_plugins = ["pytester"]


@pytest.fixture
def run(testdir):
    def do_run(*args):
        args = ["multirec"] + list(args)
        return testdir.run(*args)

    return do_run


def test_cli_multirec(tmpdir, run):
    result = run()
    assert result.ret == 0


def test_cli_multirec_run_default(tmpdir, run):
    path_to_csv = os.path.join(tmpdir, "test.csv")
    test_df = pd.DataFrame(
        data={
            "Tags": [
                "Tag1, Tag2",
                "Tag1, Tag3",
                "Tag1, Tag2, Tag3",
            ]
        }
    )
    test_df.to_csv(
        path_to_csv
    )
    out_path = os.path.join(tmpdir, "out.csv")

    result = run("run", "--size", "2", path_to_csv, out_path)
    assert result.ret == 0

    out_df = pd.read_csv(out_path)
    assert out_df["recommendations"].iloc[0] == '[2, 1]'
    assert out_df["recommendations"].iloc[1] == '[2, 0]'
    assert out_df["recommendations"].iloc[2] == '[1, 0]'
