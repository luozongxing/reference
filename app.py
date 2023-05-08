import pandas as pd
from flask import Flask, render_template, send_file, request, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileRequired, FileField, FileAllowed
from sqlalchemy import text
from flask_wtf import FlaskForm
import wtforms
from wtforms import SubmitField
from wtforms.validators import Email, Length, EqualTo, InputRequired, DataRequired
from flask_migrate import Migrate
app = Flask(__name__)

# mysql所在的主机名
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "database_learn"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
app.config['SECRET_KEY'] = 'replace_with_your_secret_key'
import os
app.config['SECRET_KEY'] = os.urandom(24)
# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中的数据库的信息

db = SQLAlchemy(app)
migrate = Migrate(app,db)

#ORM模型映射成表的三步
#1.flask db init：这步只需要执行一次
#2. flask db migrate: 识别ORM模型的改变，生成迁移脚本
#3.flask db upgrade:运行迁移脚本，同步到数据库中






# with app.app_context():
#     with db.engine.connect()as conn:
#         query = text("SELECT 1")
#         rs = conn.execute(query)
#         print(rs.fetchone())


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    singnature = db.Column(db.String(100))



# user = User(username="刘伟", password='666')

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # backref:会自动的给User模型添加一个articles的属性，用来获取文章列表
    author = db.relationship("User", backref="articles")


article = Article(title="Flask学习大纲", content="Flaskxxxxx")
# article.author_id = user.id
# user = User.query.get(article.author_id)
# article.author_id = User.query.get(article.author_id)
# print(article.author)

# with app.app_context():
#     db.create_all()


class Download(FlaskForm):

    submit = SubmitField(label='下载')


class UploadForm(FlaskForm):


    file = FileField('File', validators=[DataRequired(), FileAllowed(['xls', 'xlsx'], message='只能上传xls和xlsx格式的文件，其他文件不支持')])
    submit = SubmitField('上传')






@app.route("/uploadfile",methods=['POST','GET'])
def uploadfile():
    form = UploadForm()
    download_form = Download()
    if form.validate_on_submit():
        file = form.file.data
        file_content = file.read()
        file_type = file.content_type
        if file_type in (
        'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
            # pandas读取文件内容并且将文件内容读取转换为字典
            df = pd.read_excel(file_content)
            data = df.to_dict('records')
            #遍历读取后的数据
            for user_data in data:
                username = user_data['username']
                password = user_data['password']
                email = user_data['email']
                singnature = user_data['singnature']
                # 查询数据库 本次上传数据和数据库内的数据是否有重复
                existing_user = User.query.filter(User.username == username or User.email == email).first()
                if existing_user is None:
                    user = User(username=username,password=password,email=email,singnature=singnature)
                    db.session.add(user)
                else:
                    print('有重复')
                    flash("文件内数据与数据库数据有重复","error")

                db.session.commit()
            return 'File uploaded and parsed successfully!'

        else:
            # 上传的文件不是 Excel 文件
            flash("只允许上传 Excel 文件", "error")

    return render_template('upload.html', form=form, download_form=download_form)



@app.route("/downloadfile",methods=['POST','GET'])
def downloadfile():
    filename = r'D:\flask学习\demo04\upload\user.xls'
    return send_file(filename, as_attachment=True)





@app.route("/user/add")
def add_user():
    user = User(username="刘伟", password='666')
    db.session.add(user)
    db.session.commit()
    return "用户创建成功"


@app.route('/user/query')
def query_user():
    # user = User.query.get(1)
    # print(f"{user.id}:{user.username}--{user.password}")
    user = User.query.filter_by(username="刘伟")
    for i in user:
        print(i.username)

    return "数据查询成功"


@app.route('/user/update')
def update_user():
    users = User.query.filter_by(username="刘伟").first()
    users.password = '3333'
    db.session.commit()
    return '数据修改成功'


@app.route('/user/delete')
def delete_user():
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "数据删除成功"


@app.route("/article/add")
def article_add():
    article1 = Article(title="FLASK学习", content="Flaskxxxxxxxxxx")
    article1.author = User.query.get(2)

    article2 = Article(title="Django", content="Django学习吸吸吸")
    article2.author = User.query.get(2)

    db.session.add_all([article1,article2])

    db.session.commit()

    return "文章添加成功"

@app.route("/article/query")
def query_article():
    user =User.query.get(2)
    for article in user.articles:
        print(article.title)
    return "文章查找成功"

if __name__ == '__main__':
    app.run(debug=True)
