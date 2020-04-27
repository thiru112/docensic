# DOCKENSIC
A simple tool than will collect artifacts, executables, snapshot from docker container and its environments

> It works on Docker api engine and in file system commands

### Change the configuration file

Change the `config.json.sample` to `config.json`

- If the target system has Docker API enabled the configure the `IP` and `PORT`

### To run
> `root@example:~/dockensic# python3 src/dockensic.py [OPTIONS]`

- #### Don't run the `dockensic.py` from the `src` directoy.
- Because it breaks the script
