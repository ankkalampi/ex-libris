# Pylint-raportti

Pylint antaa seuraavanlaisen raportin sovelluksesta:

```
************* Module app
app.py:32:8: E0237: Assigning to attribute 'user' not defined in class slots (assigning-non-slot)
app.py:34:8: E0237: Assigning to attribute 'user' not defined in class slots (assigning-non-slot)
app.py:41:4: E0237: Assigning to attribute 'start_time' not defined in class slots (assigning-non-slot)
app.py:102:11: W0703: Catching too general exception Exception (broad-except)
app.py:102:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
app.py:134:4: C0103: Variable name "ISBN" doesn't conform to snake_case naming style (invalid-name)
app.py:147:8: C0103: Variable name "ISBN" doesn't conform to snake_case naming style (invalid-name)
app.py:169:11: W0703: Catching too general exception Exception (broad-except)
app.py:163:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
app.py:169:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
app.py:206:11: W0703: Catching too general exception Exception (broad-except)
app.py:256:11: W0703: Catching too general exception Exception (broad-except)
app.py:280:11: W0703: Catching too general exception Exception (broad-except)
app.py:303:11: W0703: Catching too general exception Exception (broad-except)
app.py:321:11: W0703: Catching too general exception Exception (broad-except)
app.py:321:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
app.py:356:11: W0703: Catching too general exception Exception (broad-except)
app.py:356:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
app.py:388:11: W0703: Catching too general exception Exception (broad-except)
app.py:398:19: W0613: Unused argument 'username' (unused-argument)
app.py:430:11: W0703: Catching too general exception Exception (broad-except)
app.py:435:11: W0703: Catching too general exception Exception (broad-except)
app.py:502:11: W0703: Catching too general exception Exception (broad-except)
app.py:489:21: W0613: Unused argument 'username' (unused-argument)
app.py:576:15: W0703: Catching too general exception Exception (broad-except)
************* Module book
book.py:18:64: C0103: Argument name "ISBN" doesn't conform to snake_case naming style (invalid-name)
book.py:18:0: R0913: Too many arguments (9/5) (too-many-arguments)
book.py:54:55: C0103: Argument name "ISBN" doesn't conform to snake_case naming style (invalid-name)
book.py:54:0: R0913: Too many arguments (8/5) (too-many-arguments)
book.py:242:0: R0913: Too many arguments (7/5) (too-many-arguments)
book.py:309:0: R0913: Too many arguments (9/5) (too-many-arguments)
book.py:309:0: R0914: Too many local variables (16/15) (too-many-locals)
************* Module db
db.py:17:14: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
db.py:25:8: E0237: Assigning to attribute 'connection' not defined in class slots (assigning-non-slot)
db.py:27:8: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:29:12: E0237: Assigning to attribute 'last_insert_id' not defined in class slots (assigning-non-slot)
db.py:31:8: E0237: Assigning to attribute 'db_execute' not defined in class slots (assigning-non-slot)
db.py:37:8: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
db.py:45:13: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
db.py:53:8: E0237: Assigning to attribute 'connection' not defined in class slots (assigning-non-slot)
db.py:55:8: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:59:8: E0237: Assigning to attribute 'db_query' not defined in class slots (assigning-non-slot)
db.py:63:8: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
************* Module init_db
init_db.py:12:7: W0703: Catching too general exception Exception (broad-except)
init_db.py:22:5: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
************* Module seed
seed.py:35:0: C0103: Constant name "shelf_id" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:36:0: C0103: Constant name "book_id" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:44:11: W0703: Catching too general exception Exception (broad-except)
************* Module user
user.py:11:18: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
user.py:26:19: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 8.44/10 (previous run: 8.35/10, +0.10)

```

Perustellaan, miksi näitä huomioita ei ole korjattu sovelluksessa:

## Too many arguments ja too many local variables

Ylitykset näissä eivät ole suuria, ja argumenttien sekä muuttujien määrät ovat perusteltuja.

## Argument/variable name doesn't conform to snake_case naming style

Nämä ovat pääosin poikkeuskäsittelyn ja dekoraattorien apumuuttujia, joiden lyhyet nimet ovat perusteltuja. ISBN-muuttujan kohdalla on tehty päätös isojen kirjaimien käyttämisestä, koska ISBN kirjoitetaan isoilla kirjaimilla.

## Unused argument "username"

Flask tarvitsee tätä argumenttia reitin hakemiseen.

## Catching too general Exception

Tämä tapa hallita poikkeuksia on tämän sovelluksen kontekstissa riittävä.

## Dangerous default value [] ja Assigning to attribute not defined in class slots

Nämä liittyvät tietokantafunktioiden dekoraattoreihin. Molempien varoitusten tapauksessa valittu menettely on turvallinen.

## Constant name "shelf_id" doesn't conform to UPPER_CASE naming style ja Constant name "book_id" doesn't conform to UPPER_CASE naming style 

Nämä eivät todellisuudessa ole vakioarvoja, joten niille ei kuulu UPPER_CASE -nimeämistyyli. 

