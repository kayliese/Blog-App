from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(1500), nullable=False)
    author = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.title} by {self.author}"


@app.route("/")
def index():
    allBlogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template("home.html", path="/", blogList=allBlogs)


@app.route("/new-blog", methods=["GET", "POST"])
def newBlog():
    if request.method == "POST":
        if request.form['title'].strip() == '' or request.form['body'].strip() == '' or request.form['author'].strip() == '':
            return render_template("new-blog.html", path="new-blog", error={"error": True, "message": "Please input valid blog data."})
        blog = Blog(
            title=request.form['title'], body=request.form['body'], author=request.form['author'])
        try:
            db.session.add(blog)
            db.session.commit()
        except:
            return 'There was an error adding this blog'
        return redirect("/")

    return render_template("new-blog.html", path="new-blog")


@app.route("/blog/<int:id>", methods=["GET", "POST"])
def blogById(id):
    if request.method == "POST":
        blog = Blog.query.filter_by(id=id).first()
        try:
            db.session.delete(blog)
            db.session.commit()
        except:
            return 'There was an error deleting this blog'
        return redirect("/")

    blog = Blog.query.filter_by(id=id).first()
    return render_template("blog.html", path="/", blog=blog)


if __name__ == "main":
    app.run(debug=True)
