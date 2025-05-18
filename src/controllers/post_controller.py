from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import inspect

from src.app import Post, db

app = Blueprint("post", __name__, url_prefix="/posts")


@app.route("/<int:author_id>", methods=["POST"])
def create_post(author_id):
    data = request.json

    post = Post(title=data["title"], body=data["body"], author_id=author_id)
    db.session.add(post)
    db.session.commit()

    return {"message": "Post created"}, HTTPStatus.CREATED


@app.get("/")
def list_post():
    query = db.select(Post)
    results = db.session.execute(query).scalars()

    return {
        "Post": [
            {
                "id": post.id,
                "title": post.title,
                "body": post.body,
                "author_id": post.author_id,
            }
            for post in results
        ]
    }


@app.get("/<int:post_id>")
def get_post(post_id):
    post = db.get_or_404(Post, post_id)

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "author_id": post.author_id,
    }


@app.patch("/<int:post_id>")
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])

    db.session.commit()

    return {"message": "Post updated"}, HTTPStatus.OK


@app.delete("/<int:post_id>")
def remove_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
