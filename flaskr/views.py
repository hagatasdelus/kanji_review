from flask import (
    request, render_template, redirect, url_for, Blueprint,
    session, flash, jsonify
)
from flaskr.forms import (
    RegisterKanjiForm, AnswerForm, DeleteForm, SearchForm,
    SettingForm
)
from flaskr.models import (
    Kanji, transaction
)
from flaskr.utils.answer_formats import make_answer_format

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/question', methods=['GET', 'POST'])
def question():
    form = AnswerForm()
    kanji = Kanji.get_kanji()
    if not kanji:
        flash('漢字が見つかりませんでした')
        return redirect(url_for('app.home'))
    if request.method == 'POST' and form.validate():
        if form.readings.data == session.get('readings'):
            flash('正解', 'success')
            return redirect(url_for('app.success'))
        else:
            flash('不正解', 'danger')
            return redirect(url_for('app.retry'))
    session['kanji_id'] = kanji.id
    session['readings'] = kanji.readings
    return render_template('kanji_question.html', form=form, kanji=kanji)

@bp.route('/retry', methods=['GET', 'POST'])
def retry():
    form = AnswerForm()
    kanji_id = session.get('kanji_id')
    kanji = Kanji.select_kanji_by_id(kanji_id)
    if request.method == 'POST' and form.validate():
        if form.readings.data == kanji.readings:
            flash('正解', 'success')
            return redirect(url_for('app.success'))
        else:
            flash('不正解', 'danger')
            return redirect(url_for('app.retry'))
    return render_template('kanji_question.html', form=form, kanji=kanji)

@bp.route('/success', methods=['GET', 'POST'])
def success():
    kanji_id = session.get('kanji_id')
    kanji = Kanji.select_kanji_by_id(kanji_id)
    return render_template('kanji_question.html', kanji=kanji, suc=True)

@bp.route('register_kanji', methods=['GET', 'POST'])
def register_kanji():
    form = RegisterKanjiForm(request.form)
    if request.method == 'POST' and form.validate():
        kanjis = Kanji(
            kanji = form.kanji.data,
            readings = form.readings.data,
            hints = form.hints.data,
            sp_char=form.sp_char.data
        )
        from setup import app
        with app.app_context():
            with transaction():
                kanjis.create_new_book()
            flash(f'"{form.kanji.data}"の登録が完了しました。')
        return redirect(url_for('app.register_kanji'))
    return render_template('kanji_register.html', form=form)

@bp.route('/kanji_delete', methods=['GET', 'POST'])
def kanji_delete():
    form = DeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        with transaction():
            Kanji.delete_kanji(form.kanji.data)
        flash(f'{form.kanji.data}を削除しました')
        return redirect(url_for('app.register_kanji'))
    return render_template('kanji_delete.html', form=form)

@bp.route('/search_kanji', methods=['GET'])
def search_kanji():
    form = SearchForm(request.form)
    kanji = request.args.get('kanji', None, type=str)
    kanji_info = Kanji.select_kanji_info_by_kanji(kanji)
    return render_template('search_kanji.html', form=form, kanji=kanji_info)

@bp.route('/answer_ajax', methods=['GET'])
def answer_ajax():
    kanji_id = request.args.get('kanji_id', -1, type=int)
    kanji = Kanji.select_kanji_by_id(kanji_id)
    return jsonify(data=make_answer_format(kanji))

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm(request.form)

    return render_template('settings.html', form=form)

@bp.app_errorhandler(404)
def redirect_main_page(e):
    return redirect(url_for('app.home'))
