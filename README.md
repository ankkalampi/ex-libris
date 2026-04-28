# Ex Libris - Sovellus kirjakokoelmien selailuun ja esittelyyn

## Sovelluksen toiminnot 

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään uuden kirjahyllyn. Kirjahyllyn voi määritellä julkiseksi tai yksityiseksi, ja sille voi määritellä sekä nimen että lyhyen kuvauksen.
- Käyttäjä voi tarkastella kirjahyllyjään listana ja valita listalta hyllyn tarkasteltavaksi.
	
- Käyttäjä pystyy lisäämään uuden kirjan tiedot (nimi, kirjoittaja, sivumäärä, ISBN(vapaaehtoinen), julkaisuvuosi(vapaaehtoinen), genretägi(vapaaehtoinen)).
- Käyttäjä voi tarkastella kirjahyllyään listana.
- Käyttäjä pystyy valitsemaan kirjan hyllynäkymästä ja siirtymään kirjanäkymään.
- Kirjanäkymässä käyttäjä voi muokata kirjan tietoja tai poistaa kirjan.
- Käyttäjä voi etsiä kirjaa nimen, kirjailijan, ISBN:n, julkaisuvuoden tai genretägien perusteella. Haussa käyttäjä voi määrittää, etsitäänkö kirjaa vain omista hyllyistä, vai myös muiden käyttäjien julkisista hyllyistä.

## Sovelluksen käyttöönotto

Kloonaa repositorio itsellesi:

```
git clone https://github.com/ankkalampi/ex-libris.git
```

Siirry kansioon, jonne kloonasit repositorion:

```
cd ex-libris
``` 

Asenna flask, jos se ei ole asennettuna:

```
pip install flask
```

Alusta tietokanta:

```
python init_db.py
```

Käynnistä sovellus:

```
python -m flask run
```

## Sovelluksen testaaminen suurella tietomäärällä

Suorita ensin sovelluksen käyttöönotossa kuvaillut vaiheet, jos et ole suorittanut niitä. Jos olet jo ottanut sovelluksen käyttöön, riittää suorittaa:
```
python init_db.py
```

Aja sitten seed.py:

```
python seed.py
```

Tämän jälkeen tietokannassa on runsaasti kirjoja, hyllyjä ja käyttäjiä. Muokkaamalla seuraavia kohtia seed.py:ssä, voit vaikuttaa käyttäjien, käyttäjäkohtaisten hyllyjen sekä hyllykohtaisten kirjojen määrään:

```
USER_COUNT = 200
SHELF_COUNT_PER_USER = 20
BOOK_COUNT_PER_USER = 500
```

Jos haluat ajaa seed.py:n uudestaan muokatuilla arvoilla, aja sitä ennen uudestaan:
```
python init_db.py
```

Testataksesi sovellusta käynnistä sovellus:
```
python -m flask run
```

Seed.py luo käyttäjiä, joiden käyttänimet ovat muotoa "user" + järjestysnumero, eli esim "user34". Kaikkien salasana on "password".

Kutsuun mennyt aika näkyy konsolissa kutsun tietojen alla esimerkiksi näin:
```
127.0.0.1 - - [28/Apr/2026 10:32:57] "GET /static/main.css HTTP/1.1" 304 -
elapsed time  0.44  s
```
