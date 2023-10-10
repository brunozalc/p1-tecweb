from database import Database, Note
from utils import load_data, load_template, build_response, add_to_database, extract_id_from_url, process_post_request

database = Database('notes')

def error_404():
    return build_response(code=404, reason='Not Found') + load_template('404.html').encode()

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        params = process_post_request(request)
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
        return error_404()


def update(request):
    if request.startswith('POST'):
        params = process_post_request(request)

        note = database.get_by_id(params['id'])
        note.title = params['titulo']
        note.content = params['detalhes']

        database.update(note)
        return build_response(code=303, reason='See Other', headers='Location: /')
    else:
        return error_404()

def prova(request):
    total_notes = len(load_data())
    return build_response() + load_template('prova.html').format(total_notes=total_notes).encode()