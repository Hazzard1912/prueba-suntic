# Sistema de Gestión de Documentos PDF en Django

Este es un sistema de gestión de documentos PDF basado en Django que permite a los usuarios cargar, editar, eliminar y listar documentos PDF. A cada documento se le puede asignar un aprobador, y el aprobador puede aprobar o rechazar el documento. Los usuarios solo pueden editar o eliminar sus propios documentos, y los aprobadores solo pueden aprobar o rechazar los documentos asignados a ellos. Los usuarios pueden agregar el control de seguridad de doble factor de autenticación en el apartado de **Seguridad**.

## Características

- Subir, editar, eliminar y listar documentos PDF.
- Asignar un aprobador a cada documento.
- Los aprobadores pueden aprobar o rechazar documentos.
- Los usuarios solo pueden editar o eliminar sus propios documentos.
- Los aprobadores solo pueden aprobar o rechazar documentos asignados a ellos.
- Previsualizar documentos PDF en el navegador.
- Agregar 2FA para iniciar sesión de manera segura a traves de Google Authenticator u otro servicio.

## Requisitos

- Python 3.x
- Django 3.x o superior
- Virtualenv

## Empezando

### Clona el Repositorio

```sh
git clone https://github.com/Hazzard1912/prueba-suntic.git 
cd prueba-suntic
```

### Configura el Entorno Virtual

```sh
python -m venv env
source env/bin/activate  # En Windows usa 'env\Scripts\activate'
```

### Instala las Dependencias

```sh
pip install -r requirements.txt
```

### Aplica las Migraciones

```sh
python manage.py migrate
```

### Crea un Superusuario

```sh
python manage.py createsuperuser
```

### Crea los Aprobadores de Prueba

```sh
python manage.py create_approvers
```

### Inicia el Servidor de Desarrollo

```sh
python manage.py runserver
```