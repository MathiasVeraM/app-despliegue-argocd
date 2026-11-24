import math
import socket
import time

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for

from app import store


main = Blueprint("main", __name__)


@main.app_context_processor
def add_hostname():
    return {"hostname": socket.gethostname()}


@main.get("/")
def index():
    return render_template("index.html", tasks=store.list_tasks())


@main.route("/tasks/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        try:
            store.create_task(title, description)
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "form.html",
                heading="Nueva tarea",
                action=url_for("main.create"),
                title=title,
                description=description,
            )
        flash("Tarea creada correctamente.", "success")
        return redirect(url_for("main.index"))

    return render_template(
        "form.html",
        heading="Nueva tarea",
        action=url_for("main.create"),
        title="",
        description="",
    )


@main.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit(task_id: int):
    task = store.get_task(task_id)
    if task is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        try:
            store.update_task(task_id, title, description)
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "form.html",
                heading="Editar tarea",
                action=url_for("main.edit", task_id=task_id),
                title=title,
                description=description,
            )
        flash("Tarea actualizada correctamente.", "success")
        return redirect(url_for("main.index"))

    return render_template(
        "form.html",
        heading="Editar tarea",
        action=url_for("main.edit", task_id=task_id),
        title=task["title"],
        description=task["description"],
    )


@main.post("/tasks/<int:task_id>/delete")
def delete(task_id: int):
    if not store.delete_task(task_id):
        abort(404)
    flash("Tarea eliminada correctamente.", "success")
    return redirect(url_for("main.index"))


@main.post("/tasks/<int:task_id>/toggle")
def toggle(task_id: int):
    if store.toggle_task(task_id) is None:
        abort(404)
    flash("Estado de la tarea actualizado.", "success")
    return redirect(url_for("main.index"))


@main.get("/health")
def health():
    return jsonify(status="ok")


@main.get("/carga")
def carga():
    started = time.perf_counter()
    result = 0.0
    iterations = 0
    while time.perf_counter() - started < 0.5:
        result += math.sqrt((iterations % 1000) + 1)
        iterations += 1

    return jsonify(
        status="ok",
        elapsed_seconds=round(time.perf_counter() - started, 3),
        iterations=iterations,
        result=round(result, 3),
    )
