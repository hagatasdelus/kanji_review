from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, SubmitField, BooleanField, SelectField
)
from wtforms import ValidationError
from wtforms.validators import DataRequired 
from flask import flash

class RegisterKanjiForm(FlaskForm):
    kanji = StringField('漢字: ', validators=[DataRequired()])
    readings = StringField('読み: ', validators=[DataRequired()])
    hints = SelectField('ヒント: ', choices=[('nothing', 'なし'), ('creature', '生物'), ('persons_name', '人名'), ('plant', '植物'),('Places and Buildings', '地名・建造物')])
    sp_char = BooleanField('文字数特殊?:')
    submit = SubmitField('登録')

    def validate_readings(self, field):
        if len(field.data) > 20:
            raise ValidationError('読みが長すぎます')

