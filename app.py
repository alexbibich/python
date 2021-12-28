from flask import Flask, render_template, url_for, request, redirect
import pymysql
import traceback


app = Flask(__name__)


main_user = False


con = pymysql.connect(host='localhost',
                      user='root',
                      password='mypass',
                      db='website',
                      cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/create', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        try:
            cur = con.cursor()
            cur.execute("INSERT INTO tablitsa(title, intro, text) VALUES (%s, %s, %s)", (title, intro, text))
            con.commit()
            cur.close()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html", main_user=main_user)


@app.route('/posts')
def posts():
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM tablitsa ORDER BY date DESC")
        articles = cur.fetchall()
        cur.close()
        return render_template("posts.html", articles=articles)
    except:
        return "Ошибка"


@app.route('/posts/<int:id>')
def posts_detail(id):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM tablitsa WHERE id={}".format(id))
        article = cur.fetchone()
        cur.close()
        return render_template("posts_detail.html", article=article, main_user=main_user)
    except:
        return "Ошибка"


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    try:
        cur = con.cursor()
        cur.execute(f"DELETE FROM tablitsa WHERE id={id}")
        con.commit()
        cur.close()
        return redirect('/posts')
    except:
        return ("При удалении статьи произошла ошибка.")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        try:
            cur = con.cursor()
            cur.execute("UPDATE tablitsa SET title=%s, intro=%s, text=%s WHERE id=%s", (title, intro, text, id))
            con.commit()
            cur.close()
            return redirect('/posts')
        except:
            return traceback.print_exc()
    else:
        cur = con.cursor()
        cur.execute("SELECT * FROM tablitsa WHERE id={}".format(id))
        article = cur.fetchone()
        cur.close()
        return render_template("post_update.html", article=article)


@app.route('/reg', methods=['POST', 'GET'])
def registration():
	if request.method == "POST":
		login = request.form['login']
		password = request.form['password']
		try:
			cur = con.cursor()
			cur.execute("INSERT INTO users(login, password) VALUES (%s, %s)", (login, password)) 
			con.commit()
			cur.close()
			return redirect('/home')
		except:
			return "Ошибка"
	else:
		return render_template("reg.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
	global main_user
	if request.method == "POST":
		login = request.form['login']
		password = request.form['password']

		try:
			cur = con.cursor()
			cur.execute("SELECT * FROM users;")
			users = cur.fetchall()
			cur.close()
			logins = list()
			passw = list()

			for user in users:
				logins.append(user['login'])
				passw.append(user['password'])
			if login in logins:
				if password in passw:
					main_user = True

			if main_user:
				return redirect('/home')
			else:
				return "Такого пользователя не существует!"	
		except:
			return "Ошибка"
	else:
		return render_template("log.html")


@app.route('/out')
def out():
    global main_user
    main_user = False
    return redirect('/home')


if __name__ == "__main__":
    app.run(debug=True)