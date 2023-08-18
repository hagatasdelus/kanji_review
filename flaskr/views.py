from flask import (
    request, render_template, redirect, url_for, Blueprint,
    session, flash
)
from flaskr.forms import (
    RegisterKanjiForm
)
from flaskr.models import (
    Kanji, transaction
)
from flaskr import db
import random

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/question')
def question():
    kanji_list = Kanji.query.all() # Kanjiテーブルから全レコードを取得する
    # if kanji_list:
    #     flash('リストが見つかりませんでした')
    #     return redirect(url_for('app.home'))
    kanji = random.choice(kanji_list) # ランダムに一つ選ぶ
    session['kanji_id'] = kanji.id # セッションに選んだ漢字のIDを保存する
    return render_template('kanji_question.html', kanji=kanji) # index.htmlに漢字とヒントを渡す

@bp.route('/check', methods=['POST'])
def check():
    answer = request.form['answer'] # フォームから入力された読み方を取得する
    kanji_id = session.get('kanji_id') # セッションから漢字のIDを取得する
    if kanji_id is None: # セッションがない場合はトップページにリダイレクトする
        return redirect(url_for('app.home'))
    kanji = Kanji.query.get(kanji_id) # KanjiテーブルからIDでレコードを検索する
    if answer == kanji.readings: # 入力された読み方と正解が一致した場合
        return render_template('correct.html', kanji=kanji) # correct.htmlに漢字と正解を渡す
    else: # 入力された読み方と正解が一致しなかった場合
        return render_template('kanji_question.html', kanji=kanji, error='不正解') # index.htmlに漢字とヒントとエラーメッセージを渡す
    
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
        return redirect(url_for('app.home'))
    return render_template('kanji_register.html', form=form)

@bp.app_errorhandler(404) #ページが間違うとmain
def redirect_main_page(e):
    return redirect(url_for('app.home'))

@bp.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
