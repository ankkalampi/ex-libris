# Pylint-raportti

Pylint antaa seuraavanlaisen raportin sovelluksesta:

```
************* Module src.services.user
src/services/user.py:11:18: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
src/services/user.py:26:19: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
************* Module src.services.book
src/services/book.py:18:64: C0103: Argument name "ISBN" doesn't conform to snake_case naming style (invalid-name)
src/services/book.py:18:0: R0913: Too many arguments (9/5) (too-many-arguments)
src/services/book.py:18:0: R0914: Too many local variables (16/15) (too-many-locals)
src/services/book.py:78:55: C0103: Argument name "ISBN" doesn't conform to snake_case naming style (invalid-name)
src/services/book.py:78:0: R0913: Too many arguments (8/5) (too-many-arguments)
src/services/book.py:247:0: R0913: Too many arguments (7/5) (too-many-arguments)
************* Module src.services.db
src/services/db.py:17:14: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
src/services/db.py:25:8: E0237: Assigning to attribute 'connection' not defined in class slots (assigning-non-slot)
src/services/db.py:27:8: W0102: Dangerous default value [] as argument (dangerous-default-value)
src/services/db.py:29:12: E0237: Assigning to attribute 'last_insert_id' not defined in class slots (assigning-non-slot)
src/services/db.py:31:8: E0237: Assigning to attribute 'db_execute' not defined in class slots (assigning-non-slot)
src/services/db.py:37:8: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
src/services/db.py:45:13: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
src/services/db.py:53:8: E0237: Assigning to attribute 'connection' not defined in class slots (assigning-non-slot)
src/services/db.py:55:8: W0102: Dangerous default value [] as argument (dangerous-default-value)
src/services/db.py:59:8: E0237: Assigning to attribute 'db_query' not defined in class slots (assigning-non-slot)
src/services/db.py:63:8: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
************* Module src.routes.user_routes
src/routes/user_routes.py:26:11: W0703: Catching too general exception Exception (broad-except)
************* Module src.routes.view_routes
src/routes/view_routes.py:36:11: W0703: Catching too general exception Exception (broad-except)
src/routes/view_routes.py:64:11: W0703: Catching too general exception Exception (broad-except)
src/routes/view_routes.py:72:19: W0613: Unused argument 'username' (unused-argument)
src/routes/view_routes.py:98:11: W0703: Catching too general exception Exception (broad-except)
src/routes/view_routes.py:103:11: W0703: Catching too general exception Exception (broad-except)
src/routes/view_routes.py:147:11: W0703: Catching too general exception Exception (broad-except)
src/routes/view_routes.py:134:21: W0613: Unused argument 'username' (unused-argument)
src/routes/view_routes.py:181:15: W0703: Catching too general exception Exception (broad-except)
************* Module src.routes.book_routes
src/routes/book_routes.py:62:11: W0703: Catching too general exception Exception (broad-except)
src/routes/book_routes.py:62:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
src/routes/book_routes.py:93:4: C0103: Variable name "ISBN" doesn't conform to snake_case naming style (invalid-name)
src/routes/book_routes.py:106:8: C0103: Variable name "ISBN" doesn't conform to snake_case naming style (invalid-name)
src/routes/book_routes.py:128:11: W0703: Catching too general exception Exception (broad-except)
src/routes/book_routes.py:122:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
src/routes/book_routes.py:128:4: C0103: Variable name "e" doesn't conform to snake_case naming style (invalid-name)
src/routes/book_routes.py:165:11: W0703: Catching too general exception Exception (broad-except)
************* Module src.routes.shelf_routes
src/routes/shelf_routes.py:47:11: W0703: Catching too general exception Exception (broad-except)
src/routes/shelf_routes.py:70:11: W0703: Catching too general exception Exception (broad-except)

------------------------------------------------------------------
Your code has been rated at 8.59/10 (previous run: 8.57/10, +0.02)

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

