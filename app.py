from flask import Flask,redirect,url_for,render_template,request
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'meter_reading'
 
mysql = MySQL(app)

@app.route('/')
def welcome():
    return render_template('index.html')


### apt-get install libmysqlclient-dev 
@app.route('/action_page.php',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        date_and_time=request.form['date_and_time']
        meter_reading=int(request.form['meter_reading'])
        tower_id=request.form['tower_id']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO meter_reading (tower_id,date_and_time,meter_reading) VALUES(%s,%s,%s)", (tower_id,date_and_time,meter_reading))
        mysql.connection.commit()
        cur.close()

    return render_template('result.html', data= meter_reading, time=date_and_time, tower_name=tower_id)


if __name__=='__main__':
    app.run(debug=True)