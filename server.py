from flask import Flask, render_template, request, redirect, url_for
import MySQLdb, utils

app = Flask(__name__)

currentUser = ''

@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    db = utils.db_connect()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    queryType = 'None'
    print('User: ' + currentUser)
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
        print (query)
      cur.execute(query)
      rows = cur.fetchall()
      

    return render_template('index.html', queryType=queryType, results=rows, selectedMenu='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global currentUser
    db = utils.db_connect()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
      print "HI"
      username = request.form['username']
      currentUser = username

      pw = request.form['pw']
      query = "select * from users WHERE username = '%s' AND password = '%s'" % (username, pw)
      print query
      cur.execute(query)
      if cur.fetchone():
         return redirect(url_for('mainIndex'))
    return render_template('login.html', selectedMenu='Login')



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000)
