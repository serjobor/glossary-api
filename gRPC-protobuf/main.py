from flask import Flask, render_template, request, redirect, url_for
import grpc
import glossary_pb2
import glossary_pb2_grpc

app = Flask(__name__)

# gRPC-клиент
channel = grpc.insecure_channel("localhost:50051")
stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

@app.route("/")
def index():
    terms = stub.ListTerms(glossary_pb2.Empty()).entries
    return render_template("index.html", terms=terms)

@app.route("/term/<string:name>")
def term(name):
    try:
        entry = stub.GetTerm(glossary_pb2.GetTermRequest(term=name))
        if not entry.definition:
            raise grpc.RpcError()
        return render_template("term.html", term=entry)
    except grpc.RpcError:
        return render_template("term.html", term=None, name=name)

@app.route("/add", methods=["POST"])
def add_term():
    name = request.form["term"]
    definition = request.form["definition"]
    stub.CreateTerm(glossary_pb2.CreateTermRequest(term=name, definition=definition))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
