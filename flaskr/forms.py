from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, SubmitField, BooleanField, SelectField
)
from wtforms import ValidationError
from wtforms.validators import DataRequired 
from flaskr.models import Kanji

class RegisterKanjiForm(FlaskForm):
    kanji = StringField('漢字: ', validators=[DataRequired()])
    readings = StringField('読み: ', validators=[DataRequired()])
    hints = SelectField(label='ヒント: ', choices=[('nothing', 'なし'), ('生物', '生物'), ('人名', '人名'), ('植物', '植物'),('地名・建造物', '地名・建造物')])
    sp_char = BooleanField('文字数特殊?:')
    submit = SubmitField('登録')

    def validate_kanji(self, field):
        if Kanji.select_kanji_info_by_kanji(field.data):
            raise ValidationError('その漢字はすでに登録されています')
        
    def validate_readings(self, field):
        if len(field.data) > 20:
            raise ValidationError('読みが長すぎます')

class AnswerForm(FlaskForm):
    readings = StringField()
    submit = SubmitField('答える')
