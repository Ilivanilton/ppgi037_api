# -*- coding: utf-8 -*-

from datetime import date 
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load
from tde_r08 import gera_lista_branca
from unidecode import unidecode

from json import dumps
from json import JSONEncoder



#### Bootstrap ########################################

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db = SQLAlchemy(app)


##### MODELS ###########################################

class Paciente(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    num = db.Column(db.Integer)
    sexo = db.Column(db.Integer)
    data_consulta = db.Column(db.DateTime)
    idade = db.Column(db.Integer)
    local = db.Column(db.String(150))
    hipertencao = db.Column(db.Integer)
    diabetes = db.Column(db.Integer)
    figado = db.Column(db.Integer)
    rins = db.Column(db.Integer)
    gravidez = db.Column(db.Integer)
    alergias = db.Column(db.String(200))
    reclamacao_do_paciente = db.Column(db.Text)
    apos_diagnostico = db.Column(db.String(80))
    altura = db.Column(db.Float)
    peso = db.Column(db.Float)

##### SCHEMAS ##########################################

class PacienteSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    num = fields.Int()
    sexo = fields.Int()
    data_consulta = fields.Date()
    idade = fields.Int()
    local = fields.Str()
    hipertencao = fields.Int()
    diabetes = fields.Int()
    figado = fields.Int()
    rins = fields.Int()
    gravidez = fields.Int()
    alergias = fields.Str()
    reclamacao_do_paciente = fields.Str()
    apos_diagnostico = fields.Str()
    altura = fields.Number()
    peso = fields.Number()

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
    if data.get('alergias'):
        paciente.alergias = data['alergias']
    if data.get('data_consulta'):
        paciente.data_consulta = data['data_consulta']
    if data.get('diabetes'):
        paciente.diabetes = data['diabetes']
    if data.get('figado'):
        paciente.figado = data['figado']
    if data.get('gravidez'):
        paciente.gravidez = data['gravidez']
    if data.get('hipertencao'):
        paciente.hipertencao = data['hipertencao']
    if data.get('idade'):
        paciente.idade = data['idade']
    if data.get('local'):
        paciente.local = data['local']
    if data.get('num'):
        paciente.num = data['num']
    if data.get('reclamacao_do_paciente'):
        paciente.reclamacao_do_paciente = data['reclamacao_do_paciente']
    if data.get('rins'):
        paciente.rins = data['rins']
    if data.get('sexo'):
        paciente.sexo = data['sexo']
    if data.get('altura'):
        paciente.altura = data['altura']
    if data.get('peso'):
        paciente.peso = data['peso']

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
    alergias = data["alergias"]
    data_consulta = data["data_consulta"]
    diabetes = data["diabetes"]
    figado = data["figado"]
    gravidez = data["gravidez"]
    hipertencao = data["hipertencao"]
    idade = data["idade"]
    local = data["local"]
    name = data["name"]
    num = data["num"]
    reclamacao_do_paciente = data["reclamacao_do_paciente"]
    rins = data["rins"]
    sexo = data["sexo"]
    altura = data["altura"]
    peso = data["peso"]

    paciente = Paciente.query.filter_by(name=name).first()
    if paciente is None:
        # Create a new paciente
        paciente = Paciente(
            name=name,alergias=alergias,data_consulta=data_consulta,diabetes=diabetes,
            figado=figado,gravidez=gravidez,hipertencao=hipertencao,idade=idade,
            local=local,num=num,reclamacao_do_paciente=reclamacao_do_paciente,rins=rins,
            sexo=sexo,altura=altura,peso=peso)
        db.session.add(paciente)
    db.session.commit()
    return {"message": "Created new Paciente."}


## API IA
@app.route("/recomendacao/", methods=["POST"])
def recomendacao():
    json_data = request.get_json()
    if not json_data:
        return {"message":"No input data provided"}, 400
    try:
        paciente = Paciente.query.filter(Paciente.id == json_data['id']).one()
    except NoResultFound:
        return {"message":"Paciente could not bet found."}, 400

    if json_data.get('reclamacao_do_paciente'):
        paciente.reclamacao_do_paciente = json_data['reclamacao_do_paciente']
        db.session.add(paciente)
        db.session.commit()

    dto = [
        ['PatientId', 'num', 'sexo', 'data_consulta', 'idade', 'local', 'hipertencao', 'diabetes', 'figado', 'rins', 'gravidez', 'alergias', 'reclama????o_do_paciente', 'apos_diagnostico'],
        [str(paciente.id),str(paciente.num),str(paciente.sexo), '23/12/2021',
        str(paciente.idade), paciente.local,str(paciente.hipertencao),
        str(paciente.diabetes),str(paciente.figado),str(paciente.rins),
        str(paciente.gravidez), paciente.alergias,
        paciente.reclamacao_do_paciente, json_data['diagnostico']],
    ]
    print()
    print(dto)
    print("----------------")
    print(paciente.name)
    print("------------------------------------------------------")
    result = gera_lista_branca(dto)
    return dumps(result, indent=4, cls=set_encoder,ensure_ascii=False)



class set_encoder(JSONEncoder):
    def default(self, obj):
        return list(obj)



### MAIN ######################################

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)