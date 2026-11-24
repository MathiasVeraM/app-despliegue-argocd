# Gestor de tareas

Mini aplicación CRUD con Flask para practicar despliegues en Kubernetes y GitOps con Argo CD. Las tareas se guardan únicamente en memoria del proceso; por eso se pierden al reiniciar el Pod y no se comparten entre Pods. Gunicorn usa un worker con varios threads para mantener un almacenamiento compartido dentro de cada Pod.

## Ejecutar localmente en Windows (PowerShell)

Desde la raíz del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m app
```

La aplicación queda disponible en `http://localhost:5000`. Si PowerShell bloquea la activación del entorno virtual, para la sesión actual puedes ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Pruebas

Con el entorno virtual activado, desde la raíz:

```powershell
pytest
```

## Docker y Docker Hub

Reemplaza `tu-usuario-dockerhub` por tu nombre de usuario de Docker Hub. La etiqueta de versión explícita para esta entrega es `1.0.0`.

Construir la imagen:

```powershell
$Image = "tu-usuario-dockerhub/tareas-app:1.0.0"
docker build -t $Image .
```

Ejecutarla localmente y comprobar el endpoint de salud:

```powershell
docker run --rm -d --name tareas-app -p 5000:5000 $Image
curl.exe http://localhost:5000/health
```

Al terminar la prueba local, detener el contenedor:

```powershell
docker stop tareas-app
```

Iniciar sesión y subir la imagen:

```powershell
docker login
docker push $Image
```

Verificar la descarga en una máquina limpia (o simularla localmente eliminando primero la imagen local):

```powershell
docker image rm $Image
docker pull $Image
docker run --rm -d --name tareas-app-verificacion -p 5000:5000 $Image
curl.exe http://localhost:5000/health
docker stop tareas-app-verificacion
```

Para borrar la imagen después de probarla:

```powershell
docker image rm $Image
```

## Rutas

- `GET /`: lista de tareas.
- `GET|POST /tasks/new`: formulario para crear una tarea.
- `GET|POST /tasks/<id>/edit`: editar una tarea.
- `POST /tasks/<id>/delete`: eliminar una tarea.
- `POST /tasks/<id>/toggle`: cambiar entre completada y pendiente.
- `GET /health`: respuesta JSON para probes de Kubernetes.
- `GET /carga`: cálculo de CPU de aproximadamente medio segundo para pruebas del HPA.

El pie de página muestra el hostname del proceso que atendió la página.
