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


# def test_cli_multirec_deploy(tmpdir, run):
#     result = run("run", "--path", tmpdir)
#     assert result.ret == 0


# def test_cli_multirec_deploy_start(tmpdir, run):
#     result = run("deploy", "--path", tmpdir)
#     result = run("start")
#     assert result.ret == 0


def test_cli_multirec(tmpdir, run):
    result = run()
    assert result.ret == 0
