from flask import Flask, render_template, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_  # 追加
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLiteデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 必修科目のテーブル
class RequiredCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(255))
    department = db.Column(db.String(255))
    half_period = db.Column(db.String(255))
    day_of_week = db.Column(db.String(255))
    time_slot = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    is_required = db.Column(db.Boolean)

# 選択必修科目のテーブル
class ElectiveRequiredCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(255))
    department = db.Column(db.String(255))
    half_period = db.Column(db.String(255))
    day_of_week = db.Column(db.String(255))
    time_slot = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    is_required = db.Column(db.Boolean)

# 総合科目のテーブル
class GeneralCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    half_period = db.Column(db.String(255))
    day_of_week = db.Column(db.String(255))
    time_slot = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    is_required = db.Column(db.Boolean)

# アプリケーションコンテキスト内でデータベース初期化と初期データ追加
with app.app_context():
    # データベース初期化
    db.create_all()

    # 初期データが存在しない場合のみ追加
    if RequiredCourse.query.count() == 0:
        initial_required_courses = [
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '美学基礎購読１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '美学基礎購読１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '倫理学特殊講義', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '倫理学特殊講義', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '倫理学特殊講義', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '美学概論', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '古典語・古典学７', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '古典語・古典学７', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '古典語・古典学１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '古典語・古典学１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '卒業論文１', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '倫理学概論', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '美学課題研究３', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '美学課題研究３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '美学課題研究３', 'is_required': True},
            
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '古典語・古典学３', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '古典語・古典学３', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '思想史７', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '思想史７', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '美術演習３', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '美術演習３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '美術演習３', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '数理学１', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '数理学１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '数理学１', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '宗教学概論', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '哲学課題研究７', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '哲学課題研究７', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '哲学課題研究７', 'is_required': True},

            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '宗教学基礎講読１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '宗教学基礎講読１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '哲学演習７', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '哲学演習７', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '哲学演習７', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '哲学課題研究１', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '哲学課題研究１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '哲学課題研究１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '倫理学課題研究５', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '倫理学課題研究５', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '倫理学課題研究５', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '哲学基礎講読１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '哲学基礎講読１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '哲学課題研究５', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '哲学課題研究５', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '哲学課題研究５', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '卒業論文１', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '哲学概論', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '哲学演習３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '哲学演習３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '哲学演習３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '宗教学課題系研究５', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '宗教学課題系研究５', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '宗教学課題系研究５', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '哲学特殊講義１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '哲学特殊講義１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '哲学特殊講義１', 'is_required': True},

            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': 'クリティカル・シンキング１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '美術演習７', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '美術演習７', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '美術演習７', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '哲学課題研究３', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '哲学課題研究３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '哲学課題研究３', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '倫理学課題研究１', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '倫理学課題研究１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '倫理学課題研究１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '哲学特殊講義７', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '哲学特殊講義７', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '哲学特殊講義７', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '宗教特殊講義１', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '宗教特殊講義１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '宗教特殊講義１', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '記号論理１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '記号論理１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '宗教学演習３', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '宗教学演習３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '宗教学演習３', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '美学特殊講義１', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '美学特殊講義１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '美学特殊講義１', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '卒業論文１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '宗教特殊講義３', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '宗教特殊講義３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '宗教特殊講義３', 'is_required': True},

            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '思想史１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '思想史１', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '美学史１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '美学史１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '美学特殊講義７', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '美学特殊講義７', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '美学特殊講義７', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': 'クリティカル・シンキング１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '美学課題研究５', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '美学課題研究５', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '美学課題研究５', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '宗教課題研究３', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '宗教課題研究３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '宗教課題研究３', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '宗教史３', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '宗教史３', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '倫理学演習３', 'is_required': True},
            {'grade': '3', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '倫理学演習３', 'is_required': True},
            {'grade': '4', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '倫理学演習３', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '哲学概論', 'is_required': True},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '倫理学基礎講読１', 'is_required': True},
            {'grade': '2', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '倫理学基礎講読１', 'is_required': True},

            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '西洋史概説', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '日本史特講３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '日本史特講３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '日本史特講３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '日本史特講１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '日本史特講１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '日本史特講１', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '東洋史概説', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '日本考古学概説１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '日本史基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '東洋史基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '東洋史基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '考古学基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '西洋史研究実習１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '西洋史研究実習１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '西洋史研究実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '歴史民俗学１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '歴史民俗学１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '歴史民俗学１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '東洋史研究実習１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '東洋史研究実習１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '東洋史研究実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '考古学研究実習１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '考古学研究実習１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '考古学研究実習１', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '西洋史概説', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '外国考古学概説１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '東洋史特講１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '東洋史特講１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '東洋史特講１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '考古学基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '日本史料研究１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '日本史料研究１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '日本史料研究１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '東洋史ゼミナール１／東洋史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '東洋史ゼミナール１／東洋史ゼミナール３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール１／西洋史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール１／西洋史ゼミナール３', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '西洋史研究法入門', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '日本史概説', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '西洋史特講３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '西洋史特講３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '西洋史特講３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '東洋史料文研研究１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '東洋史料文研研究１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '東洋史料文研研究１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '考古学ゼミナール１／考古学ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '考古学ゼミナール１／考古学ゼミナール３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '西洋史研究実習１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '西洋史研究実習１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '西洋史研究実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '西洋史基礎実習１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール１／西洋史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール１／西洋史ゼミナール３', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '東洋史概説', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '日本史ゼミナール１／日本史ゼミナール３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '西洋史ゼミナール１／西洋史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '西洋史ゼミナール１／西洋史ゼミナール３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '日本史基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '東洋史基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '東洋史特講３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '東洋史特講３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '東洋史特講３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '日本史基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '考古学方法論１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '考古学方法論１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '考古学方法論１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '東洋史ゼミナール１／東洋史ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '東洋史ゼミナール１／東洋史ゼミナール３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '文化財学１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '文化財学１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '文化財学１', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '史学概論', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学特講３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学特講３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学特講３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学方法論３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学方法論３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学方法論３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '文化財ゼミナール１／文化財ゼミナール３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '文化財ゼミナール１／文化財ゼミナール３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '日本史特講１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '日本史特講１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '日本史特講１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '考古学特講１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '考古学特講１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '考古学特講１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史料文献研究１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史料文献研究１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史料文献研究１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '日本史研究実習１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '日本史研究実習１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '日本史研究実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '日本史料研究３', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '日本史料研究３', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '日本史料研究３', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '西洋史基礎実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '古文書・古記録学１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '古文書・古記録学１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '古文書・古記録学１', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '日本史概説', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '日本史研究実習１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '日本史研究実習１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '日本史研究実習１', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '前期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '考古学実地研究１', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '前期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '考古学実地研究１', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '前期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '考古学実地研究１', 'is_required': True},

            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '日本史研究法入門', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '東洋史研究法入門', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '日本考古学概説２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '日本史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '東洋史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '東洋史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '考古学基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '歴史民俗学２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '歴史民俗学２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '歴史民俗学２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '日本史料研究２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '日本史料研究２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '日本史料研究２', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '東洋史講究', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '外国考古学概説２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '東洋史特講４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '東洋史特講４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '東洋史特講４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '考古学基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '考古学研究実習２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '考古学研究実習２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '考古学研究実習２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '東洋史ゼミナール２／東洋史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '東洋史ゼミナール２／東洋史ゼミナール４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール２／西洋史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール２／西洋史ゼミナール４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '西洋史特講４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '西洋史特講４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '西洋史特講４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '東洋史料文研研究２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '東洋史料文研研究２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '東洋史料文研研究２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '考古学ゼミナール２／考古学ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '考古学ゼミナール２／考古学ゼミナール４', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '考古学研究法入門', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '東洋史特講４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '東洋史特講４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '東洋史特講４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '西洋史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '日本史料研究４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '日本史料研究４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '日本史料研究４', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '西洋史講究', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '東洋史講究', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '西洋史講究', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '日本史ゼミナール２／日本史ゼミナール４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '日本史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '東洋史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '日本史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '考古学方法論２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '考古学方法論２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '考古学方法論２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '東洋史ゼミナール２／東洋史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '東洋史ゼミナール２／東洋史ゼミナール４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '文化財学２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '文化財学２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '文化財学２', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '学問の扉', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学特講４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学特講４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学特講４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学方法論４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学方法論４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '考古学方法論４', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '文化財ゼミナール２／文化財ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '文化財ゼミナール２／文化財ゼミナール４', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '日本史講究', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '考古学特講２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '考古学特講２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '考古学特講２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '東洋史研究実習２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '東洋史研究実習２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '東洋史研究実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史料文献研究２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史料文献研究２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史料文献研究２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール２／西洋史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '西洋史ゼミナール２／西洋史ゼミナール４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '東洋史特講２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '東洋史特講２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '東洋史特講２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '日本史研究実習２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '日本史研究実習２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '日本史研究実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史研究実習２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史研究実習２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史研究実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史特講２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史特講２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史特講２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史ゼミナール２／西洋史ゼミナール４', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '西洋史ゼミナール２／西洋史ゼミナール４', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '日本史特講２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '日本史特講２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '日本史特講２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '西洋史研究実習２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '西洋史研究実習２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '西洋史研究実習２', 'is_required': True},
            {'grade': '1', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '日本史講究', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '西洋史基礎実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '古文書・古記録学２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '古文書・古記録学２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '古文書・古記録学２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '土曜', 'time_slot': '1', 'course_name': '日本史研究実習２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '土曜', 'time_slot': '1', 'course_name': '日本史研究実習２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '土曜', 'time_slot': '1', 'course_name': '日本史研究実習２', 'is_required': True},
            {'grade': '2', 'department': '史学科', 'half_period': '後期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '考古学実地研究２', 'is_required': True},
            {'grade': '3', 'department': '史学科', 'half_period': '後期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '考古学実地研究２', 'is_required': True},
            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '考古学実地研究２', 'is_required': True},

            {'grade': '4', 'department': '史学科', 'half_period': '後期', 'day_of_week': '集中', 'time_slot': '1', 'course_name': '卒業論文', 'is_required': True},
        ]

        for course_data in initial_required_courses:
            course = RequiredCourse(**course_data)
            db.session.add(course)

    if ElectiveRequiredCourse.query.count() == 0:
        initial_elective_required_courses = [
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '選択必修1', 'is_required': False},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '選択必修1', 'is_required': False},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '選択必修2', 'is_required': False},
            # 他の初期データも同様に追加
        ]

        for course_data in initial_elective_required_courses:
            course = ElectiveRequiredCourse(**course_data)
            db.session.add(course)

    if GeneralCourse.query.count() == 0:
        initial_general_courses = [
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '地球環境の変動と生命史', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '地球科学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': 'アカデミック・ライディング', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '美学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '法学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '映像文化論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '少子化・高齢化社会を生きる', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '国際情勢', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '宗教学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '政治学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '人類の進化', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '民俗学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '憲法', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '人類の進化', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '1', 'course_name': '地理学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '歴史学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '生命科学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '科学史', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'アジアの歴史・社会・文化', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'キャリアデザイン', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'History of Japan１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'Japanese Society１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'アカデミック・ライティング１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '考古学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '日本の歴史・社会・文化', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': 'Japanese Culture１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '「生きる」事の哲学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '言語学から見た世界', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '社会学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '映像文化論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '1', 'course_name': '心理学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '1', 'course_name': '異文化コミュニケーション論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '1', 'course_name': '美術史', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '1', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '身体科学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': 'キャリア・ストレスマネジメント', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': 'キャリアデザイン', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': 'Japanese Literature１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '国際日本学入門１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '論理学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '経済発展と人口変動', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': 'ジェンダー論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '社会学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '異文化コミュニケーション論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '国際法', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': 'ゲノム改変と私たちの生活', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '倫理学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '身体の健康', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '教育学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': 'メディア論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '日本語教育学入門', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '欧米の歴史・社会・文化', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '国際経済論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': 'スポーツ文化論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '宇宙を理解する', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': 'Japan in the World１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '美術史', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '音楽文化論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '労働と労働者の権利', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '民俗学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '憲法', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '総合研究１～８', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '1', 'course_name': '化学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '経済学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '物理学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': 'メディア論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': 'Enviro Geo of Japan１', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '文学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '日常生活の中の経済学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': 'ジェンダー論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '政治学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '数学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '哲学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '憲法', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '現代思想論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': 'ジェンダー論', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '現代社会を支える科学技術', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '心の健康', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '土曜', 'time_slot': '3', 'course_name': '心理学', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '土曜', 'time_slot': '3', 'course_name': '現代ビジネスと企業の社会的責任', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '集中', 'time_slot': '1', 'course_name': '総合研究１～８（北海道中川町における...）', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '集中', 'time_slot': '1', 'course_name': '総合研究１～８（北海道から学ぶ...）', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '情報と社会', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '欧米の歴史・社会・文化', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': 'アカデミック・ライティング（日本語）２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '教材・教具論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '法学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '映像文化論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '国際情勢', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '3', 'course_name': '総合研究１～８（コミュニケーションのための情報デザイン）', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '宗教学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '戦後日本の政治', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '4', 'course_name': '総合研究１～８（Chinese and Japanese~）', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '憲法', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '月曜', 'time_slot': '5', 'course_name': '国際情勢', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '生命科学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '欧米の歴史・社会・文化', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '心の健康', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'キャリアデザイン', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'History of Japan２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'Enviro Geo of Japan２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': 'アカデミック・ライティング（英語）２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': '情報と数理', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '3', 'course_name': 'Japanese Culture２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': '「生きる」事の哲学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '4', 'course_name': 'アジアの歴史・社会・文化', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '日本の歴史・社会・文化', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '火曜', 'time_slot': '5', 'course_name': '環境と生命のつながり', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '1', 'course_name': '総合研究１～８（文理学部生による地域連携活動の発展可能性）', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '美学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '身体科学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '多文化共生社会を生きる', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': 'キャリア・ストレスマネジメント', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': 'Japanese Literature２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '2', 'course_name': '日本語教育のための文法', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '身体表現論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '国民国家とグローバル資本主義', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '経済発展と人口変動', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '日本の自然と災害', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '総合研究１～８（カンボジア研究（SDGs達成への貢献））', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '歴史学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '心理学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '物理学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '演劇論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '国際法', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '情報とコミュニケーション', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '4', 'course_name': '総合研究１～８（文理的思考のすすめ～知の探究ゼミ～）', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '倫理学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': 'デジタル産業革命と社会の変容', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '身体の健康', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': '現代社会を支える化学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '水曜', 'time_slot': '5', 'course_name': 'Japanese Society２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': 'Japanese 教育学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '1', 'course_name': '国際日本入門２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '文学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': '国際経済論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': 'スポーツ文化論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': 'データと対話するための統計学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '2', 'course_name': 'Japan in the World２', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '心理学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '宇宙科学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '美術史', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '3', 'course_name': '数学を楽しむ', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '民俗学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '憲法', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': 'イスラム圏の歴史・社会・文化', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '演劇論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '市民社会と法', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '身のまわりの生命現象', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '総合研究１～８（文理的思考のすすめ～知のスクランブル～）', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '木曜', 'time_slot': '5', 'course_name': '総合研究１～８（英語で学ぶ文理融合，知のフロンティア２）', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '1', 'course_name': '社会福祉学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '経済学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '公と私の社会科学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '2', 'course_name': '原子の世界', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '情報科学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '欧米の歴史・社会・文化', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': '映像文化論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '3', 'course_name': 'ジェンダー論', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '4', 'course_name': '戦後日本の政治', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '哲学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '言語学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '憲法', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '金曜', 'time_slot': '5', 'course_name': '統計学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '土曜', 'time_slot': '2', 'course_name': '地球科学', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '集中', 'time_slot': '1', 'course_name': 'キャリアデザイン', 'is_required': False},
            {'half_period': '後期', 'day_of_week': '集中', 'time_slot': '1', 'course_name': 'インターンシップ', 'is_required': False},
        
        ]

        for course_data in initial_general_courses:
            course = GeneralCourse(**course_data)
            db.session.add(course)

    db.session.commit()

