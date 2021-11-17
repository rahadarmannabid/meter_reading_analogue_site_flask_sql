from flask import Flask,redirect,url_for,render_template,request
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'meter_reading'
 
mysql = MySQL(app)

@app.route('/')
def welcome():
    return render_template('index.html')


### apt-get install libmysqlclient-dev 
@app.route('/action_page.php',methods=['POST','GET'])
def submit():
    
    if request.method=='POST':
        ### get the data from the form
        date_and_time=str(request.form['date_and_time'])
        ### replace the T of the date comes from front end 
        date_and_time=date_and_time.replace('T',' ')
        meter_reading=int(request.form['meter_reading'])
        tower_id=request.form['tower_id']
        ###connect the table from the sqlserver
        cur=mysql.connection.cursor()
        cur.execute("SELECT meter_reading From meter_reading")
        data=cur.fetchall()
        for row in data:
            previous_data=str(row)
            previous_data = previous_data.replace("(","").replace(")","").replace(",","")
            previous_data=int(previous_data)
            
        hourly_consumption=meter_reading-previous_data
        cur.execute("INSERT INTO meter_reading (tower_id,date_and_time,meter_reading,hourly_consumption) VALUES(%s,%s,%s,%s)", (tower_id,date_and_time,meter_reading,hourly_consumption))
        mysql.connection.commit()
        cur.close()

    return render_template('result.html', data= meter_reading, time=date_and_time, tower_name=tower_id, hourly_consumption=hourly_consumption)


if __name__=='__main__':
    app.run(debug=True)