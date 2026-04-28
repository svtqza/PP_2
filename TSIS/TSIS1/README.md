# TSIS 1 PhoneBook — Extended Contact Management

## How to run

1. Create database:

```bash
createdb phonebook
```

2. Edit `config.py` and write your real PostgreSQL password.

3. Install psycopg2:

```bash
pip3 install psycopg2-binary
```

4. Run SQL files:

```bash
psql -d phonebook -f schema.sql
psql -d phonebook -f procedures.sql
```

5. Run app:

```bash
python3 phonebook.py
```

## GitHub commands

```bash
git add TSIS1/
git commit -m "Add extended PhoneBook management"
git push origin main
```
