from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import flask
import re
from application import db
from application.videos.models import Video
from application.videos.forms import VideoForm

bp = Blueprint("videos", __name__)


@bp.route("/videos/new/")
def video_form():
    form = VideoForm()
    return render_template("videos/new.html", form=form)


@bp.route("/videos/", methods=["POST"])
def videos_create():

    if flask.request.method == 'POST':
        form = VideoForm(request.form)
        if form.validate_on_submit():

            url = form.url.data
            pattern = re.compile('(?<=\?v=).*')


            new_video = Video(form.title.data, re.search(pattern,url)[0])
            db.session().add(new_video)
            db.session().commit()
            return redirect(url_for("videos.videos_index"))

@bp.route("/videos/remove/<video_id>", methods=["POST"])
def remove_video(video_id):
    video = Video.query.get(video_id)
    db.session().delete(video)
    db.session().commit()

    return redirect(url_for("videos.videos_index"))


@bp.route("/videos", methods=["GET"])
def videos_index():

    videos = Video.query


    return render_template("videos/list.html", videos=Video.query.all())


@bp.route('/')
def index():
    return render_template("index.html")
