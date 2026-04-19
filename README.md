# Fitness tracking app project
## IDATG2002 - Group 5

Group members: \
Gabriel Brindle \
Odin Arvhage \
Didrik Christoffer Bråten \
Sondre Odberg
## How to run
Clone this repository.

add file ```.env```
where contents would be:
```
DB_HOST={ip to database}
DB_PORT=3306
DB_NAME={database name}
DB_USER={db username}
DB_PASSWORD= {db password}

```

Then, go to your terminal and type
```
python -m venv .venv
```
This should create a .venv folder.

Run
```
.venv\Scripts\activate.bat
```

Then, use pip to install streamlit:
```
pip install -r requirements.txt
```

That should be everything, to execute the program run
```
python -m streamlit run main.py
```