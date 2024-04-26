# swiftai_interface
Web/Flask based interface for the swiftai pipeline


## Installation instructions

- Clone this repository
- Setup conda env
- Install requirements.txt for this repo
- Download and install `swiftai` wheel file
- Clone [`swiftai` repo](https://github.com/mrsharkleton/swiftai)
    - Ideally use branch were package can be installed with pip
- install requirements.txt for `swiftai`
- Clone [`xnat_connect` repo](https://github.com/mrsharkleton/xnat_connect)
- install requirements.txt for `xnat_connect`
- pip install `xnat_connect`


## Run the interface

`flask --app app run`

Include `--debug` flag for development work (so code reloads after changes)


## Run the worker

If not using docker, by default the jobs will be added to the queue, but will not be processed until a worker is started.

Use the command (typically in another terminal on the same machine) `rq worker` to start the worker

When using docker there will be a worker container that is automatically started when all the containers start.
