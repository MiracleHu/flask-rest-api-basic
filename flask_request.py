import os
from flask import Flask, flash, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
from zipfile import ZipFile, is_zipfile
import json

UPLOAD_FOLDER = '/Users/huh/Desktop'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# http://localhost:5000/query-example?language=en&framework=&website=
@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None
    framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    website = request.args.get('website')

    return '''<h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)

'''
Form Data Next we have form data. Form data comes from a form that has been sent as a POST request to a route. 
So instead of seeing the data in the URL (except for cases when the form is submitted with a GET request), 
the form data will be passed to the app behind the scenes. 
Even though you can't easily see the form data that gets passed, your app can still read it.
'''

# To demonstrate this, modify the form-example route to accept both GET and POST requests and to return a simple form.
@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST': #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework) # fill the template

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

'''
POST body example
{
    "language" : "Python",
    "framework" : "Flask",
    "website" : "Scotch",
    "version_info" : {
        "python" : 3.4,
        "flask" : 0.12
    },
    "examples" : ["query", "form", "json"],
    "boolean_test" : true
}
'''

'''
If the JSON object sent with the request doesn't have a key that is accessed in your view function, 
then the request will fail. If you don't want it to fail when a key doesn't exist, 
you'll have to check if the key exists before trying to access it. Here's an example:

language = None
if 'language' in req_data:
    language = req_data['language']
'''

@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    # assign everything from the JSON object into a variable using request.get_json()
    req_data = request.get_json()

    language = req_data['language']
    framework = req_data['framework']
    python_version = req_data['version_info']['python'] #two keys are needed because of the nested object
    example = req_data['examples'][0] #an index is needed because of the array
    boolean_test = req_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

@app.route('/test', methods=['GET']) #GET requests will be blocked
def test_example():
    # assign everything from the JSON object into a variable using request.get_json()
    return 'OK'

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/api/v1/fabric/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         print('request.files', request.files)
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         print('file:---->', file)
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         # if file.filename == '':
#         #     flash('No selected file')
#         #     return redirect(request.url)
#         # if file and allowed_file(file.filename):
#         #     filename = secure_filename(file.filename)
#         #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #     return redirect(url_for('uploaded_file',
#         #                             filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''


@app.route('/api/v1/fabric/upload/hubs', methods=['PUT']) #GET requests will be blocked
def test_upload():
    print('request.files:', request.files)
    # # ImmutableMultiDict([('', <FileStorage: 'testzip.zip' ('application/zip')>)]
    # # Attention: '' in ImmutableMultiDict is the file name in zip file
    file = request.files['']
    if not file:
        print('No file part')
    print('file name:', file.filename)
    print('is is_zipfile:', is_zipfile(file))
    res = ''
    with ZipFile(file, 'r') as req_zip:
        # # printing all the contents of the zip file
        req_zip.printdir()
        print('req_zip.getinfo("hub/"):', req_zip.getinfo('hub/'))
        print('req_zip.namelist():', req_zip.namelist())
        
        with req_zip.open('hub/hub2/hub_output.json') as req_file:
            res = req_file.read()
            # print(res)
            parsed = json.loads(res)
            print('network_id:', parsed['network_id'])
            # print('parsed:', parsed)
        # # extracting all the files
        # print('Extracting all the files now...')
        # req_zip.extractall()
        # print('Done!')
    return Response(response=json.dumps({"status": "success", "json": parsed}), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000