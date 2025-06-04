from app import app
from flask import render_template, request, redirect, url_for
from app.models.user import User

@app.route("/usuarios")
def listar_usuarios():
    usuarios = User.query.all()
    return render_template("usuarios_list.html", usuarios=usuarios)

@app.route("/usuarios/add", methods=["GET", "POST"])
def add_usuario():
    if request.method == "POST":
        username = request.form.get("username")
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        if username and nome and senha:
            user = User(username=username, nome=nome)
            user.set_password(senha)
            user.save()
            return redirect(url_for("listar_usuarios"))
        error = "Preencha todos os campos."
        return render_template("usuario_add.html", error=error)
    return render_template("usuario_add.html")

@app.route("/usuarios/<int:user_id>/edit", methods=["GET", "POST"])
def edit_usuario(user_id):
    user = User.query.get(user_id)
    if not user:
        return "Usuário não encontrado", 404
    if request.method == "POST":
        user.username = request.form.get("username")
        user.nome = request.form.get("nome")
        senha = request.form.get("senha")
        if senha:
            user.set_password(senha)
        user.save()
        return redirect(url_for("listar_usuarios"))
    return render_template("usuario_edit.html", user=user)

@app.route("/usuarios/<int:user_id>/delete", methods=["POST"])
def delete_usuario(user_id):
    user = User.query.get(user_id)
    if not user:
        return "Usuário não encontrado", 404
    user.delete()
    return redirect(url_for("listar_usuarios"))