from myapp.forms import (
    AnswerForm,
    DeleteForm,
    RegisterKanjiForm,
    SearchForm,
    SettingForm,
)
from myapp.models import Kanji, transaction
from myapp.utils.answer_formats import make_answer_format

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

bp = Blueprint("app", __name__, url_prefix="")


@bp.route("/")
def home():
    session["score"] = 0
    return render_template("home.html")


@bp.route("/question", methods=["GET", "POST"])
def question():
    form = AnswerForm()
    kanji = Kanji.get_kanji()
    circle = session.get("circle", True)
    if not kanji:
        flash("漢字が見つかりませんでした")
        return redirect(url_for("app.home"))
    if request.method == "POST" and form.validate():
        if form.readings.data == "q":
            session["score"] = 0
            return redirect(url_for("app.question"))
        if form.readings.data == session.get("readings"):
            flash("正解", "success")
            session["score"] = session.get("score", 0) + 1
            if not circle:
                return redirect(url_for("app.question"))
            return redirect(url_for("app.success"))
        else:
            flash("不正解", "danger")
            return redirect(url_for("app.retry"))
    session["kanji_id"] = kanji.id
    session["readings"] = kanji.readings
    time = session.get("time", 8)
    se = session.get("success_sound", False)
    hints_exist = session.get("hints_exist", False)
    gamemode = session.get("review_mode", False)
    score = session.get("score", 0)
    return render_template(
        "kanji_question.html",
        form=form,
        kanji=kanji,
        circle=circle,
        time=time,
        se=se,
        hints_on=hints_exist,
        gamemode=gamemode,
        score=score,
    )


@bp.route("/retry", methods=["GET", "POST"])
def retry():
    form = AnswerForm()
    kanji_id = session.get("kanji_id")
    kanji = Kanji.select_kanji_by_id(kanji_id)
    circle = session.get("circle", True)
    if request.method == "POST" and form.validate():
        if form.readings.data == "q":
            return redirect(url_for("app.question"))
        if form.readings.data == kanji.readings:
            flash("正解", "success")
            session["score"] = session.get("score", 0) + 1
            if not circle:
                return redirect(url_for("app.question"))
            return redirect(url_for("app.success"))
        else:
            flash("不正解", "danger")
            return redirect(url_for("app.retry"))
    time = session.get("time", 8)
    se = session.get("success_sound", False)
    hints_exist = session.get("hints_exist", False)
    gamemode = session.get("review_mode", False)
    score = session.get("score", 0)
    return render_template(
        "kanji_question.html",
        form=form,
        kanji=kanji,
        circle=circle,
        time=time,
        se=se,
        hints_on=hints_exist,
        gamemode=gamemode,
        score=score,
    )


@bp.route("/success", methods=["GET", "POST"])
def success():
    kanji_id = session.get("kanji_id")
    kanji = Kanji.select_kanji_by_id(kanji_id)
    circle = session.get("circle", True)
    time = session.get("time", 8)
    se = session.get("success_sound", False)
    return render_template(
        "kanji_question.html", kanji=kanji, circle=circle, time=time, se=se, suc=True
    )


@bp.route("register_kanji", methods=["GET", "POST"])
def register_kanji():
    form = RegisterKanjiForm(request.form)
    if request.method == "POST" and form.validate():
        kanjis = Kanji(
            kanji=form.kanji.data,
            readings=form.readings.data,
            hints=form.hints.data,
            sp_char=form.sp_char.data,
        )
        from setup import app

        with app.app_context():
            with transaction():
                kanjis.create_new_book()
            flash(f'"{form.kanji.data}"の登録が完了しました。')
        return redirect(url_for("app.register_kanji"))
    session["score"] = 0
    return render_template("kanji_register.html", form=form)


@bp.route("/kanji_delete", methods=["GET", "POST"])
def kanji_delete():
    form = DeleteForm(request.form)
    if request.method == "POST" and form.validate():
        with transaction():
            Kanji.delete_kanji(form.kanji.data)
        flash(f"{form.kanji.data}を削除しました")
        return redirect(url_for("app.register_kanji"))
    session["score"] = 0
    return render_template("kanji_delete.html", form=form)


@bp.route("/search_kanji", methods=["GET"])
def search_kanji():
    form = SearchForm(request.form)
    kanji = request.args.get("kanji", None, type=str)
    kanji_info = Kanji.select_kanji_info_by_kanji(kanji)
    session["score"] = 0
    return render_template("search_kanji.html", form=form, kanji=kanji_info)


@bp.route("/answer_ajax", methods=["GET"])
def answer_ajax():
    kanji_id = request.args.get("kanji_id", -1, type=int)
    failed = request.args.get("failed", -1, type=int)
    if failed == -1:
        return
    if failed == 0:
        session["score"] = 0
    kanji = Kanji.select_kanji_by_id(kanji_id)
    return jsonify(data=make_answer_format(kanji))


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    form = SettingForm(request.form)
    if request.method == "POST" and form.validate():
        flash("設定が更新されました")
        session["circle"] = form.circle.data
        session["time"] = form.next_Q_time.data
        session["success_sound"] = form.success_sound.data
        session["hints_exist"] = form.hints_exist.data
        session["review_mode"] = form.review_mode.data
        return redirect(url_for("app.settings"))
    circle = session.get("circle", True)
    time = session.get("time", 8)
    se = session.get("success_sound", False)
    hints_exist = session.get("hints_exist", False)
    gamemode = session.get("review_mode", False)
    session["score"] = 0
    return render_template(
        "settings.html",
        form=form,
        circle_on=circle,
        time=time,
        se_on=se,
        hints_on=hints_exist,
        gamemode=gamemode,
    )


# @bp.before_request
# def before_request():
#     if request.endpoint not in ['question', 'retry', 'success']:
#         session['score'] = 0


@bp.app_errorhandler(404)
def redirect_main_page(e):
    return redirect(url_for("app.home"))


@bp.app_errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
