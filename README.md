# Memory Game proyecto-g1

Proyecto web construido con Django que implementa un juego tipo "Memory" con registro de usuarios y estadísticas de partidas.

Este README reúne la documentación esencial del proyecto y resume la documentación completa disponible en `DOCUMENTACION_PROYECTO.txt` y `DOCUMENTACION_DETALLADA_LINEA_POR_LINEA.txt`.

## Resumen rápido
- Tecnologías: Python, Django (6.x), SQLite (por defecto), HTML/CSS/JS para frontend.
- Apps principales:
  - `accounts`: registro, inicio de sesión y cierre de sesión.
  - `memory_game`: lógica del juego, guardado de resultados y perfil de usuario.

## Ubicación del proyecto
Carpeta raíz del workspace:

`C:\Users\Laptop-Sistemas\Downloads\casi final\proyectoAR\proyectoAR\proyecto-g1\`

Abrir PowerShell en esa carpeta antes de ejecutar comandos.

## Requisitos previos
- Windows / macOS / Linux con Python 3.x instalado.
- Tener privilegios para crear/activar un entorno virtual.

## Preparación (PowerShell)
1. Abrir PowerShell y navegar a la carpeta del proyecto:

```powershell
cd "C:\Users\Laptop-Sistemas\Downloads\casi final\proyectoAR\proyectoAR\proyecto-g1\"
```

2. Crear el entorno virtual (si no existe):

```powershell
python -m venv env
```

3. Activar el entorno virtual (PowerShell):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\env\Scripts\Activate.ps1
```

4. Actualizar pip (opcional pero recomendado):

```powershell
python -m pip install --upgrade pip
```

5. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

## Inicializar la base de datos
1. Ejecutar migraciones para crear las tablas necesarias:

```powershell
python manage.py migrate
```

2. (Opcional) Crear un superusuario para acceder al panel de administración:

```powershell
python manage.py createsuperuser
```

## Ejecutar la aplicación (desarrollo)
1. Iniciar servidor local:

```powershell
python manage.py runserver
```

2. Abrir navegador y visitar:

- Sitio principal: `http://127.0.0.1:8000/`
- Panel admin: `http://127.0.0.1:8000/admin/`

## Estructura y archivos importantes (resumen)
- `manage.py` — utilidad de línea de comandos de Django (migraciones, runserver, etc.).
- `memory_project/settings.py` — configuración principal (BASE_DIR, SECRET_KEY, DEBUG, DATABASES, INSTALLED_APPS, MIDDLEWARE, STATIC settings).
- `memory_project/urls.py` — rutas globales: `admin/`, `accounts/`, raíz -> `memory_game/`.
- `accounts/`
  - `urls.py` — rutas `login/`, `register/`, `logout/`.
  - `views.py` — `login_view`, `register_view`, `logout_view`.
  - `forms.py` — `RegisterForm` extiende `UserCreationForm` añadiendo `email`.
  - `templates/accounts/` — `login.html`, `register.html` (formularios y estilos).
- `memory_game/`
  - `models.py` — `GameRecord` guarda `user`, `level`, `win`, `duration_seconds`, `created_at`.
  - `views.py` — `select_level`, `play_basic`, `play_medium`, `play_hard`, `save_result`, `profile`.
  - `urls.py` — rutas del juego: `play/..`, `save_result/`, `perfil/`.
  - `templates/memory_game/` — plantillas del juego (game UI, perfil, selección de nivel).
- `db.sqlite3` — base de datos SQLite (contenida en el repositorio; puede eliminarse y recrearse con migraciones).
- `requirements.txt` — lista de dependencias del proyecto.

> Para una explicación completa y línea por línea de archivos clave consulte `DOCUMENTACION_DETALLADA_LINEA_POR_LINEA.txt` en la raíz del proyecto.

## Flujo básico de uso (para un usuario)
1. Registrarse (`/accounts/register/`).
2. Iniciar sesión (`/accounts/login/`).
3. Seleccionar nivel y jugar.
4. Al terminar, el juego envía automáticamente el resultado a la ruta `save_result/` y se guarda en la base de datos.
5. Consultar estadísticas en `perfil/`.

## Seguridad y buenas prácticas
- No publicar `SECRET_KEY`. En entorno real, moverlo a variables de entorno.
- Mantener `DEBUG = False` en producción.
- No versionar bases de datos con datos reales (`db.sqlite3`) ni la carpeta del entorno virtual `env/`.
- Revisar `requirements.txt` y actualizar dependencias antes de desplegar.

## Despliegue
- Archivo `Dockerfile` incluido (revisar y adaptar según entorno de despliegue).
- Se incluye `whitenoise` en `MIDDLEWARE` para servir archivos estáticos en entornos de producción simples.
- Configurar `ALLOWED_HOSTS` con los dominios válidos.

## Errores comunes y solución rápida
- PowerShell bloquea activación del entorno: ejecutar `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force` antes de activar.
- Error al instalar paquetes: asegurarse de que el entorno virtual esté activado y usar `python -m pip install -r requirements.txt`.
- Problemas con la base de datos: eliminar `db.sqlite3` y ejecutar `python manage.py migrate` (pierde datos existentes).

## Recursos adicionales
- `DOCUMENTACION_PROYECTO.txt` — documentación resumida del proyecto.
- `DOCUMENTACION_DETALLADA_LINEA_POR_LINEA.txt` — explicación extendida y didáctica, línea por línea para no programadores.
