from flask import render_template, redirect, Blueprint, request
from models import Game, User
from app import db
import datetime # will need later for age checks

games_blueprint=Blueprint("games",__name__)

@games_blueprint.route("/games")
def games():
    games=Game.query.all() # sort this alphabetically
    return render_template("index.jinja",games=games)

@games_blueprint.route("/games/<id>")
def show_game(id):
    users=User.query.all()
    game=Game.query.get(id)
    if game.user_id is not None:
        game_user=User.query.get(game.user_id)
    else:
        game_user=None
    return render_template("show_game.jinja",game=game,users=users,game_user=game_user)

@games_blueprint.route("/games/<id>/delete",methods=["POST"])
def delete_game(id):
    game=Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    return redirect("/games")

@games_blueprint.route("/users")
def users():
    users=User.query.all() # sort this alphabetically if we add a user edit function
    return render_template("users.jinja",users=users)

@games_blueprint.route("/games/<id>/check_out",methods=["POST"])
def check_out(id):
    user_id=request.form["user"]
    game=Game.query.get(id)
    game.check_out(user_id)
    db.session.commit()
    return redirect(f"/games/{id}")

@games_blueprint.route("/games/<id>/check_in",methods=["POST"])
def check_in(id):
    game=Game.query.get(id)
    game.check_in()
    db.session.commit()
    return redirect(f"/games/{id}")

@games_blueprint.route("/games/new")
def new_game_form():
    return render_template("new_game.jinja")

@games_blueprint.route("/games",methods=["POST"])
def add_game():
    game=Game(title=request.form["title"],
              genre=request.form["genre"],
              description=request.form["description"],
              age_rating=request.form["age_rating"]
    )
    db.session.add(game)
    db.session.commit()
    return redirect("/games")

# @tasks_blueprint.route("/tasks")
def tasks():
    tasks=Task.query.all()
    return render_template("tasks/index.jinja",tasks=tasks)

# @tasks_blueprint.route("/tasks/<id>")
def show_task(id):
    task=Task.query.get(id)
    return render_template("tasks/show.jinja",task=task)

# @tasks_blueprint.route("/tasks/new")
def task_form():
    users=User.query.all()
    return render_template("tasks/new.jinja",users=users)

# @tasks_blueprint.route("/tasks",methods=["POST"])
def add_task():
    task=Task(description=request.form["description"],
              duration=request.form["duration"],
              completed="completed" in request.form,
              user_id=request.form["user"]
    )
    db.session.add(task)
    db.session.commit()
    return redirect("/tasks")

# @tasks_blueprint.route("/tasks/<id>/edit")
def edit_task(id):
    users=User.query.all()
    task=Task.query.get(id)
    return render_template("tasks/edit.jinja",users=users,task=task)

# @tasks_blueprint.route("/tasks/<id>",methods=["POST"])
def update_task(id):
    task=Task.query.get(id)
    task.description=request.form["description"]
    task.duration=request.form["duration"]
    task.completed="completed" in request.form
    task.user_id=request.form["user"]
    db.session.commit()
    return redirect(f"/tasks/{id}")

# @tasks_blueprint.route("/tasks/<id>/delete",methods=["POST"])
def delete_task(id):
    task=Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/tasks")