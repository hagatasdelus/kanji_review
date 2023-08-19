from flask import (
    request, render_template, redirect, url_for, Blueprint,
    session, flash
)
from flaskr.forms import (
    RegisterKanjiForm, AnswerForm
)
from flaskr.models import (
    Kanji, transaction
)
from flaskr import db

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
    if form.validate_on_submit():
        if form.readings.data == session.get('readings'):
            flash('正解', 'success')
            return redirect(url_for('app.question'))
        else:
            flash('不正解', 'danger')
            return redirect(url_for('app.retry'))
    session['kanji_id'] = kanji.id
    session['readings'] = kanji.readings
    return render_template('question.html', form=form, kanji=kanji)

@bp.route('/question/retry', methods=['GET', 'POST'])
def retry():
    form = AnswerForm()
    kanji_id = session.get('kanji_id')
    kanji = Kanji.select_kanji_by_id(kanji_id)
    if form.validate_on_submit():
        if form.readings.data == kanji.readings:
            flash('正解', 'success')
            return redirect(url_for('app.question'))
        else:
            flash('不正解', 'danger')
            return redirect(url_for('app.retry'))
    return render_template('question.html', form=form, kanji=kanji)

# @bp.route('/question', methods=['GET', 'POST'])
# def question():
#     kanji = Kanji.get_kanji()
#     form = AnswerForm(request.form)
#     if request.method == 'POST' and form.validate():
#         if kanji.readings == form.readings.data:
#             return redirect(url_for('app.check', kanji_id=kanji.id))
#     # kanji_list = Kanji.query.all() # Kanjiテーブルから全レコードを取得する
#     # if kanji_list:
#     #     flash('リストが見つかりませんでした')
#     #     return redirect(url_for('app.home'))
#     # kanji = random.choice(kanji_list) # ランダムに一つ選ぶ
#     session['kanji_id'] = kanji.id # セッションに選んだ漢字のIDを保存する
#     session['kanji'] = form.readings.data
#     return render_template('kanji_question.html', kanji=kanji, form=form) # index.htmlに漢字とヒントを渡す

# @bp.route('/check/<id>', methods=['GET', 'POST'])
# def check(kanji_id):
#     # kanji_id = session.get('kanji_id') # セッションから漢字のIDを取得する
#     answer = session.get('kanji')
#     if not kanji_id: # セッションがない場合はトップページにリダイレクトする
#         return redirect(url_for('app.question'))
#     kanji = Kanji.select_kanji_by_id(kanji_id) # KanjiテーブルからIDでレコードを検索する
#     if answer == kanji.readings: # 入力された読み方と正解が一致した場合
#         return render_template('correct.html', kanji=kanji) # correct.htmlに漢字と正解を渡す
#     else: # 入力された読み方と正解が一致しなかった場合
#         return render_template('kanji_question.html', kanji=kanji, error='不正解') # index.htmlに漢字とヒントとエラーメッセージを渡す
    
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
            flash('kanji registration has been completed')
        return redirect(url_for('app.register_kanji'))
    return render_template('kanji_register.html', form=form)

@bp.app_errorhandler(404) #ページが間違うとmain
def redirect_main_page(e):
    return redirect(url_for('app.home'))

@bp.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
