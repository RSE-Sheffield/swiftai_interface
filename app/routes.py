from flask import render_template, request, redirect, url_for, session
from app import app, redQueue
from app.utils import parse_file_locs
from app.pipelines import methodDict, new_job

@app.route('/')
def home():
    """
    Home endpoint
    """

    return render_template("home.html")

@app.get('/pipeline')
def pipeline_get():
    """
    Pipeline GET endpoint
    
    Renders the pipeline page
    """

    # Get a list of all methods available for selection
    methodList = list(methodDict.keys())
    return render_template("pipeline.html",
                           methodList = methodList)
    
@app.post('/pipeline')
def pipeline_post():
    """
    Pipeline POST endpoint
    
    Adds job to redis queue based on selections
    """

    imageList = session["selected_scans"]
    methodSelect = request.form.get("method")
    method = methodDict.get(methodSelect)

    # Loop though all selected scans and queue them up with the selected
    # pipeline
    for image in imageList:

        # TODO: This needs replacing with something more robust
        file_out = image.replace(".nii.gz", "_segmentation.nii.gz")

        # TODO: If working from XNAT then need a download files and, if 
        # required, convert files job added before running the pipeline

        job = redQueue.enqueue(new_job, method, image, file_out)

        print(job)

    return redirect('queue')

@app.post('/upload_file')
def upload_file():
    """
    Upload file POST endpoint

    Takes csv file selected, uploads and parses it, and rerenders the pipeline
    page populating the scan selection box with the locations contained in file
    """

    if 'file' not in request.files:
         return "No file Part!"
    
    file = request.files.get('file')

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file'

    session['current_file'] = file.filename
    session['scanList'] = parse_file_locs(file.stream)
    return redirect(url_for('pipeline_get'))

@app.post('/clear_file')
def clear_file():
    """
    Clear file POST endpoint

    Removes the currently uploaded file and rerenders the pipeline page
    """
    session['scan_list'] = []
    session['current_file'] = None
    return redirect(url_for('pipeline_get'))

@app.post('/select_source')
def select_source():
    """
    Select source POST endpoint

    Takes selection of data source, updates session info, and rerenders the
    pipeline page.
    """

    session['data_source'] = request.form.get("source")

    # If local source is selected then file upload is allowed straight away
    # Otherwise a connection to an XNAT server must be made before file upload
    if session['data_source'] == "Local":
        session["upload_allowed"] = True
    else:
        session["upload_allowed"] = False

    # If we're already connected to XNAT and change the source from it then we
    # should disconnect before returing to the pipeline page
    if session.get("XNAT_connected") == True and session['data_source'] != "XNAT":
        return redirect(url_for('xnat_disconnect'), code = 307)
    else:
        return redirect(url_for('pipeline_get'))

@app.post('/select_scans')
def select_scans():
    """
    Select scans POST endpoint

    Takes the list of scans selected and adds them to the session data for
    later enqueuing
    """
    if request.form.get("use_all"):
        session["selected_scans"] = session.get("scan_list")
    else:
        session["selected_scans"] = request.form.getlist("image-data")

    return redirect(url_for('pipeline_get'))

@app.post('/xnat_connect')
def xnat_connect():
    """
    XNAT connect POST endpoint

    Currently just a dummy function.
    
    Creates a connection to the specified XNAT server.
    Should return an error/warning if the connection cannot be made.
    """
    session["XNAT_servername"] = request.form.get("XNATurl")
    session["XNAT_connected"] = True

    # Once connection is made then a file with scan locations can be uploaded
    session["upload_allowed"] = True

    return redirect(url_for('pipeline_get'))

@app.post('/xnat_disconnect')
def xnat_disconnect():
    """
    XNAT disconnect POST endpoint

    Currently just a dummy function.

    Disconnects from current XNAT server
    """

    session["XNAT_connected"] = False
    session["upload_allowed"] = False

    return redirect(url_for('pipeline_get'))

@app.post('/reset_session')
def reset_session():
    """
    Reset session POST endpoint

    Clears all session variables.
    """
    session.clear()
    return redirect(url_for('pipeline_get'))

if __name__ == '__main__':
    app.run(debug=True)