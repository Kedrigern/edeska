# Uřední deska

Prototyp úřední desky / vývěsky napsané ve Flasku (Python3).

Projekt je vytvořen ze skeletonu: https://github.com/realpython/flask-skeleton

## Závislosti

```
pip3 install -r requirments.txt
```


## Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
$ python manage.py create_data
```

### Run the Application

```sh
$ python manage.py runserver
```

So access the application at the address [http://localhost:5000/](http://localhost:5000/)

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```
