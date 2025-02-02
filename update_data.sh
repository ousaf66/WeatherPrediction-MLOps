#!/bin/bash

# Navigate to the project directory (use quotes or backslashes for spaces)
cd "/Users/yousaf/Desktop/untitled folder 9/course-project-ousaf66" || exit

# Run the data collection script
# Since we are now in the project directory, we can just do:
# (Make sure collect_data.py is in this directory)
source env/bin/activate   # If you are using a virtual environment named 'env'

/usr/bin/python3 ./collect_data.py

# Add new or updated data to DVC tracking
dvc add data/

# Stage the DVC files and data changes in Git
git add data.dvc .gitignore data/
git commit -m "Update forecast data: $(date '+%Y-%m-%d %H:%M:%S')"

# Push data to DVC remote
dvc push

# Push changes to Git remote
git push origin main
