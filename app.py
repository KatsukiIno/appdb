from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class RequiredCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(255))
    department = db.Column(db.String(255))
    half_period = db.Column(db.String(255))
    day_of_week = db.Column(db.String(255))
    time_slot = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    is_required = db.Column(db.Boolean)

class ElectiveRequiredCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(255))
    department = db.Column(db.String(255))
    half_period = db.Column(db.String(255))
    day_of_week = db.Column(db.String(255))
    time_slot = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    is_required = db.Column(db.Boolean)

class GeneralCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    half_period = db.Column(db.String(255))
    day_of_week = db.Column(db.String(255))
    time_slot = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    is_required = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

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
        ]

        for course_data in initial_required_courses:
            course = RequiredCourse(**course_data)
            db.session.add(course)

    if ElectiveRequiredCourse.query.count() == 0:
        initial_elective_required_courses = [
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '1', 'course_name': '選択必修1', 'is_required': False},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '月曜', 'time_slot': '2', 'course_name': '選択必修1', 'is_required': False},
            {'grade': '1', 'department': '哲学科', 'half_period': '前期', 'day_of_week': '火曜', 'time_slot': '2', 'course_name': '選択必修2', 'is_required': False},
        ]

        for course_data in initial_elective_required_courses:
            course = ElectiveRequiredCourse(**course_data)
            db.session.add(course)

    if GeneralCourse.query.count() == 0:
        initial_general_courses = [
            {'half_period': '前期', 'day_of_week': '水曜', 'time_slot': '3', 'course_name': '総合科目1', 'is_required': False},
            {'half_period': '前期', 'day_of_week': '木曜', 'time_slot': '4', 'course_name': '総合科目2', 'is_required': False},
        ]

        for course_data in initial_general_courses:
            course = GeneralCourse(**course_data)
            db.session.add(course)

    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_courses', methods=['POST'])
def get_courses():
    grade = request.form.get('grade')
    department = request.form.get('department')
    half_period = request.form.get('halfPeriod')
    print(f"Received request with grade={grade}, department={department}, half_period={half_period}")

    courses1 = RequiredCourse.query.filter_by(grade=grade, department=department, half_period=half_period).all()
    courses2 = ElectiveRequiredCourse.query.filter_by(grade=grade, department=department, half_period=half_period).all()
    courses3 = GeneralCourse.query.filter_by(half_period=half_period).all()

    courses_list = [
        {'day_of_week': course.day_of_week, 'time_slot': course.time_slot, 'course_name': course.course_name, 'is_required': course.is_required}
        for course in courses1 + courses2 + courses3
    ]

    return jsonify({'courses': courses_list}) 


if __name__ == '__main__':
    app.run(debug=True)
