## README ##

This homework is an exercise to train basic web-development skills with `flask`.

### How to run ###

* Clone current branch and install required modules

`$ git clone https://github.com/anipy/study_stuff.git --branch hw-webapi`

`$ cd study_stuff/hw-webapi`

`$ pip install -r requirements.txt`

* Create a database

`$ python createdb.py`

* Run application

`$ python falsk_app.py`

Now application is avaliable by url `http://127.0.0.1:42069`

### Run via Docker ###

* Clone current branch

`$ git clone https://github.com/anipy/study_stuff.git --branch hw-webapi`

`$ cd study_stuff/hw-webapi`

* Build docker image

`$ docker build --tag inspiring_imgs:0.0.1 .`

* Run docker container

`$ docker run -d --restart=always --name inspiring -p 42069:42069 inspiring_imgs:0.0.1`

Now application is avaliable by url `http://127.0.0.1:42069`

### Available API methods ###

```
    /next               GET     - return random picture and quote
      args:
        source - 'internet' or 'local'
        lang - 'en' or 'ru'
        width - picture width in pixels
        height - picture height in pixels
        render - 1 or 0: render html page or do not

    /quotes             GET     - return list of quotes from DB

    /pictures           GET     - return list of image urls from DB

    /quote/add          POST    - add new quote to DB
      args:
        {'quote': <quote>}

    /quote/<id>         GET     - get quote with id=<id> from DB
    /quote/<id>         PATCH   - update quote with id=<id>
    /quote/<id>         DELETE  - delete quote with id=<id>

    /picture/add        POST    - add new image url
      args:
        {'img_url': <img_url>}

    /picture/<id>       GET     - get picture with id=<id> from DB
      args:
        render - 1 or 0: render an image or not
        width - picture width in pixels
        height - picture height in pixels
    /picture/<id>       PATCH   - update image url in DB
    /picture/<id>       DELETE  - delete image url in DB
```