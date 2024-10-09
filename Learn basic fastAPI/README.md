# * Setup

```
# Move to folder /Learn basic fastAPI/app (as working directory),
# it important to run python command in this folder 
# because we use import in code base on condition that this folder is root dir

# Create env
python -m venv venv
source /venv/bin/active

# Install requirement in requirement.txt (in Fast API folder)
# Run app by command
uvicorn main:app --reload

# create file migration automaticaly by
alembic revision --autogenerate -m "<migation_name>"
```
