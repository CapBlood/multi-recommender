import subprocess


def run_web(csv_path, mapping):
    subprocess.run([
        "streamlit", "run", "src/multirec/web/app.py",
        csv_path, mapping])


if __name__ == '__main__':
    run_web()
