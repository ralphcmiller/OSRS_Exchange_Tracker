#!/bin/bash

# 1. Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv .venv
fi

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install Python packages from requirements.txt
pip install -r requirements.txt

# 4. Run setup-db.py 
python functions/setup-db.py

# 5. Run app.py
python app.py

# Deactivate the virtual environment when done
deactivate
