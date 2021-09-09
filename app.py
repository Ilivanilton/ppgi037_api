import datetime
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load


#### Bootstrap ########################################

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/db.db"
db = SQLAlchemy(app)


##### MODELS ###########################################

class Paciente(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))


##### SCHEMAS ##########################################

class PacienteSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

    def format_name(self, paciente):
        return "{}".format(paciente.name)


#### Validacoes #########################################

def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


paciente_schema = PacienteSchema()
pacientes_schema = PacienteSchema(many=True)



##### API Pacientes ######################################

#### READ_ALL

@app.route("/pacientes/", methods=["GET"])
def get_pacientes():
    pacientes = Paciente.query.all()
    # Serialize the queryset
    result = pacientes_schema.dump(pacientes)
    return {"pacientes": result}


#### READ

@app.route("/pacientes/<int:pk>", methods=["GET"])
def get_paciente(pk):
    try:
        paciente = Paciente.query.filter(Paciente.id == pk).one()
    except NoResultFound:
        return {"message": "Paciente could not be found."}, 400
    paciente_result = paciente_schema.dump(paciente)
    return {"paciente": paciente_result}


#### UPDATE

@app.route('/pacientes/<int:pk>', methods=['PUT'])
def update_paciente(pk):
    data = request.get_json()
    try:
        paciente = Paciente.query.filter(Paciente.id == pk).one()
    except NoResultFound:
        return {"message": "Paciente could not be found."}, 400
    if data.get('name'):
        paciente.name = data['name']
    db.session.add(paciente)
    db.session.commit()
    result = paciente_schema.dump(paciente)
    return {"message": "edited!"}

#### DELETE

@app.route('/pacientes/<int:pk>', methods=['DELETE'])
def delete_paciente(pk):
    try:
        paciente = Paciente.query.filter(Paciente.id == pk).one()
    except NoResultFound:
        return {"message": "Paciente could not be found."}, 400
    db.session.delete(paciente)
    db.session.commit()
    return {"message": "Paciente deleted!"}


#### CREATE

@app.route("/pacientes/", methods=["POST"])
def new_paciente():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = paciente_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    name = data["name"]
    paciente = Paciente.query.filter_by(name=name).first()
    if paciente is None:
        # Create a new paciente
        paciente = Paciente(name=name)
        db.session.add(paciente)
    db.session.commit()
    return {"message": "Created new Paciente."}


## API IA
@app.route("/recomendacao1/", methods=["POST"])
def recomendacao1:
    pass

def recomendacao2:
    pass




### MAIN ######################################

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)