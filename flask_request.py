from flask import Flask, request #import main Flask class and request object

app = Flask(__name__) #create the Flask app

@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None
    framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    website = request.args.get('website')

    return '''<h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)

##Form Data Next we have form data. Form data comes from a form that has been sent as a POST request to a route. 
# So instead of seeing the data in the URL (except for cases when the form is submitted with a GET request), 
# the form data will be passed to the app behind the scenes. 
# Even though you can't easily see the form data that gets passed, your app can still read it.

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

# POST body example
# {
#     "language" : "Python",
#     "framework" : "Flask",
#     "website" : "Scotch",
#     "version_info" : {
#         "python" : 3.4,
#         "flask" : 0.12
#     },
#     "examples" : ["query", "form", "json"],
#     "boolean_test" : true
# }

# If the JSON object sent with the request doesn't have a key that is accessed in your view function, 
# then the request will fail. If you don't want it to fail when a key doesn't exist, 
# you'll have to check if the key exists before trying to access it. Here's an example:

# language = None
# if 'language' in req_data:
#     language = req_data['language']

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

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000