from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI' : "amqp://guest:guest@localhost"}


@app.route('/compute', methods = ['POST'] )
def compute():

    operation = request.json.get("operation")
    value = request.json.get("value")
    other = request.json.get("other")
    email = request.json.get("email")
    msg = "Please wait result is computed!"
    subject = "Testing"
    with ClusterRpcProxy(CONFIG) as rpc:
        rpc.mail.send.async(email,subject,msg)
        rpc.compute.compute.async(operation,value,other,email)
        return msg,200
app.run(debug = True)