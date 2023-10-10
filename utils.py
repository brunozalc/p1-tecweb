import json
from urllib.parse import unquote_plus
from database import Database, Note

db = Database('notes')


# extrai o caminho da request
def extract_route(request):
    path = request.split()[1]
    if path == '/':
        return ''
    path = path[1:]
    return path

# lê um arquivo em modo binário


def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# carrega os dados do database


def load_data(filename=None):
    return db.get_all()


# carrega um template da pasta de templates


def load_template(filename):
    with open("templates/" + filename, encoding="utf-8") as f:
        return f.read()

# adiciona um item ao database


def add_to_database(params):
    note = Note(title=params['titulo'], content=params['detalhes'])
    db.add(note)

# extrai o id de uma nota da request


def extract_id_from_url(request):
    parts = request.split(' ')
    url = parts[1]
    note_id = url.split('/')[-1]
    return note_id

# processa uma requisição POST e extrai os parâmetros


def process_post_request(request):
    request = request.replace('\r', '')
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {}
    for chave_valor in corpo.split('&'):
        chave, valor = chave_valor.split('=')
        params[chave] = unquote_plus(valor)
    return params


# constrói uma resposta http com o código, razão e cabeçalhos especificados


def build_response(body='', code=200, reason='OK', headers=''):
    return f"HTTP/1.1 {code} {reason}\n{headers}\n{body}".encode()
