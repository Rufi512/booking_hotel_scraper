# booking_hotel_scraper
Scraping a hoteles y departamentos en www.booking.com usando Splash y Django rest

## Instalacion

Compila primero todo los servicios

```bash
  docker-compose up -d --build
```

luego ejecuta y crea las migraciones de django:

```bash
  docker-compose exec web python manage.py makemigrations 

  docker-compose exec web python manage.py migrate 
```

#### Usar psql con Docker
```bash
  docker-compose exec db psql --username=hug58 --dbname=bookingDB
```

#### Para listar todas las database
```bash
    \l
```


#### hacer scraping a otra pagina de booking

```bash
    docker-compose exec web python tools/main.py https://www.booking.com/hotel/cl/ibis-budget-providencia.es.html
```

por ultimo corre la db y gunicorn


```bash
  docker-compose up
```

## Para desmotar la imagen usa el comando

```bash
  docker-compose down -v
```


