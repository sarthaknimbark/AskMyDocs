from subprocess import Popen
import os
from pathlib import Path
import sys

def start_streamlit():
    streamlit_command = "python -m streamlit run app.py"  # Replace 'app.py' with your Streamlit app filename
    process = Popen(streamlit_command.split())
    process.communicate()

if __name__ == '__main__':
    start_streamlit()
