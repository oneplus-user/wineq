create env 

```bash
conda create -n wineq python=3.11.4 -y
python --version # to see the verison installed
```

activate env
```bash
conda activate wineq
```

create a req file and install the req
```bash
pip install -r requirements.txt
```

create template.py to generate folder(with .gitkeep) & files structures. Then run it with:
-> python template.py

download the data from 
https://drive.google.com/drive/folders/18zqQiCJVgF7uzXgfbIJ-04zgz1ItNfF5?usp=sharing
to data_given folder

```bash
git init
```
```bash
dvc init 
```
```bash
dvc add data_given/winequality.csv
```

```bash
git remote add origin https://github.com/oneplus-user/wineq.git #add remote repo given(name): origin and URL to specify remote [ONE TIME]
git branch -M main #in local, to change current branch name from master to main[ONE TIME]
```

```bash
git pull # to pull all the files in remote(NOTE: It will not alter changes made in local)
```
```bash
git add . && git commit -m "first commit"
#in local, add . means to add all files for versioning purpose
#in local, and commit to changes(Its like saying its final)
```
```bash
git push origin main #push all the changes commited in local
```

Next 
1. we generate params.yaml files.
2. we create file inside src named:get_data.py --> touch src/get_data.py
Note:
we tried to import pandas but currently pandas is not there. How we know this?
In terminal@MLOps level:(for any python commands, first type python) like below and exit
-> python
-> import pandas (will give error, so exit)
-> exit()
Hence add pandas in requirements.txt and separately in terminal@MLOps level:
-> pip install pandas

then add content of get_data.py to get data from s3
then add content of load_data.py to load and save data to data/raw folder
then add stage in dvc.yaml for above
-> dvc repro















tox command -
```bash
tox
```
for rebuilding -
```bash
tox -r 
```
pytest command
```bash
pytest -v
```

setup commands -
```bash
pip install -e . 
```

build your own package commands- 
```bash
python setup.py sdist bdist_wheel
```