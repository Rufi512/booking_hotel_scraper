# booking_hotel_scraper
Scraping a hoteles y departamentos en www.booking.com usando Splash y Django rest

## Instalacion

Compila primero todo los servicios

```bash
  docker-compose build
```

luego ejecuta y crea las migraciones de django:


```bash
  docker-compose run web bash -c "python manage.py makemigrations && python manage.py migrate"
```

por ultimo corre docker


```bash
  docker-compose up
```

## hacer scraping a otra pagina de booking

```bash
  docker-compose run web python tools/main.py https://www.booking.com/hotel/cl/ibis-budget-providencia.es.html
```

## Para desmotar la imagen usa el comando

```bash
  docker-compose down
```


