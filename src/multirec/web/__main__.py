import subprocess


def run_web():
    subprocess.run(["streamlit", "run", "src/multirec/web/app.py"])


if __name__ == '__main__':
    run_web()
