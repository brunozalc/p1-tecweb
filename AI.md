# avaliação intermediária

## índice

1. [conceitos básicos de web](#conceitos-básicos-de-web)
2. [projeto 1A](#projeto-1a)
3. [projeto 1B](#projeto-1b)

---

## conceitos básicos de web

### métodos HTTP

- **GET**: solicita dados de um recurso.

    ```python
        request = "GET <URI> HTTP/1.1\r\nHost: <HOST>\r\n\r\n"
    ```

- **POST**: envia dados para serem processados por um recurso.

    ```python
        request = "POST <URI> HTTP/1.1\r\nHost: <HOST>\r\nContent-Type: <CONTENT-TYPE>\r\nContent-Length: <LENGTH>\r\n\r\n<DATA>"
    ```

### status codes

- **200 OK**: tudo certo.
- **404 Not Found**: recurso não encontrado.

---

## projeto 1A

### adicionando uma página de erro 404

1. **criar um template HTML**
    - salve um arquivo `404.html` com o conteúdo HTML que você deseja.

    ```html
    <!DOCTYPE html>
    ...

    <div class="appbar">
      <img src="../img/logo-getit.png" class="logo" />
      <span class="subtitle">Como o Post-it, mas com outro verbo</span>
    </div>

    <div class="error-container">
      <h1>404</h1>
      <p>Página não encontrada</p>
      <button class="btn" type="button" onclick="window.location.href='/'">Voltar para a página inicial</button>
    </div>

    ```

2. **criar uma função em `views.py`**
    - implemente uma função que utilize dados (se necessário) e construa a página HTML.

    ```python
    def error_404():
        return build_response(code=404, reason='Not Found') + load_template('404.html').encode()
    ```

3. **atualizar `server.py`**
    - modifique o `server.py` para lidar com a nova rota.

    ```python
    ...

    elif route.startswith('update'):
        response = update(request)
    else:
        response = error_404()   
    ...
    ```

---

## projeto 1B

### criando um mini-projeto do zero, em que o site só armazena uma nota por vez

1. **iniciando um ambiente virtual**
    - crie um ambiente virtual com o comando `python3 -m venv venv`.
    - ative o ambiente virtual com o comando `source venv/bin/activate`.

    ```bash
    python3 -m venv env
    env\Scripts\Activate.ps1
    ```

2. **criando um projeto Django**
    - instale o Django no ambiente virtual com o comando `pip install django`.
    - crie um projeto Django com o comando `django-admin startproject meuProjeto`.

    ```python
    pip install django
    ```

    ```bash
    django-admin startproject meuProjeto .
    ```

3. **criando um app Django**
    - crie um app Django com o comando `python manage.py startapp meuApp`.

    ```bash
    python manage.py startapp meuApp
    ```

4. **configurando o arquivo `settings.py`**
    - abra o arquivo `settings.py` e modifique o `DATABASES` para usar o SQLite.
    - adicione o app criado em `INSTALLED_APPS`.
    - fazer as migrações iniciais.

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
    ```

    ```python
    INSTALLED_APPS = [
        'meuProjeto.meuApp.MeuappConfig',
    ]
    ```

    ```bash
    python manage.py migrate
    ```

5. **criando um modelo**
    - abra o arquivo `models.py` e crie um modelo.
    - faça as migrações.

    ```python
    class Note(models.Model):
        titulo = models.CharField(max_length=200)
        conteudo = models.TextField()

        def __str__(self):
            return self.titulo
    ```

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **criando um superusuário**
    - crie um superusuário com o comando `python manage.py createsuperuser`.
    - modifique o arquivo admin.py.

    ```bash
    python manage.py createsuperuser
    ```

    ```python
    from django.contrib import admin
    from .models import Note

    admin.site.register(Note)
    ```

7. **criando um template**
    - crie os arquivos `base.html` e `index.html` na pasta `templates`.
    - modifique o arquivo `views.py` para renderizar o template com somente a última nota

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Getit</title>
    </head>
    <body>

    <main class="container">
    <form class="form-card" method="post">
        {% csrf_token %}
        <input
        id="titulo"
        class="form-card-title"
        type="text"
        name="titulo"
        placeholder="Título"
        />
        <textarea
        id="detalhes"
        class="autoresize"
        name="detalhes"
        placeholder="Digite o conteúdo..."
        ></textarea>
        <button class="btn" type="submit">Criar</button>
    </form>
        <p>{{ last_note.conteudo }}</p>
    </body>
    </html>
    ```

    ```python
    from django.shortcuts import render
    from django.http import HttpResponse
    from .models import Note

    def index(request):
        if request.method == 'POST':
            titulo = request.POST.get('titulo')
            conteudo = request.POST.get('conteudo')
            Note.objects.create(titulo=titulo, conteudo=conteudo)
            return redirect('index')

        last_note = Note.objects.last()
        return render(request, 'index.html', {'last_note': last_note})
    ```

8. **criando uma rota**
    - modifique o arquivo `urls.py` para criar uma rota para o template.

    ```python
    from django.contrib import admin
    from django.urls import path
    from .views import index

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index, name='index'),
    ]
    ```

9. **executando o servidor**
    - execute o servidor com o comando `python manage.py runserver`.

    ```bash
    python manage.py runserver
    ```
