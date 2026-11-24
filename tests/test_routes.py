def test_index_and_create_task(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Todavía no hay tareas".encode() in response.data

    response = client.post(
        "/tasks/new",
        data={"title": "Estudiar Kubernetes", "description": "Repasar probes"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Estudiar Kubernetes" in response.data
    assert b"Repasar probes" in response.data
    assert b"Tarea creada correctamente" in response.data


def test_rejects_empty_title_and_edits_task(client):
    response = client.post(
        "/tasks/new",
        data={"title": "   ", "description": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "El título no puede estar vacío.".encode() in response.data

    client.post("/tasks/new", data={"title": "Antes"})
    response = client.post(
        "/tasks/1/edit",
        data={"title": "Después", "description": "Actualizada"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Despu\xc3\xa9s" in response.data
    assert b"Actualizada" in response.data


def test_toggle_and_delete_task(client):
    client.post("/tasks/new", data={"title": "Completar informe"})

    response = client.post("/tasks/1/toggle", follow_redirects=True)
    assert response.status_code == 200
    assert b"Completada" in response.data

    response = client.post("/tasks/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Completar informe" not in response.data


def test_health_and_cpu_load_endpoints(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

    response = client.get("/carga")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