# 例: HTML ファイルの指定
@app.route('/')
def index():
    return render_template('index.html')

# クライアントからの授業情報取得リクエストを処理
@app.route('/get_courses', methods=['POST'])
def get_courses():
    grade = request.form.get('grade')
    department = request.form.get('department')
    half_period = request.form.get('halfPeriod')
    print(f"Received request with grade={grade}, department={department}, half_period={half_period}")

    # データベースから該当する授業情報を取得
    courses1 = RequiredCourse.query.filter_by(grade=grade, department=department, half_period=half_period).all()
    courses2 = ElectiveRequiredCourse.query.filter_by(grade=grade, department=department, half_period=half_period).all()
    courses3 = GeneralCourse.query.filter_by(half_period=half_period).all()

    # 結果をリストに変換
    courses_list = [
        {'day_of_week': course.day_of_week, 'time_slot': course.time_slot, 'course_name': course.course_name, 'is_required': course.is_required}
        for course in courses1 + courses2 + courses3
    ]

    return jsonify({'courses': courses_list})  # レスポンスの構造を修正


# 新しい授業を追加するエンドポイント
@app.route('/add_new_course', methods=['POST'])
def add_new_course():
    data = request.json
    if data.get('course_type') == 'required':
        new_course = RequiredCourse(
            grade=data['grade'],
            department=data['department'],
	        half_period=data['halfPeriod'],
            day_of_week=data['dayOfWeek'],
            time_slot=data['timeSlot'],
            course_name=data['courseName'],
            is_required=True
        )
    elif data.get('course_type') == 'elective_required':
        new_course = ElectiveRequiredCourse(
            grade=data['grade'],
            department=data['department'],
            half_period=data['halfPeriod'],
            day_of_week=data['dayOfWeek'],
            time_slot=data['timeSlot'],
            course_name=data['courseName'],
            is_required=False
        )
    elif data.get('course_type') == 'general':
        new_course = GeneralCourse(
            half_period=data['halfPeriod'],
            day_of_week=data['dayOfWeek'],
            time_slot=data['timeSlot'],
            course_name=data['courseName'],
            is_required=False
        )
    else:
        return jsonify({'error': 'Invalid course type'}), 400

    # データベースに追加
    db.session.add(new_course)
    db.session.commit()

    return jsonify({'message': 'Course added successfully'}), 200


