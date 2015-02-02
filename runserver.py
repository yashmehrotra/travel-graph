from travelgraph import app

app.run(host='0.0.0.0',debug=True)
# from werkzeug.contrib.fixers import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app)
# app.run(debug=True)
