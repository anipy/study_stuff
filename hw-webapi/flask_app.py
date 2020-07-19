"""Small Flask application to combine quotes by Forismatic.Com (http://forismatic.com/en/api/)
    and pictures by Lorem Picsum (https://picsum.photos/) together.

    You can also add your own quotes and picture urls into SQLite DB and randomly combine them.

    Existing API methods:

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
"""

import sqlite3
from functools import wraps

import requests
from werkzeug.exceptions import abort

from config import DB, DEFAULT_IMAGE, DEFAULT_QUOTE
from flask import Flask, jsonify, request, url_for
from waitress import serve

app = Flask(__name__)


def db_connect(func):
    """Decorator to launch function execution on database"""

    @wraps(func)
    def wrapper_func(*a, **kw):
        with sqlite3.connect(DB) as db:
            crs = db.cursor()
            ret_value = func(crs, *a, **kw)
            db.commit()
        return ret_value

    return wrapper_func


@db_connect
def _get_random_entry(crs: sqlite3.Cursor, table: str) -> str:
    """Get random entry from given table

    Args:
      crs: sqlite3.Cursor to execute sql query

      table: table name to select random entry from

    Returns:
      Text value of entry
    """
    query_res = crs.execute(f"select * from {table} order by random() limit 1;")
    if query_res:
        query_res = query_res.fetchall()
        return query_res[0][1] if query_res else str()
    else:
        return str()


@db_connect
def _get_entry_by_id(crs: sqlite3.Cursor, eid: int, table: str) -> list:
    """Get specific entry from table by its id

    Args:
      crs: sqlite3.Cursor to execute sql query

      eid: entry id

      table: table name to select from

    Returns:
      A list of entries matching condition
    """
    query_res = crs.execute(f"select * from {table} where id=:eid", {"eid": eid})
    if query_res:
        return query_res.fetchall()
    else:
        return list()


@db_connect
def _del_entry_by_id(crs: sqlite3.Cursor, eid: int, table: str) -> int:
    """Delete entry from table

    Args:
      crs: sqlite3.Cursor to execute sql query

      eid: entry id

      table: table name to delete from

    Returns:
      Integer ID of deleted entry
    """
    if crs.execute(f"delete from {table} where id=:eid", {"eid": eid}):
        return eid
    else:
        return -1


@db_connect
def _upd_entry_by_id(crs: sqlite3.Cursor, eid: int, new_value: str, table: str) -> int:
    """Update value of specific entry by its id

    Args:
      crs: sqlite3.Cursor to execute sql query

      eid: entry id

      new_value: value to set up as new one

      table: table name for update operation

    Returns:
      Integer ID of updated entry
    """
    if crs.execute(
        f"update {table} set txt=:new_val where id=:eid",
        {"eid": eid, "new_val": new_value},
    ):
        return eid
    else:
        return -1


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    """Main page"""
    return "<h1>Inspiring thoughts... Go to /next</h1>"


@app.route("/next", methods=["GET"])
def next_thought():
    """Page of random inspiring thoughts

    Http args:
      source: defines which source to use: either `internet` or `local` (SQLite DataBase)

      width: width for return picture

      height: height fot return picture

      lang: defines which language to use: either `en` or `ru`

      render: if 1 - response is HTML, if 0 - response is JSON
    """
    source = request.args.get("source", default="internet", type=str)
    width = request.args.get("width", default=600, type=int)
    height = request.args.get("height", default=400, type=int)
    lang = request.args.get("lang", default="en", type=int)
    render = request.args.get("render", default=1, type=int)

    if source == "internet":
        picture_url = f"https://picsum.photos/{width}/{height}?grayscale=true"
        quote_text = requests.post(
            "http://api.forismatic.com/api/1.0/",
            params={"method": "getQuote", "format": "json", "lang": lang},
        ).json()["quoteText"]
    elif source == "local":
        picture_url = _get_random_entry("images") or url_for(
            "static", filename=DEFAULT_IMAGE
        )
        quote_text = _get_random_entry("quotes") or DEFAULT_QUOTE

    else:
        picture_url = url_for("static", filename=DEFAULT_IMAGE)
        quote_text = DEFAULT_QUOTE

    if render:
        return (
            f'<h2 align="center">{quote_text}</h2>'
            f'<div align="center">'
            f"<img src={picture_url} height={height} width={width} /></div>"
        )
    else:
        return jsonify(picture_url=picture_url, quote_text=quote_text)


@app.route("/quotes", methods=["GET"])
@db_connect
def quote_list(crs: sqlite3.Cursor):
    """Get all quotes from DB"""
    quotes = crs.execute("select * from quotes")
    return jsonify(quotes.fetchall())


@app.route("/pictures", methods=["GET"])
@db_connect
def picture_list(crs: sqlite3.Cursor):
    """Get all picture urls from DB"""
    pictures = crs.execute("select * from images")
    return jsonify(pictures.fetchall())


@app.route("/quote/add", methods=["POST"])
@db_connect
def quote_add(crs: sqlite3.Cursor):
    """Insert new quote into DB"""
    crs.execute(
        "insert into quotes (txt) values (:quote)", {"quote": request.json["quote"]}
    )
    return jsonify({"id": crs.lastrowid, "table": "quotes"}), 201


@app.route("/picture/add", methods=["POST"])
@db_connect
def picture_add(crs: sqlite3.Cursor):
    """Insert new picture url into DB"""
    crs.execute(
        "insert into images (txt) values (:img_url)",
        {"img_url": request.json["img_url"]},
    )
    return jsonify({"id": crs.lastrowid, "table": "images"}), 201


@app.route("/quote/<int:qid>", methods=["GET", "PATCH", "DELETE"])
def quote_process(qid: int):
    """Process quote by its id"""
    if request.method == "GET":
        return jsonify(
            _get_entry_by_id(eid=qid, table="quotes") or [[-1, DEFAULT_QUOTE]]
        )
    elif request.method == "PATCH":
        return jsonify(
            _upd_entry_by_id(eid=qid, new_value=request.json["quote"], table="quotes")
        )
    elif request.method == "DELETE":
        return jsonify(_del_entry_by_id(eid=qid, table="quotes"))
    else:
        abort(400)


@app.route("/picture/<int:pid>", methods=["GET", "PATCH", "DELETE"])
def picture_process(pid: int):
    """Process picture by its id

    Http args (for GET method only):
      render: if 1 - response is HTML, if 0 - response is JSON

      width: width for return picture

      height: height fot return picture
    """
    if request.method == "GET":
        render = request.args.get("render", default=1, type=int)
        width = request.args.get("width", default=600, type=int)
        height = request.args.get("height", default=400, type=int)
        img_url = _get_entry_by_id(eid=pid, table="images") or [
            [-1, url_for("static", filename=DEFAULT_IMAGE)]
        ]
        if not render:
            return jsonify(img_url)
        else:
            return f'<img src="{img_url[0][1]}" height={height} width={width}/>'

    elif request.method == "PATCH":
        return jsonify(
            _upd_entry_by_id(eid=pid, new_value=request.json["img_url"], table="images")
        )

    elif request.method == "DELETE":
        return jsonify(_del_entry_by_id(eid=pid, table="images"))

    else:
        abort(400)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=42069)
