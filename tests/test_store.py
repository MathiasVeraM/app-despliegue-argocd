import pytest

from app import store


def test_create_list_get_and_update_task():
    created = store.create_task("  Preparar entrega  ", " Revisar el README ")

    assert created == {
        "id": 1,
        "title": "Preparar entrega",
        "description": "Revisar el README",
        "completed": False,
    }
    assert store.list_tasks() == [created]
    assert store.get_task(1) == created

    updated = store.update_task(1, "Entregar", "Subir cambios")
    assert updated == {
        "id": 1,
        "title": "Entregar",
        "description": "Subir cambios",
        "completed": False,
    }


def test_toggle_delete_and_missing_ids():
    task = store.create_task("Probar aplicación")

    assert store.toggle_task(task["id"])["completed"] is True
    assert store.toggle_task(task["id"])["completed"] is False
    assert store.delete_task(task["id"]) is True
    assert store.get_task(task["id"]) is None
    assert store.delete_task(task["id"]) is False
    assert store.update_task(999, "No existe") is None
    assert store.toggle_task(999) is None


@pytest.mark.parametrize("title", ["", "  ", "\t"])
def test_rejects_empty_title(title):
    with pytest.raises(ValueError, match="título no puede estar vacío"):
        store.create_task(title)

    task = store.create_task("Título válido")
    with pytest.raises(ValueError, match="título no puede estar vacío"):
        store.update_task(task["id"], title)
