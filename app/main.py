from flask import Flask
from flask_restx import Api, Resource, fields
from libraries.myRele import MyRele
import serial
import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Raspi API',
    description='API de comunicação com raspberry, controlando reles, e recebendo informações do arduino nano',
)


ns = api.namespace('reles', description='Lista de reles')

rele = api.model('Rele', {
    'id': fields.Integer(readonly=True, description='identificador'),
    'GPIO': fields.Integer(required=True, description='Numero da porta GPIO do rele'),
    'tag': fields.String(required=True,description='Tag identificação do rele'),
    'descricao': fields.String(required=True, description='Localização e funcionamento do rele'),
    'status': fields.Boolean(required=True, description='true para ligado, false para deslilgado'),
    'date_updated': fields.DateTime(dt_format='rfc822')
})


class ReleDAO(object):
    def __init__(self):
        self.counter = 0
        self.reles = []


    def get(self, id):
        for rele in self.reles:
            if rele['id'] == id:
                return rele
        api.abort(404, "Rele {} não existe".format(id))

    def create(self, data):
        rele = data
        print(rele)
        self.reles.append(rele)
        return rele

    def update(self, id, data):
        rele = self.get(id)
        if rele['status']:
            MyRele(id).off()
            rele['status'] = 0
        else:
            MyRele(id).on()
            rele['status'] = 1
        rele.update(rele)
        return rele

    def delete(self, id):
        rele = self.get(id)
        self.reles.remove(rele)

RDAO = ReleDAO()
RDAO.create({'id':14, 'GPIO': 14, 'tag':'rele-1', 'descricao': 'rele 1', 'status':MyRele(14).check()})
# RDAO.create({'GPIO': 17, 'tag':'rele-2', 'descricao': 'rele 2', 'status':False})
RDAO.create({'id':18, 'GPIO': 18, 'tag':'rele-3', 'descricao': 'rele 3', 'status':MyRele(18).check()})



@ns.route('/')
class ReleList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_reles')
    @ns.marshal_list_with(rele)
    def get(self):
        '''List all tasks'''
        return RDAO.reles

    @ns.doc('create_rele')
    @ns.expect(rele)
    @ns.marshal_with(rele, code=201)
    def post(self):
        '''Create a new task'''
        return RDAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Rele not found')
@ns.param('id', 'Nenhum rele identificado')
class Rele(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_rele')
    @ns.marshal_with(rele)
    def get(self, id):
        '''Fetch a given resource'''
        return RDAO.get(id)

    @ns.doc('delete_rele')
    @ns.response(204, 'Rle deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        RDAO.delete(id)
        return '', 204

    @ns.expect(rele)
    @ns.marshal_with(rele)
    def put(self, id):
        '''Update a task given its identifier'''
        return RDAO.update(id, api.payload)
#
# nsa = api.namespace('temperatura', description='exibe condições meterológicas')
# temperatura = api.model('Temperatura', {
#     'dht22': fields.Integer(readonly=True, description='Sensor de tempratura'),
#     'luminosidade': fields.Integer(required=True, description='Sensor de Luminosidade'),
# })
#
#
# class TemperaturaDAO(object):
#     def __init__(self):
#         self.temperatura = []
#
#
#     def get(self, id):
#         comunicacao = serial.Serial('/dev/ttyUSB0', 9600)
#         try:
#             a = comunicacao.readline()
#             b = json.loads(a.decode("utf-8"))
#             self.temperatura = b
#         except (OSError, serial.SerialException):
#             print(serial.SerialException)
#             pass
#         api.abort(404, "Rele {} não existe".format(id))
#
#
# temp = TemperaturaDAO()
#
# @nsa.route('/')
# class TempList(Resource):
#     '''Shows a list of all todos, and lets you POST to add new tasks'''
#     @nsa.doc('list_temp')
#     @nsa.marshal_list_with(temp)
#     def get(self):
#         '''List all tasks'''
#         return temp.temperatura
#
#


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80,debug=True)