from sqlalchemy.exc import IntegrityError

@app.route('/delete_course', methods=['POST'])
def delete_course():
    data = request.json
    course_name_to_delete = data.get('courseName')
    course_type = data.get('courseType')
    grade = data.get('grade')
    department = data.get('department')
    half_period = data.get('halfPeriod')
    day_of_week = data.get('dayOfWeek')
    time_slot = data.get('timeSlot')

    if course_name_to_delete and course_type:
        # データベースから講義を削除
        try:
            if course_type == 'required':
                course = RequiredCourse.query.filter_by(
                    course_name=course_name_to_delete,
                    grade=grade,
                    department=department,
                    half_period=half_period,
                    day_of_week=day_of_week,
                    time_slot=time_slot
                ).first()
            elif course_type == 'elective_required':
                course = ElectiveRequiredCourse.query.filter_by(
                    course_name=course_name_to_delete,
                    grade=grade,
                    department=department,
                    half_period=half_period,
                    day_of_week=day_of_week,
                    time_slot=time_slot
                ).first()
            elif course_type == 'general':
                course = GeneralCourse.query.filter_by(
                    course_name=course_name_to_delete,
                    half_period=half_period,
                    day_of_week=day_of_week,
                    time_slot=time_slot
                ).first()
            else:
                return jsonify({'error': 'Invalid course type'}), 400

            if course:
                db.session.delete(course)
                db.session.commit()
                return jsonify({'message': 'Course deleted successfully'}), 200
            else:
                return jsonify({'error': 'Course not found'}), 404

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': 'IntegrityError - The course is associated with other records'}), 500

    else:
        return jsonify({'error': 'Invalid request'}), 400



