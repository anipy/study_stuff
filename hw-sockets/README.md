## README ##

This homework is an exercise to train basic sockets skills with `socket` library.

### How to run ###

* Clone current branch

`$ git clone https://github.com/anipy/study_stuff.git --branch hw-sockets`

`$ cd study_stuff/hw-sockets`

* Run on server host

`$ nohup python server.py --port 13072 > /dev/null 2>&1`

* Run on client host

`$ python client.py --host {server-host} --port 13072`
