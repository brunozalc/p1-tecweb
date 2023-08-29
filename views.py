from database import Database, Note
from utils import load_data, load_template, build_response, add_to_database, extract_id_from_url
from urllib.parse import unquote_plus

database = Database('notes')


def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        add_to_database(params)
        return build_response(code=303, reason='See Other', headers='Location: /')

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(
            id=dados.id, title=dados.title, content=dados.content)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response() + load_template('index.html').format(notes=notes).encode()


def delete(request):
    note_id = extract_id_from_url(request)
    database.delete(note_id)
    return build_response(code=303, reason='See Other', headers='Location: /')


def edit(request):
    note_id = extract_id_from_url(request)
    note = database.get_by_id(note_id)

    if request.startswith('GET'):
        edit_template = load_template('edit.html')
        print("fornecendo o template de edição")
        return build_response() + edit_template.format(id=note.id, title=note.title, content=note.content).encode()
    else:
        return build_response(code=404, reason='Not Found')


def update(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        note = database.get_by_id(params['id'])
        note.title = params['titulo']
        note.content = params['detalhes']

        database.update(note)
        return build_response(code=303, reason='See Other', headers='Location: /')
    else:
        return build_response(code=404, reason='Not Found')