# @app.route('/search_courses', methods=['GET'])
# def search_courses():
#     search_term = request.args.get('search_term', '')

#     # 検索クエリが空の場合は空の結果を返す
#     if not search_term:
#         return jsonify({'results': []})

#     # データベースクエリを実行して検索結果を取得
#     results = RequiredCourse.query.filter(or_(RequiredCourse.course_name.ilike(f'%{search_term}%'))).all()

#     # 結果をJSON形式で返す
#     return jsonify({'results': [course.course_name for course in results]})
    
@app.route('/search_courses', methods=['GET'])
def search_courses():
    search_term = request.args.get('search_term', '')
    table_type = request.args.get('table_type', '')  # 新たに追加

    # 検索クエリが空の場合は空の結果を返す
    if not search_term:
        return jsonify({'results': []})

    # テーブルタイプに応じてクエリを実行して検索結果を取得
    if table_type == 'required':
        results = RequiredCourse.query.filter(RequiredCourse.course_name.ilike(f'%{search_term}%')).all()
        formatted_results = [{'course_name': course.course_name, 'grade': course.grade, 'department': course.department, 'day_of_week': course.day_of_week, 'time_slot': course.time_slot, 'half_period': course.half_period} for course in results]
    elif table_type == 'elective_required':
        results = ElectiveRequiredCourse.query.filter(ElectiveRequiredCourse.course_name.ilike(f'%{search_term}%')).all()
        formatted_results = [{'course_name': course.course_name, 'grade': course.grade, 'department': course.department, 'day_of_week': course.day_of_week, 'time_slot': course.time_slot, 'half_period': course.half_period} for course in results]
    elif table_type == 'general':
        results = GeneralCourse.query.filter(GeneralCourse.course_name.ilike(f'%{search_term}%')).all()
        formatted_results = [{'course_name': course.course_name, 'day_of_week': course.day_of_week, 'time_slot': course.time_slot, 'half_period': course.half_period} for course in results]
    else:
        return jsonify({'error': 'Invalid table type'}), 400

    # 結果をJSON形式で返す（各コースの詳細情報も含む）
    # formatted_results = [{'course_name': course.course_name, 'grade': course.grade, 'department': course.department, 'day_of_week': course.day_of_week, 'time_slot': course.time_slot, 'half_period': course.half_period} for course in results]

    return jsonify({'results': formatted_results})



if __name__ == '__main__':
    app.run(debug=True)
