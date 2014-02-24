from flask import Flask, render_template, request, redirect, url_for
import MySQLdb, utils

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    db = utils.db_connect()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    queryType = 'None'
    rows = []
    # if user typed in a post ...
    if request.method == 'POST':
      searchTerm = request.form['search']
      if searchTerm == 'movies':
         query = "SELECT * from movies"
         queryType = 'movies'
      else:
        query = "SELECT * FROM stores where name LIKE '%%%s%%' OR type LIKE '%%%s%%' ORDER BY name" % (searchTerm, searchTerm)
        queryType = 'stores'

      cur.execute(query)
      rows = cur.fetchall()
      

    return render_template('index.html', queryType=queryType, results=rows, selectedMenu='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = utils.db_connect()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
      print "HI"
      username = request.form['username']
      pw = request.form['pw']
      query = "select * from users WHERE username = '%s' AND password = '%s'" % (username, pw)
      print query
      cur.execute(query)
      if cur.fetchone():
         return redirect(url_for('mainIndex'))
    return render_template('login.html', selectedMenu='Login')

@app.route('/checkLogin', methods=['POST'])
def checkLogin():
  abduction = {'firstname': request.form['firstname'],
               'lastname': request.form['lastname']}
  return render_template('report2.html', abduction = abduction)

@app.route('/simple')
def simple():
  return render_template('simple.html')

@app.route('/simple2', methods=['POST'])
def simple2():
  return render_template('simple2.html')


@app.route('/simple3')
def simple3():
  return render_template('simple3.html')

@app.route('/simple4', methods=['POST'])
def simple4():
  return render_template('simple4.html', name=request.form['name'])



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000)
