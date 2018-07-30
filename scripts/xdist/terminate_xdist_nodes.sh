#!/bin/bash
set -e

echo "Terminating xdist containers with pytest_container_manager.py"
xdist_task_arns=$(<xdist_files/${XDIST_FILE_NAME_PREFIX}_task_arns.txt)
python scripts/xdist/pytest_container_manager.py -a down --task_arns ${xdist_task_arns}
