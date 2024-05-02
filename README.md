# swiftai_interface
Web/Flask based interface for the swiftai pipeline


## Installation instructions

- Clone this repository
- Setup conda env
- Install requirements.txt for this repo
- Download and install `swiftai` wheel file
- install requirements.txt for `swiftai`
    - Unsure if they are included as part of installing the wheel, I had to clone the `swiftai` repo and install `requirements.txt` as a seperate step
- Clone [`xnat_connect` repo](https://github.com/mrsharkleton/xnat_connect)
- install requirements.txt for `xnat_connect`
- pip install `xnat_connect`


## Run the interface

Use `flask --app app run` for development work.  
Optinally include `--debug` flag so code reloads after changes.  

Use `gunicorn --bind 0.0.0.0:8000 app:app` for deployment on Port 8000 of a server  

## Run the worker

By default the jobs will be added to the queue, but will not be processed until a worker is started.  
Use the command (typically in another terminal on the same machine) `rq worker` to start the worker


## Status of interface

### Features working

#### Run Local Jobs
The interface can be used to specify the location of local files to be processed.  
This is done by uploading a csv file with a column name with 'Location' (case-sensitive) in it. e.g. `fileLocation`.  
Upon upload the interface will present the list of files for proccessing, these can be selected and de-selected as required.  
When completed the file will be saved to the output directory (see below), with the pipeline name appended to the end.  
If a file specified deosn't exist the job will not be queued.  

#### Specify output directory
When running locally the files will always be saved in a folder called `data_out` in the user's home directory.  
You can optionally specify a sub-directory name in the "Select pipeline" section of the interface.  
If left blank this will default to the name of the pipeline being run (e.g. `Spleen_Segment` if the `Spleen Segment` pipeline is chosen).  

#### Prioritise jobs on add
By default any new job will be added to the back of the processing queue.  
However, if the 'Prioritise job' checkbox in the "Select pipeline" section of the interface is checked, the added jobs will be put at the front of the queue.  

#### View queues
The status of the queues can be seen on the `/queue`.  
This page is produced by the `rq-dashboard` package, and so isn't fully integrated into the interface (i.e. no links back to the main page).  
The page includes information about the currently queued jobs, running jobs, comleted jobs, and failed jobs (including traceback).


### Features not working

#### Interfacing with XNAT server
While there is the option for using XNAT as a source, this is only a dummy interface and doesn't actually connect to anything.  
Should be relatively straightforward to get connected with the xnatconnect package

#### Processing files from XNAT server
Needs functionallity for downloading the selected scans from the XNAT server and, if required, converting them to an appropriate format for processing.  
I've added some comments to the code to indicate what I think would need to be done and where, but essentially there needs to be steps for: 
- Checking if the current source is an XNAT server  
- Does the specified scan exist on the server?  
- If yes, download the scan from the XNAT server  
- Is the scan in the right format, convert if not  

For the 'Download' and 'Convert' steps it would be possible to add them to the queue, and make any following steps wait until they are done (using the `depends_on` parameter of the `enqueue()` function).

#### General error signalling
Currently there is little in the way of error messages indicating to an end user something has gone wrong. This could be improved.


## Using docker

> [!WARNING]
> This doesn't work yet

Need to make sure all files and repos are downloaded (as describe above)
`docker compose up`
