# PythonAnywhere Scipts

Requirements are python 3.9 and pip

Getting started
---------------
1. Clone this repo
2. Create a virtual environment with mkvirtual
3. Install the requirements

```bash
$ git clone https://github.com/jeroencvlier/pythonanywhere_scripts.git
$ cd pythonanywhere_scripts
$ mkvirtualenv pyany
$ workon pyany
$ pip install -r requirements.txt
```


```bash
curl -L -o pythonanywhere_scripts-0.2.0-py3-none-any.whl  "https://github.com/jeroencvlier/pythonanywhere-scripts/releases/download/v0.2.0/pythonanywhere_scripts-0.2.0-py3-none-any.whl"
pip install pythonanywhere_scripts-0.2.0-py3-none-any.whl

```

Be sure to have the environment variables set in the .env file

To use the local sync, supply the cronjob with the correct path to the script

```bash
11 23 * * * /Users/jeroenvanlier/miniconda3/envs/pyany/bin/python /Users/jeroenvanlier/Documents/Github/pythonanywhere_scripts/src/local_rsync.py >> /Users/jeroenvanlier/Documents/Github/pythonanywhere_scripts/logs/local_rsync_logfile.log 2>&1
```