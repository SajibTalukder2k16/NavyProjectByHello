from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3 as sql
from flask_mysqldb import MySQL
import MySQLdb
from flask_fontawesome import FontAwesome
from datetime import datetime, timedelta
import time
from datetime import date, timedelta
import csv
import os
import json

app = Flask(__name__, template_folder='template', static_folder='static',)
fa = FontAwesome(app)
app.secret_key = "123456"
mysql = MySQL(app)

Blood_Group = ['-','O+Ve','O-Ve','A+Ve','A-Ve','AB+Ve','AB-Ve','B+Ve','B-Ve']
Home_District = ['-', 'Bagerhat','Bandarban','Barguna','Barisal','Bhola','Bogra','Brahmanbaria','Chandpur','Chittagong','Chuadanga','Comilla','Cox\'s Bazar','Dhaka','Dinajpur','Faridpur','Feni','Gaibandha','Gazipur','Gopalganj','Habiganj','Jaipurhat','Jamalpur','Jessore','Jhalakati','Jhenaidah','Khagrachari','Khulna','Kishoreganj','Kurigram','Kushtia','Lakshmipur','Lalmonirhat','Madaripur','Magura','Manikganj','Meherpur','Moulvibazar','Munshiganj','Mymensingh','Naogaon','Narail','Narayanganj','Narsingdi','Natore','Nawabganj','Netrakona','Nilphamari','Noakhali','Pabna','Panchagarh','Parbattya Chattagram','Patuakhali','Pirojpur','Rajbari','Rajshahi','Rangpur','Satkhira','Shariatpur','Sherpur','Sirajganj','Sunamganj','Sylhet','Tangail','Thakurgaon']
Highest_Education = ['-','Class 8','SSC','HSC','B.Sc','BA','M.Sc','Diploma']
Ongoing_Education = ['-','SSC','HSC','B.Sc','BA','M.Sc']
Service_Category = ['-','Continuous','Non-Continuous']
Present_Engagement = ['-','Intial','1st','2nd','3rd','4th','5th']
Number_of_GCB = ['-','1st GCB','2nd GCB','3rd GCB']
Choice_of_Area_for_drafting = ['-','Dhaka','Khulna','Chattogram','Mongla','Patuakhali','Kaptai']
Choice_of_Next_Appointment = ['-','Instructor','Sea Service','Shore Service']
Medical_Category = ['-','A','B','C']
YesNo = ['-','No','Yes']
Name_of_Ship = ['-','ALI HAIDER','DURGAM','NISHAN','SANGU','GOMATI','ABU BAKR','SHAH AMANAT']
Branch = {  'Seaman' : ['OD', 'AB', 'LS', 'PO', 'CPO', 'SCPO(X)', 'MCPO(X)'],
            'Electrical' : ['EN-II', 'EN-I', 'LEN', 'EA-IV', 'EA-III', 'EA-II', 'EA-I', 'CEA', 'MCPO(L)'],
            'RadioElectrical' : ['REN-II','REN-I','LREN','REA-IV','REA-III','REA-II','REA-I','CREA','MCPO(R)'],
            'EngineRoom' : ['ME-II','ME-I','LME','ERA-IV','ERA-III','ERA-II','ERA-I','CERA','MCPO(E)'],
            'Supply' : ['SA-II','SA-I','LSA','PO(S)','CPO(S)','SCPO(S)','MCPO(S)'],
            'Secretariat':['WTR-II','WTR-I','LWTR','PO(WTR)','CPO(WTR)','SCPO(WTR)','MCPO(WTR)'],
            'Medical':['MA-II','MA-I','LMA','PO(MED)','CPO(MED)','SCPO(MED)','MCPO(MED)'],
            'Cook':['CK-II','CK-I','LCK','PO(CK)','CPO(CK)','SCPO(CK)','MCPO(CK)'],
            'Topaz':['TOP-II','TOP-I','LTOP'],
            'Ordnance':['EN-II(ORD)','EN-I(ORD)','LEN(ORD)','OA-IV','OA-III','OA-II','OA-I','COA','MCPO(OE)'],
            'Shipwright':['ME-II(SW)','ME-I(SW)','LME(SW)','ERA-IV(SW)','ERA-III(SW)','ERA-II(SW)','ERA-I(SW)','SERA(SW)','MCPO(SW)'],
            'Provost':['PM-II','PM-I','LPN','PO(R)','MAA','SCPO(REG)','MCPO(REG)'],
            'Steward':['STWD-II','STWD-I','LSTWD','PO(STWD)','CPO(STWD)','SCPO(STWD)','MCPO(STWD)']
            }
Marital_Status = ['-','Single', 'Married', 'Divorced']
Leave_Category = ['P Leave','C Leave','Recreation Leave','Sick Leave','Ex Bangladesh Leave']
User_Type = ['System Administrator', 'ADO', 'Divisional Officer', 'Commanding Officer', 'Staff Officer', 'Comflot', 'Sailor']
Static_Search_list_for_database = ['StateofOverWeight' , 'Height' , 'Emailaddress', 'ServiceIdCardNo' , 'NIDCardNo' , 'DrivingLicenseNo','name','MobileNo_1','MobileNo_2','ServiceIdCardNo' , 'NIDCardNo' , 'DrivingLicenseNo','Emailaddress','MobileNo','FathersMobileNo','MothersMobileNo','Medicalcategory','NameofShip','AddressofWife','LastDateofBloodDonation', 'MLR']
Static_Search_list_for_html = ['Name','Mobile No 1','Mobile No 2','Service Id CardNo' , 'NID Card No' , 'Driving License No','Email address','Wife Mobile No','Fathers Mobile No','Mothers Mobile No','Brothers Mobile No','Medical Category','Name of Ship']
Column = ['O_No' ,'ADO_O_No', 'name' , 'Branch' , 'Rank' , 'BloodGroup', 'marrital_status', 'PresentAddress' , 'PermanentAddress' , 'DateofBirth' , 'DateofMarriage' , 'MobileNo_1' , 'MobileNo_2' , 'Weight' , 'StateofOverWeight' , 'Height' , 'Emailaddress', 'ServiceIdCardNo' , 'NIDCardNo' , 'DrivingLicenseNo', 'NextofKin' , 'Relationship' , 'ContactNumberofNextofKin' , 'NameofWife' , 'MobileNo', 'AddressofWife'  , 'Anyspecialinfowife'   , 'FathersName' , 'FathersMobileNo' , 'MothersName' , 'MothersMobileNo' , 'FathersAddress' , 'MothersAddress', 'FamilyCrisis', 'ServiceCategory', 'PresentEngagement' , 'NextREEngagementDue' , 'DateofNextIncrement' , 'DateofNextGCB', 'NumberofGCB' , 'EffectivedateofexistingGCB', 'DateofNextPromotion', 'Medicalcategory' , 'DateofLastPromotion' , 'DateofJoiningService' , 'DateofJoiningShip' , 'NameofShip' ,'NumberofDaysatSea', 'UNMission' , 'GoodWillMission' , 'DAONumber', 'highestEducation' , 'OngoingcivilEducation' ,'NameofImportantCourses' , 'NameofNextCourse' , 'ForeignCourse' , 'SpecialQualification' ,'ChoiceofAreaForPosting' , 'ChoiceofNextAppointment' , 'ChoiceofNextCourse' ,'ExtraCurricularActivities' , 'GamesAndSports', 'LastDateofBloodDonation', 'MLR' ]

#mysql database creation and connection
with app.app_context():
    try:
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'hello'
        cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS navy")
        mysql.connection.commit()
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_DB'] = 'navy'
        cur.execute('use navy')    
        cur.execute('CREATE TABLE IF NOT EXISTS System (O_No varchar(30) PRIMARY KEY, pass text)')
        cur.execute('CREATE TABLE IF NOT EXISTS Comflot (O_No varchar(30) PRIMARY KEY, pass text, name text, Branch text, Rank text)')
        cur.execute('CREATE TABLE IF NOT EXISTS Staff (O_No varchar(30) PRIMARY KEY, pass text, name text, Branch text, Rank text)')
        cur.execute('CREATE TABLE IF NOT EXISTS Commanding (O_No varchar(30) PRIMARY KEY, pass text, name text, NameofShip text, Branch text, Rank text)')
        cur.execute('CREATE TABLE IF NOT EXISTS Divisional (O_No varchar(30) PRIMARY KEY, pass text, name text, Branch text, Rank text, CO_O_No varchar(30), foreign key(CO_O_No) references Commanding(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS ADO (O_No varchar(30) PRIMARY KEY, pass text, name text, Branch text, Rank text, DO_O_No varchar(30), foreign key(DO_O_No) references Divisional(O_No))')
        query = 'CREATE TABLE IF NOT EXISTS Sailor (O_No varchar(30) PRIMARY KEY, ADO_O_No varchar(30)'
        for i in range(2, len(Column)):
            query = query + ', ' + Column[i] + ' text'
        query = query + ', foreign key(ADO_O_No) references ADO(O_No))'
        cur.execute(query)
        cur.execute('CREATE TABLE IF NOT EXISTS Sibling (idx int NOT NULL AUTO_INCREMENT  PRIMARY KEY,SiblingName text, SiblingMobileNo text , SiblingAddress text,O_No varchar(30), foreign key(O_No) references Sailor(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS  Children (idx int NOT NULL AUTO_INCREMENT  PRIMARY KEY,ChildrenName text, DOBofChildren text , Anyspecialinfochildren text,O_No varchar(30), foreign key(O_No) references Sailor(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS Area_Remark (idx int NOT NULL AUTO_INCREMENT PRIMARY KEY, O_No_to varchar(30), O_No_from varchar(30), remarks TEXT, date TEXT, foreign key(O_No_to) references Sailor(O_No), foreign key(O_No_from) references Comflot(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS CO_Remark (idx int NOT NULL AUTO_INCREMENT PRIMARY KEY, O_No_to varchar(30), O_No_from varchar(30), remarks TEXT, date TEXT, foreign key(O_No_to) references Sailor(O_No), foreign key(O_No_from) references Commanding(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS DO_Remark (idx int NOT NULL AUTO_INCREMENT PRIMARY KEY, O_No_to varchar(30), O_No_from varchar(30), remarks TEXT, date TEXT, foreign key(O_No_to) references Sailor(O_No), foreign key(O_No_from) references Divisional(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS ADO_Remark (idx int NOT NULL AUTO_INCREMENT PRIMARY KEY, O_No_to varchar(30), O_No_from varchar(30), remarks TEXT, date TEXT, foreign key(O_No_to) references Sailor(O_No), foreign key(O_No_from) references ADO(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS TY (idx int NOT NULL AUTO_INCREMENT PRIMARY KEY, fromty TEXT, toty TEXT, tybillet TEXT, purpose TEXT, duration TEXT, securityclearence TEXT, O_No varchar(30), foreign key(O_No) references Sailor(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS Evaluation (idx int NOT NULL AUTO_INCREMENT PRIMARY KEY,dateofevaluation text,nameoftask text,performance text,achivementpoint text,special text,O_No varchar(30), foreign key(O_No) references Sailor(O_No))')
        cur.execute('CREATE TABLE IF NOT EXISTS LeaveHistory (idx int NOT NULL AUTO_INCREMENT PRIMARY KEY,type text,froml text,tol text,O_No varchar(30), foreign key(O_No) references Sailor(O_No))')
        cur.execute("INSERT INTO System (O_No, pass) VALUES (%s, %s)", ("admin", '123456'))
    except:
        print("Database Connection or Creation Problem Detected.")
    mysql.connection.commit()
    cur.close()
#mysql database creation end

@app.context_processor
def inject_user():
    id = ''
    usertype = ''
    if 'O_No' in session:
        id = session['O_No']
        usertype = session['usertype']
    return dict(user=id, type = usertype)

def addyearmonth(joindate,addyear,addmonth):
    year = joindate.year
    month = joindate.month
    month = month + (addmonth-1)
    year = year + addyear + int(month/12)
    month = (month%12)+1
    day = joindate.day
    returndate = str(year)+"-"+str(month)+"-"+str(day)
    returndate = datetime.strptime(returndate,'%Y-%m-%d')
    return returndate

def calculateReEngagement(joiningdate,pengage,scat):
    if(scat==0):
        if(pengage==0):
            rengdate = addyearmonth(joiningdate,12,8)
            return rengdate
        elif(pengage==1):
            rengdate = addyearmonth(joiningdate,20,8)
            return rengdate
        elif(pengage==2):
            rengdate = addyearmonth(joiningdate,25,8)
            return rengdate
        elif(pengage==3):
            rengdate = addyearmonth(joiningdate,30,8)
            return rengdate
        elif(pengage==4):
            rengdate = addyearmonth(joiningdate,32,8)
            return rengdate
        elif(pengage==5):
            rengdate = addyearmonth(joiningdate,34,8)
            return rengdate
    elif(scat==1):
        if(pengage==0):
            rengdate = addyearmonth(joiningdate,3,8)
            return rengdate
        elif(pengage==1):
            rengdate = addyearmonth(joiningdate,6,8)
            return rengdate
        elif(pengage==2):
            rengdate = addyearmonth(joiningdate,9,8)
            return rengdate
        elif(pengage==3):
            rengdate = addyearmonth(joiningdate,21,8)
            return rengdate
        elif(pengage==4):
            rengdate = addyearmonth(joiningdate,29,8)
            return rengdate
        elif(pengage==5):
            rengdate = addyearmonth(joiningdate,34,8)
            return rengdate

def getnotification():
    notificationlist = []
    e_list = eligiblelist_to_dictionary(eligiblelist())
    today = datetime.strptime(str(date.today()),'%Y-%m-%d')
    for row in e_list:
        mcur = mysql.connection.cursor()
        mcur.execute("Select * from TY where toty = '' and O_No = %s", (row['O_No'], ))
        rows = mcur.fetchall()
        
        for trow in rows:
            print(trow)
            fromty = datetime.strptime(trow[1],'%Y-%m-%d')
            returnty = fromty + timedelta(days = int(trow[5] ) - 1)
            returntyalert = fromty + timedelta(days = int(trow[5]) - 3)
            print(returnty, returntyalert)
            if today >= returntyalert and today <= returnty:
                notificationlist.append({'O_No': row['O_No'], "Notification" : "Return from TY for O_No : " + row['O_No'] + ", Name : " + row['name'] + ", Name of Ship : " + row['NameofShip'] + ", Branch : " + row['Branch'] + ", Rank : " + row['Rank'] + " on " + str(returnty)})
            elif today >= returnty:
                notificationlist.append({'O_No': row['O_No'], "Notification" : "Return from TY time is Over for O_No : " + row['O_No'] + ", Name : " + row['name'] + ", Name of Ship : " + row['NameofShip'] + ", Branch : " + row['Branch'] + ", Rank : " + row['Rank'] + " on " + str(returnty)})
        mcur.close()

        
        if row['NextREEngagementDue'] != '':
            nextreengagementdue = datetime.strptime(row['NextREEngagementDue'],'%Y-%m-%d')
            nextreengagementduealert = nextreengagementdue - timedelta(days = 5)
            if today >= nextreengagementduealert and today <= nextreengagementdue:
                notificationlist.append({'O_No': row['O_No'], "Notification" : "Next Re Engagement Due for O_No : " + row['O_No'] + ", Name : " + row['name'] + ", Name of Ship : " + row['NameofShip'] + ", Branch : " + row['Branch'] + ", Rank : " + row['Rank'] + " on " + str(nextreengagementdue)})
        
        if row['DateofNextIncrement'] != '':
            dateofnextincrement = datetime.strptime(row['DateofNextIncrement'],'%Y-%m-%d')
            dateofnextincrementalert = dateofnextincrement - timedelta(days = 5)
            if today >= dateofnextincrementalert and today <= dateofnextincrement:
                notificationlist.append({'O_No': row['O_No'], "Notification" : "Date of Next Increment for O_No : " + row['O_No'] + ", Name : " + row['name'] + ", Name of Ship : " + row['NameofShip'] + ", Branch : " + row['Branch'] + ", Rank : " + row['Rank'] + " on " + str(nextreengagementdue)})
        
        if row['DateofNextGCB'] != '':
            dateofnextgcb = datetime.strptime(row['DateofNextGCB'],'%Y-%m-%d')
            dateofnextgcbalert = dateofnextgcb - timedelta(days = 120)
            if today >= dateofnextgcbalert and today <= dateofnextgcb:
                notificationlist.append({'O_No': row['O_No'], "Notification" : "Date of Next GCB for O_No : " + row['O_No'] + ", Name : " + row['name'] + ", Name of Ship : " + row['NameofShip'] + ", Branch : " + row['Branch'] + ", Rank : " + row['Rank'] + " on " + str(nextreengagementdue)})
        if row['DateofJoiningService'] != '':
            rldue = datetime.strptime(row['DateofJoiningService'],'%Y-%m-%d')
            rlduealert = rldue - timedelta(days = 30)
            if today >= dateofnextgcbalert and today <= dateofnextgcb:
                notificationlist.append({'O_No': row['O_No'], "Notification" : "RL Due for O_No : " + row['O_No'] + ", Name : " + row['name'] + ", Name of Ship : " + row['NameofShip'] + ", Branch : " + row['Branch'] + ", Rank : " + row['Rank'] + " on " + str(rldue)})
        

    return notificationlist


@app.route('/')
def home():
    if('O_No' in session):
        login_status = True
        notifications = getnotification()
        if len(notifications):
            session['notifications'] = True
        return render_template("index.html",login_status=login_status)
    else:
        return redirect(url_for('login_page'))
    
@app.route('/login_page')
def login_page():
    if 'O_No' in session:
        session['notifications'] = False
        return redirect(url_for('home'))
    else:
        return render_template('login_page.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = request.form
        #mysql login 
        cur = mysql.connection.cursor()
        sql_select_query = """select pass from System where O_No = %s"""
        cur.execute(sql_select_query, (result['O_No'],))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == result['password']:
                session['usertype'] = '0'
                session['usertype1'] = 'System Admin'
                session['O_No'] = result['O_No']
        cur.close()
        cur = mysql.connection.cursor()
        sql_select_query = """select pass from Comflot where O_No = %s"""
        cur.execute(sql_select_query, (result['O_No'],))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == result['password']:
                session['usertype'] = '5'
                session['usertype1'] = 'Comflot'
                session['O_No'] = result['O_No']
        cur.close()
        cur = mysql.connection.cursor()
        sql_select_query = """select pass from Staff where O_No = %s"""
        cur.execute(sql_select_query, (result['O_No'],))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == result['password']:
                session['usertype'] = '4'
                session['usertype1'] = 'Staff Officer'
                session['O_No'] = result['O_No']
        
        cur.close()
        cur = mysql.connection.cursor()
        sql_select_query = """select pass from Commanding where O_No = %s"""
        cur.execute(sql_select_query, (result['O_No'],))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == result['password']:
                session['usertype'] = '3'
                session['usertype1'] = 'Commanding Officer'
                session['O_No'] = result['O_No']
        
        cur.close()
        cur = mysql.connection.cursor()
        sql_select_query = """select pass from Divisional where O_No = %s"""
        cur.execute(sql_select_query, (result['O_No'],))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == result['password']:
                session['usertype'] = '2'
                session['usertype1'] = 'Divisional Officer'
                session['O_No'] = result['O_No']
        
        cur.close()
        cur = mysql.connection.cursor()
        sql_select_query = """select pass from ADO where O_No = %s"""
        cur.execute(sql_select_query, (result['O_No'],))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == result['password']:
                session['usertype'] = '1'
                session['usertype1'] = 'ADO'
                session['O_No'] = result['O_No']
        session['notifications'] = False
        cur.close()

    return redirect(url_for('home'))

@app.route('/ownprofile')
def ownprofile():
    if 'O_No' in session:
        if session['usertype'] == '0':
            query = "select * from System where O_No = %s"
        if session['usertype'] == '1':
            query = "select * from ADO where O_No = %s"
        if session['usertype'] == '2':
            query = "select * from Divisional where O_No = %s"
        if session['usertype'] == '3':
            query = "select * from Commanding where O_No = %s"
        if session['usertype'] == '4':
            query = "select * from Staff where O_No = %s"
        if session['usertype'] == '5':
            query = "select * from Comflot where O_No = %s"
        mcur = mysql.connection.cursor()
        mcur.execute(query, (session['O_No'], ))
        rows = mcur.fetchall()
        print(rows)
        mcur.close()
        return render_template('ownprofile.html', rows  = rows[0], login_status = True)

@app.route('/addadminlist')
def addadminlist():
    if 'O_No' in session:
        mcur = mysql.connection.cursor()
        if session['usertype'] == '2':
            mcur.execute("Select * from ADO where DO_O_No = %s", (session['O_No'],))
        elif session['usertype'] == '3':
            mcur.execute("select ADO.O_No, ADO.pass, ADO.name, ADO.Branch, ADO.Rank, ADO.DO_O_No, Divisional.CO_O_No from ADO join Divisional on ADO.DO_O_No = Divisional.O_No where Divisional.CO_O_No = %s;", (session['O_No'], ))
        else:
            mcur.execute("Select * from ADO")
        adolist = mcur.fetchall()
        print(adolist)
        mcur.close()
        
        mcur = mysql.connection.cursor()
        if session['usertype'] == '3':
            mcur.execute("Select * from Divisional where CO_O_No = %s", (session['O_No'], ))
        else:
            mcur.execute("Select * from Divisional")
        dolist = mcur.fetchall()
        mcur.close()

        mcur = mysql.connection.cursor()
        mcur.execute("Select * from Commanding")
        colist = mcur.fetchall()
        mcur.close()

        mcur = mysql.connection.cursor()
        mcur.execute("Select * from Staff")
        stafflist = mcur.fetchall()
        mcur.close()

        mcur = mysql.connection.cursor()
        mcur.execute("Select * from Comflot")
        comflotlist = mcur.fetchall()
        mcur.close()


        mcur = mysql.connection.cursor()
        mcur.execute("Select * from System")
        systemlist = mcur.fetchall()
        mcur.close()
        return render_template("addadminlist.html", systemlist = systemlist, comflotlist = comflotlist, stafflist = stafflist, colist = colist, dolist = dolist, adolist = adolist, login_status = True)
    return redirect(url_for("home"))

@app.route('/addadminlist/updateadmin/<string:uid>/<string:admintype>')
def updateadmin(uid, admintype):
    if 'O_No' in session:
        mcur = mysql.connection.cursor()
        if admintype == '0':
            mcur.execute("Select * from System where O_No = %s", (uid,))
            rows = mcur.fetchall()
        if admintype == '5':
            mcur.execute("Select * from Comflot where O_No = %s", (uid,))
            rows = mcur.fetchall()
        if admintype == '4':
            mcur.execute("Select * from Staff where O_No = %s", (uid,))
            rows = mcur.fetchall()
        if admintype == '3':
            mcur.execute("Select * from Commanding where O_No = %s", (uid,))
            rows = mcur.fetchall()
        if admintype == '2':
            mcur.execute("Select * from Divisional where O_No = %s", (uid,))
            rows = mcur.fetchall()
        if admintype == '1':
            mcur.execute("Select * from ADO")
            rows = mcur.fetchall()
        row = rows[0]
        mcur.close()
        return render_template('updateadmin.html',row = row, uid = uid, id = int(admintype), login_status = True, Name_of_Ship = Name_of_Ship,Branch_key = Branch, Branch = json.dumps(Branch))

@app.route('/addadminlist/updateadmin/<string:uid>/<string:admintype>/updatingadmin', methods = ['POST', 'GET'])
def updatingadmin(uid, admintype):
    if 'O_No' in session:
        if request.method == 'POST':
            req = request.form.to_dict(flat=False)
            mcur = mysql.connection.cursor()
            if admintype == '0':
                 query = "UPDATE System SET "
            if admintype == '1':
                query = "UPDATE ADO SET "
            if admintype == '2':
                 query = "UPDATE Divisional SET "
            if admintype == '3':
                 query = "UPDATE Commanding SET "
            if admintype == '4':
                 query = "UPDATE Staff SET "
            if admintype == '5':
                 query = "UPDATE Comflot SET "
            param = ()
            first = True
            for key in req:
                if first:
                    query += key + " = %s "
                else:
                    query += ", "+ key + " = %s "
                first = False
                param = param +( req[key][0], )
            query += "WHERE O_No = %s"
            param = param + (uid, )
            mcur.execute(query, param)
            mcur.connection.commit()
            mcur.close()
        
            return redirect(url_for('addadminlist'))
    return redirect(url_for('home'))

@app.route('/addadminlist/handover/<string:admintype>', methods = ['POST', 'GET'])
def handover(admintype):
    if 'O_No' in session:
        if request.method == 'POST':
            req = request.form
            mcur = mysql.connection.cursor()
            if admintype == 'ADO':
                mcur.execute("UPDATE Sailor SET ADO_O_No = %s WHERE ADO_O_No = %s", (req['newado'], req['oldado'], ))
            if admintype == "DO":
                mcur.execute("UPDATE ADO SET DO_O_No = %s WHERE DO_O_No = %s", (req['newdo'], req['olddo'], ))
            if admintype == "CO":
                mcur.execute("UPDATE Divisional SET CO_O_No = %s WHERE CO_O_No = %s", (req['newco'], req['oldco'], ))
            mcur.connection.commit()
            mcur.close()
            return redirect(url_for('addadminlist'))
    return redirect(url_for('home'))

@app.route('/addadminlist/addadmin/<int:id>')
def addadmin(id):
    if 'O_No' in session:
        return render_template('addadmin.html', login_status = True, Name_of_Ship = Name_of_Ship, id = id,Branch_key = Branch, Branch = json.dumps(Branch))
    return redirect(url_for("home"))

@app.route('/adminlist/addadmin/<int:id>/addingadmin', methods = ['POST', 'GET'])
def addingadmin(id):
    if 'O_No' in session:
        if request.method == 'POST':
            try:
                req = request.form.to_dict(flat=False)
                mcur = mysql.connection.cursor()
                if id == 0:
                    query = "INSERT INTO System ("
                if id == 5:
                    query = "INSERT INTO Comflot ("
                if id == 4:
                    query = "INSERT INTO Staff ("
                if id == 3:
                    query = "INSERT INTO Commanding ("
                if id == 2:
                    query = "INSERT INTO Divisional ("
                if id == 1:
                    query = "INSERT INTO ADO ("
                param = ()
                first = True
                for key in req:
                    if first:
                        query += key
                    else:
                        query += ", "+ key
                    first = False
                    param = param +( req[key][0], )
                query += ") VALUES ("
                first = True
                for key in req:
                    if first:
                        query += "%s"
                    else:
                        query += ", %s"
                    first = False
                query += ")"
                #return query
                mcur.execute(query, param)
                #mcur.execute("INSERT INTO ADO (O_No, pass, name, DO_O_No, Branch, Rank) VALUES(%s, %s, %s, %s, %s, %s)",(req['O_No1'][0], req['pass1'][0], req['name1'][0], req['DO_O_No1'], req['Branch'][0], req['Rank'][0],))
                
                mysql.connection.commit()
                mcur.close()
            except:
                pass

            return redirect(url_for('addadminlist'))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if 'O_No' in session:
        session.pop('O_No', None)
        session.pop('usertype', None)
        session['notifcations'] = False
        session['logged_in']=False
    return redirect(url_for('home'))

def eligiblelist():
    ret = []
    if('O_No' in session):
        if session['usertype'] == '0' or session['usertype'] == '5' or session['usertype'] == '4':
            with app.app_context():
                cur = mysql.connection.cursor()
                sql_select_query = """select * from Sailor"""
                cur.execute(sql_select_query)
                rows = cur.fetchall()
                for row in rows:
                    temp = []
                    for i in range(len(row)):
                        temp.append(row[i])
                    ret.append(temp)

                cur.close() 
        elif session['usertype'] == '3' :
            cur = mysql.connection.cursor()
            sql_select_query = """select NameofShip from Commanding where O_No = %s"""
            cur.execute(sql_select_query,(session['O_No'],))
            rows = cur.fetchall()
            shipname = rows[0][0]
            sql_select_query = """select * from Sailor where NameofShip = %s"""
            cur.execute(sql_select_query, (shipname, ))
            rows = cur.fetchall()
            for row in rows:
                temp = []
                for i in range(len(row)):
                    temp.append(row[i])
                ret.append(temp)
            cur.close() 
        elif session['usertype'] == '2' :
            cur = mysql.connection.cursor()
            sql_select_query = """select O_No from ADO where DO_O_No = %s"""
            cur.execute(sql_select_query,(session['O_No'],))
            rows = cur.fetchall()
            for row in rows:
                ado_id= row[0]
                cur = mysql.connection.cursor()
                sql_select_query = """select * from Sailor where ADO_O_No = %s"""
                cur.execute(sql_select_query, (ado_id, ))
                rows = cur.fetchall()
                for row in rows:
                    temp = []
                    for i in range(len(row)):
                        temp.append(row[i])
                    ret.append(temp)
                cur.close() 
        elif session['usertype'] == '1' :
            cur = mysql.connection.cursor()
            sql_select_query = """select * from Sailor where ADO_O_No = %s"""
            cur.execute(sql_select_query, (session['O_No'], ))
            rows = cur.fetchall()
            for row in rows:
                temp = []
                for i in range(len(row)):
                    temp.append(row[i])
                ret.append(temp)
            cur.close() 

    return ret 

def eligiblelist_to_dictionary(e_list):
    ret = []
    for row in e_list:
        temp = {}
        for i in range(len(row)):
            temp[Column[i]] = row[i]
        ret.append(temp)
    return ret

def eligiblelist_to_list(e_list):
    ret = []
    for row in e_list:
        temp = []
        for i in Column:
            temp.append(row[i])
        ret.append(temp)
    return ret

@app.route('/show')
def show():
    if('O_No' in session):
        login_status = True
        e_list = eligiblelist()
        return render_template("show.html",static_on = 1,Static_Search_list_for_database = Static_Search_list_for_database,Static_Search_list_for_html = Static_Search_list_for_html, rows = e_list,login_status=login_status)

    else:
        login_status = False



@app.route('/notification')
def notification():
    if 'O_No' in session:
        if session['usertype'] == '1' or session['usertype'] == '2' or session['usertype'] == '3':
            notifications = getnotification()
            return render_template('notification.html', login_status = True, rows = notifications)
    return redirect(url_for('home'))

@app.route('/show/search', methods = ['POST', 'GET'])
def search_static():
    if 'O_No' in session:
        if request.method == 'POST':
            req = request.form.to_dict(flat=False)
            login_status = True
            e_list = eligiblelist()
            e_list = eligiblelist_to_dictionary(e_list)
            ret = []
            for row in e_list:
                if req['field'][0] is None:
                    req['field'][0] = ''
                id = row['O_No']
                cur = mysql.connection.cursor()
                sql_select_query = """select SiblingMobileNo from Sibling where O_No = %s"""
                cur.execute(sql_select_query,(id,))
                rows = cur.fetchall()
                l = len(rows)
                for i in range(l):
                    if(len(rows[i])==1):
                        if req['field'][0].lower() in rows[i][0].lower():
                            if row not in ret:
                                ret.append(row)
                for value in Static_Search_list_for_database:
                    if req['field'][0].lower() in row[value].lower():
                        if row not in ret:
                            ret.append(row) 
            e_list = eligiblelist_to_list(ret)
            return render_template("show.html",static_on = 0, Static_Search_list_for_database = Static_Search_list_for_database,Static_Search_list_for_html = Static_Search_list_for_html, rows = e_list,login_status=login_status)

    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>')
def profile(id):
    
    if('O_No' in session):
        login_status = True
        
    else:
        login_status = False
        return redirect(url_for('home'))
    e_list = eligiblelist()
    ok = False
    for row in e_list:
        if row[0] == id:
            ok = True
    if 'O_No' in session and ok == True:
        with app.app_context():
                cur = mysql.connection.cursor()
                sql_select_query = """select * from Sailor where O_No = %s"""
                cur.execute(sql_select_query, (id, ))
                rows = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                sql_select_query = """select * from Children where O_No = %s"""
                cur.execute(sql_select_query, (id, ))
                childrenrows = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                sql_select_query = """select * from Sibling where O_No = %s"""
                cur.execute(sql_select_query, (id, ))
                siblingrows = cur.fetchall()
                cur.close()
        
        temprow = {}
        for i in range(len(rows[0])):
            temprow[Column[i]]=rows[0][i]
        childrenrow = []
        print(childrenrows)
        for row in childrenrows:
            temp = []
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            childrenrow.append(temp)
        siblingrow = []
        for row in siblingrows:
            temp = []
            temp.append(row[1])
            temp.append(row[2])
            temp.append(row[3])
            siblingrow.append(temp)
        return render_template('profile.html', id = id,siblingrow = siblingrow,childrenrow = childrenrow, rows = temprow, login_status = login_status, Column = Column)
        #return render_template('profile.html',id = id, Column = Column,usertype = usertype,rows=temprow,Name_of_Ship = Name_of_Ship, Medical_Category = Medical_Category,YesNo = YesNo,Home_District = Home_District, Marital_Status = Marital_Status,Branch_key = Branch, Branch = json.dumps(Branch), Blood_Group = Blood_Group, Highest_Education = Highest_Education, Ongoing_Education = Ongoing_Education, Service_Category = Service_Category, Present_Engagement = Present_Engagement, Number_of_GCB = Number_of_GCB, Choice_of_Area_for_drafting = Choice_of_Area_for_drafting, Choice_of_Next_Appointment = Choice_of_Next_Appointment, User_Type = User_Type, login_status=login_status)
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/editprofile')
def editprofile(id):
    if('O_No' in session):
        login_status = True
    else:
        login_status = False
        return redirect(url_for('home'))
    if session['usertype'] != '4':
        e_list = eligiblelist()
        ok = False
        for row in e_list:
            if row[0] == id:
                ok = True
        if 'O_No' in session and ok == True:
            with app.app_context():
                    cur = mysql.connection.cursor()
                    sql_select_query = """select * from Sailor where O_No = %s"""
                    cur.execute(sql_select_query, (id, ))
                    rows = cur.fetchall()
                    cur.close()
                    cur = mysql.connection.cursor()
                    sql_select_query = """select * from Children where O_No = %s"""
                    cur.execute(sql_select_query, (id, ))
                    childrenrows = cur.fetchall()
                    cur.close()
                    cur = mysql.connection.cursor()
                    sql_select_query = """select * from Sibling where O_No = %s"""
                    cur.execute(sql_select_query, (id, ))
                    siblingrows = cur.fetchall()
                    cur.close()
            usertype = int(session['usertype'])
            temprow = {}
            for i in range(len(rows[0])):
                temprow[Column[i]] = rows[0][i]
            
            childrenrow = []
            for row in childrenrows:
                temp = []
                temp.append(row[1])
                temp.append(row[2])
                temp.append(row[3])
                childrenrow.append(temp)
            siblingrow = []
            for row in siblingrows:
                temp = []
                temp.append(row[1])
                temp.append(row[2])
                temp.append(row[3])
                siblingrow.append(temp)
            return render_template('editprofile.html',childrenrow = childrenrow, siblingrow = siblingrow ,id = id, Column = Column,usertype = usertype,rows=temprow,Name_of_Ship = Name_of_Ship, Medical_Category = Medical_Category,YesNo = YesNo,Home_District = Home_District, Marital_Status = Marital_Status,Branch_key = Branch, Branch = json.dumps(Branch), Blood_Group = Blood_Group, Highest_Education = Highest_Education, Ongoing_Education = Ongoing_Education, Service_Category = Service_Category, Present_Engagement = Present_Engagement, Number_of_GCB = Number_of_GCB, Choice_of_Area_for_drafting = Choice_of_Area_for_drafting, Choice_of_Next_Appointment = Choice_of_Next_Appointment, User_Type = User_Type, login_status=login_status)

    return redirect(url_for('profile',id = id))

@app.route('/adduser')
def adduser():
    if 'O_No' in session:
        return render_template('adduser.html',Name_of_Ship = Name_of_Ship, Medical_Category = Medical_Category,YesNo = YesNo,Home_District = Home_District, Marital_Status = Marital_Status,Branch_key = Branch, Branch = json.dumps(Branch), Blood_Group = Blood_Group, Highest_Education = Highest_Education, Ongoing_Education = Ongoing_Education, Service_Category = Service_Category, Present_Engagement = Present_Engagement, Number_of_GCB = Number_of_GCB, Choice_of_Area_for_drafting = Choice_of_Area_for_drafting, Choice_of_Next_Appointment = Choice_of_Next_Appointment, User_Type = User_Type, login_status=True)
    return redirect(url_for('home'))

@app.route('/adduser/adding_user',methods=['POST','GET'])
def adding_user():
     if 'O_No' in session:
        if request.method =='POST':
            req = request.form.to_dict(flat=False)
            dic=dict()
            for col in Column:
                if col in req:
                    #print(req[col])
                    if(req[col][0]=='- - -'):
                        req[col][0]=''
                    if(req[col][0]!=''):
                        dic[col]=req[col][0]
            #try:
            if('Weight' in dic and 'Height' in dic):
                dic['StateofOverWeight']=round(float(dic['Weight'])*float(dic['Weight'])/float(dic['Height']),2)
            #nextreengagement calculation
            if('DateofJoiningShip' in dic):
                dateofjoiningship = dic['DateofJoiningShip']
                if('PresentEngagement' in dic and dic['PresentEngagement'] != '-'):
                    presentengagement = Present_Engagement.index(dic['PresentEngagement']) - 1
                    if('ServiceCategory' in dic and dic['ServiceCategory'] != '-'):
                        servicecategory = Service_Category.index(dic['ServiceCategory']) - 1
                        dateofjoiningship = datetime.strptime(dateofjoiningship,'%Y-%m-%d')
                        dic['NextREEngagementDue']=calculateReEngagement(dateofjoiningship,presentengagement,servicecategory)
                        dic['NextREEngagementDue'] = dic['NextREEngagementDue'].strftime("%Y-%m-%d")     
            if('EffectivedateofexistingGCB' in dic):
                effectivedateofexistinggcb = dic['EffectivedateofexistingGCB']
                effectivedateofexistinggcb = datetime.strptime(effectivedateofexistinggcb,'%Y-%m-%d')
                dic['DateofNextGCB'] = addyearmonth(effectivedateofexistinggcb,4,0)
                dic['DateofNextGCB'] = dic['DateofNextGCB'].strftime("%Y-%m-%d")
            #date of next increment
            if('DateofJoiningShip' in dic):
                DateofJoiningShip = dic['DateofJoiningShip']
                DateofJoiningShip = datetime.strptime(DateofJoiningShip,'%Y-%m-%d')
                dic['DateofNextIncrement'] = addyearmonth(DateofJoiningShip,0,11)
                dic['DateofNextIncrement'] = dic['DateofNextIncrement'].strftime("%Y-%m-%d")
            if 'ADO_O_No' not in dic:
                dic['ADO_O_No'] = session['O_No']
            for col in Column:
                if(col not in dic):
                    dic[col]=''
                else:
                    dic[col]=str(dic[col])
            query = "INSERT INTO Sailor (O_No "
            for i in range(1,len(Column)):
                query = query + ', ' + Column[i]
            query += ')  VALUES ( %s'
            for i in range(1,len(Column)):
                query += ",%s"
            query += ')'
            param = ()
            for col in Column:
                param = param +( dic[col], )
                
            mcur = mysql.connection.cursor()
            mcur.execute(query, param)
            mysql.connection.commit()
            mcur.close()
            ret = []
            req = request.form
            mcur = mysql.connection.cursor()
            for i in range(1,100):
                id1 = 'SiblingName' + str(i)
                id2 = 'SiblingMobileNo' + str(i)
                id3 = 'SiblingAddress' + str(i)
                if id1 in req:
                    if (req[id1] is None and req[id2] is None and req[id3] is None) or( req[id1] == '' and req[id2] == '' and req[id3] == ''):
                        pass
                    else:
                        mcur.execute("INSERT INTO Sibling (SiblingName,SiblingMobileNo,SiblingAddress,O_No) VALUES (%s,%s,%s,%s)",(req[id1],req[id2],req[id3],req['O_No']))
                        ret.append((req[id1], req[id2], req[id3]))
            mysql.connection.commit()
            mcur.close()

            ret = []
            req = request.form
            mcur = mysql.connection.cursor()
            for i in range(1,100):
                id1 = 'ChildrenName' + str(i)
                id2 = 'DOBofChildren' + str(i)
                id3 = 'Anyspecialinfochildren' + str(i)
                if id1 in req:
                    if (req[id1] is None and req[id2] is None and req[id3] is None) or( req[id1] == '' and req[id2] == '' and req[id3] == ''):
                        pass
                    else:
                        mcur.execute("INSERT INTO Children (ChildrenName,DOBofChildren,Anyspecialinfochildren,O_No) VALUES (%s,%s,%s,%s)",(req[id1],req[id2],req[id3],req['O_No']))
                        ret.append((req[id1], req[id2], req[id3]))
            mysql.connection.commit()
            mcur.close()
            #except:
                #pass
        
     return redirect(url_for('show'))    

@app.route('/profile/<string:id>/updating_user', methods = ['POST', 'GET'])
def updating_user(id):
    if 'O_No' in session:
        
        if request.method =='POST':
            req = request.form.to_dict(flat=False)
            dic=dict()
            for col in Column:
                if col in req:
                    if(req[col][0]=='- - -'):
                        req[col][0]=''
                    if(req[col][0]!=''):
                        dic[col]=req[col][0]
            print(req)

        if('Weight' in dic and 'Height' in dic):
            dic['StateofOverWeight']=round(float(float(dic['Weight'])*float(dic['Weight']))/float(dic['Height']),2)
        if('DateofJoiningShip' in dic):
            dateofjoiningship = dic['DateofJoiningShip']
            if('PresentEngagement' in dic and dic['PresentEngagement'] != '-'):
                presentengagement = Present_Engagement.index(dic['PresentEngagement']) - 1
                if('ServiceCategory' in dic and dic['ServiceCategory'] != '-'):
                    servicecategory = Service_Category.index(dic['ServiceCategory']) - 1
                    dateofjoiningship = datetime.strptime(dateofjoiningship,'%Y-%m-%d')
                    dic['NextREEngagementDue']=calculateReEngagement(dateofjoiningship,presentengagement,servicecategory)
                    dic['NextREEngagementDue'] = dic['NextREEngagementDue'].strftime("%Y-%m-%d")       
        if('EffectivedateofexistingGCB' in dic):
            effectivedateofexistinggcb = dic['EffectivedateofexistingGCB']
            effectivedateofexistinggcb = datetime.strptime(effectivedateofexistinggcb,'%Y-%m-%d')
            dic['DateofNextGCB'] = addyearmonth(effectivedateofexistinggcb,4,0)
            dic['DateofNextGCB'] = dic['DateofNextGCB'].strftime("%Y-%m-%d")
            print(dic['DateofNextGCB'])

        if('DateofJoiningShip' in dic):
            DateofJoiningShip = dic['DateofJoiningShip']
            DateofJoiningShip = datetime.strptime(DateofJoiningShip,'%Y-%m-%d')
            dic['DateofNextIncrement'] = addyearmonth(DateofJoiningShip,0,11)
            dic['DateofNextIncrement'] = dic['DateofNextIncrement'].strftime("%Y-%m-%d")
        try:
            mcur = mysql.connection.cursor()
            query = "UPDATE Sailor SET "
            first = True
            print(dic)
            for col in Column:
                if col in dic:
                    if first == False:
                        query += ", "
                    first = False
                    query += col + "=" + "%s"
            query += " WHERE O_No = %s"
            param = ()
            for col in Column:
                if col in dic:
                    param = param +( dic[col], )
            param = param + (dic['O_No'], )
            mcur.execute(query, param)
            mysql.connection.commit()
            mcur.close()
            ret = []
            req = request.form
            mcur = mysql.connection.cursor()
            mcur.execute("DELETE FROM Sibling WHERE O_No = %s", (req['O_No'],))
            mcur.connection.commit()
            mcur.close()
            mcur = mysql.connection.cursor()
            mcur.execute("DELETE FROM Children WHERE O_No = %s", (req['O_No'],))
            mcur.connection.commit()
            mcur.close()
            mcur = mysql.connection.cursor()
            for i in range(1,100):
                id1 = 'SiblingName' + str(i)
                id2 = 'SiblingMobileNo' + str(i)
                id3 = 'SiblingAddress' + str(i)
                if id1 in req:
                    if (req[id1] is None and req[id2] is None and req[id3] is None) or( req[id1] == '' and req[id2] == '' and req[id3] == ''):
                        pass
                    else:
                        mcur.execute("INSERT INTO Sibling (SiblingName,SiblingMobileNo,SiblingAddress,O_No) VALUES (%s,%s,%s,%s)",(req[id1],req[id2],req[id3],req['O_No']))
                        ret.append((req[id1], req[id2], req[id3]))
            mysql.connection.commit()
            mcur.close()

            ret = []
            req = request.form
            mcur = mysql.connection.cursor()
            for i in range(1,100):
                id1 = 'ChildrenName' + str(i)
                id2 = 'DOBofChildren' + str(i)
                id3 = 'Anyspecialinfochildren' + str(i)
                if id1 in req:
                    if (req[id1] is None and req[id2] is None and req[id3] is None) or( req[id1] == '' and req[id2] == '' and req[id3] == ''):
                        pass
                    else:
                        mcur.execute("INSERT INTO Children (ChildrenName,DOBofChildren,Anyspecialinfochildren,O_No) VALUES (%s,%s,%s,%s)",(req[id1],req[id2],req[id3],req['O_No']))
                        ret.append((req[id1], req[id2], req[id3]))
            mysql.connection.commit()
            mcur.close()
        except:
            return "Can't Update"
        return redirect(url_for('profile', id = id))
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/TyHistory')
def tyhistory(id):
    if('O_No' in session):
        login_status = True
        cur = mysql.connection.cursor()
        cur.execute('select * from TY where O_No = %s',(id, ))
        rows = cur.fetchall()
        ret = []
        #idx, fromty, toty , tybillet , purpose , duration , securityclearence , O_No
        today = date.today()
        for row in rows:
            temp = {}
            temp['idx'] = row[0]
            temp['fromty'] = row[1]
            temp['toty'] = row[2]
            temp['tybillet'] = row[3]
            temp['purpose'] = row[4]
            temp['duration'] = row[5]
            temp['securityclearence'] = row[6]
            temp['O_No'] = row[7]
            temp['TotalDuration'] = '0'
            if temp['toty'] is None or temp['toty'] == '':
                #today to from dif
                today = str(today)
                d1 = datetime.strptime(today, "%Y-%m-%d")
                print(temp['fromty'])
    
                d2 = datetime.strptime(temp['fromty'], "%Y-%m-%d")
                dif = abs((d2 - d1).days) 
                temp['TotalDuration'] = dif
            else:
                #to to from dif i
                d1 = datetime.strptime(temp['toty'], "%Y-%m-%d")
                d2 = datetime.strptime(temp['fromty'], "%Y-%m-%d")
                dif = abs((d2 - d1).days)
                temp['TotalDuration'] = dif

            if temp['toty'] is None or temp['toty'] == '':
                temp['Button'] = True
            ret.append(temp)

        return render_template('tyhistory.html', rows = ret, login_status = login_status, id = id )
    else:
        login_status = False
        return redirect(url_for('home'))
    
@app.route('/profile/<string:id>/TyHistory/completety/<int:idx>')
def completety(id, idx):
    today = date.today()
    if('O_No' in session):
        login_status = True
        try:
            mcur = mysql.connection.cursor()
            #mcur.execute("UPDATE UserInfo SET O_No=%s, usertype=%s, pass=%s, name=%s, Branch=%s, Rank=%s, MobileNo_1=%s, MobileNo_2=%s, DateofBirth=%s, PresentAddress=%s, PermanentAddress=%s, marrital_status=%s, DateofMarriage=%s, ServiceIdCardNo=%s, NIDCardNo=%s, DrivingLicenseNo=%s, BloodGroup=%s, LastDateofBloodDonation=%s, Height=%s, Weight=%s, StateofOverWeight=%s, FacebookAccount=%s, Emailaddress=%s, home_district=%s, NextofKin=%s, Relationship=%s, ContactNumberofNextofKin=%s, NameofWife=%s, AddressofWife=%s, MobileNo=%s, Anyspecialinfowife=%s, ChildrenNumber=%s, ChildrenName=%s, DOBofChildren=%s, Anyspecialinfochildren=%s, FathersName=%s, FathersMobileNo=%s,FathersAddress=%s, MothersName=%s, MothersMobileNo=%s, MothersAddress=%s, FamilyCrisis=%s, SiblingNumber=%s, BrothersName=%s, BrothersMobileNo=%s, BrothersAddress=%s, highestEducation=%s, OngoingcivilEducation=%s, DateofJoiningService=%s, ServiceCategory=%s, Medicalcategory=%s, DateofLastPromotion=%s, DateofNextPromotion=%s, PresentEngagement=%s, NextREEngagementDue=%s, DateofNextIncrement=%s, NumberofGCB=%s, EffectivedateofexistingGCB=%s,DateofNextGCB=%s,DateofJoiningShip=%s, NameofShip=%s, UNMission=%s, GoodWillMission=%s, DAONumber=%s, PLeaveAvailed=%s, LastDateofPL=%s, PLeaveDue=%s , RecreationLeaveDue=%s, CLeaveAvailed=%s, CLeaveDue=%s, SickLeave=%s, ExBangladeshLeave=%s, Rl=%s, Sourceofdebt=%s, Amountofdebt=%s, ADOsRemark=%s, DivisionalOfficersRemark=%s, COsSpecialRemark=%s, AreaCommanderRemark=%s, ChoiceofAreaForPosting=%s, ChoiceofNextAppointment=%s, NameofImportantCourses=%s, NameofNextCourse=%s, ForeignCourse=%s, SpecialQualification=%s, ChoiceofNextCourse=%s, DateofProceedinginTyDuty=%s, TyBillet=%s, PurposetofTy=%s, TyDuration=%s, IfNotReturn=%s, DateofreturnfromTY=%s, TotalTyDuration=%s, TyHistorySummary=%s, DateoflastSecurityClearance=%s, ExtraCurricularActivities=%s, GamesAndSports=%s WHERE O_No=%s" ,(dic['O_No'],dic['usertype'],dic['pass'],dic['name'],dic['Branch'],dic['Rank'],dic['MobileNo_1'],dic['MobileNo_2'],dic['DateofBirth'],dic['PresentAddress'],dic['PermanentAddress'],dic['marrital_status'],dic['DateofMarriage'],dic['ServiceIdCardNo'],dic['NIDCardNo'],dic['DrivingLicenseNo'],dic['BloodGroup'],dic['LastDateofBloodDonation'],dic['Height'],dic['Weight'],dic['StateofOverWeight'],dic['FacebookAccount'],dic['Emailaddress'],dic['home_district'],dic['NextofKin'],dic['Relationship'],dic['ContactNumberofNextofKin'],dic['NameofWife'],dic['AddressofWife'],dic['MobileNo'],dic['Anyspecialinfowife'],dic['ChildrenNumber'],dic['ChildrenName'],dic['DOBofChildren'],dic['Anyspecialinfochildren'],dic['FathersName'],dic['FathersMobileNo'],dic['FathersAddress'],dic['MothersName'],dic['MothersMobileNo'],dic['MothersAddress'],dic['FamilyCrisis'],dic['SiblingNumber'],dic['BrothersName'],dic['BrothersMobileNo'],dic['BrothersAddress'],dic['highestEducation'],dic['OngoingcivilEducation'],dic['DateofJoiningService'],dic['ServiceCategory'],dic['Medicalcategory'],dic['DateofLastPromotion'],dic['DateofNextPromotion'],dic['PresentEngagement'],dic['NextREEngagementDue'],dic['DateofNextIncrement'],dic['NumberofGCB'],dic['EffectivedateofexistingGCB'],dic['DateofNextGCB'],dic['DateofJoiningShip'],dic['NameofShip'],dic['UNMission'],dic['GoodWillMission'],dic['DAONumber'],dic['PLeaveAvailed'],dic['LastDateofPL'],dic['PLeaveDue'],dic['RecreationLeaveDue'],dic['CLeaveAvailed'],dic['CLeaveDue'],dic['SickLeave'],dic['ExBangladeshLeave'],dic['Rl'],dic['Sourceofdebt'],dic['Amountofdebt'],dic['ADOsRemark'],dic['DivisionalOfficersRemark'],dic['COsSpecialRemark'],dic['AreaCommanderRemark'],dic['ChoiceofAreaForPosting'],dic['ChoiceofNextAppointment'],dic['NameofImportantCourses'],dic['NameofNextCourse'],dic['ForeignCourse'],dic['SpecialQualification'],dic['ChoiceofNextCourse'],dic['DateofProceedinginTyDuty'],dic['TyBillet'],dic['PurposetofTy'],dic['TyDuration'],dic['DateofreturnfromTY'] ,dic['IfNotReturn'],dic['TotalTyDuration'],dic['TyHistorySummary'],dic['DateoflastSecurityClearance'],dic['ExtraCurricularActivities'],dic['GamesAndSports'], id))
            mcur.execute("UPDATE TY SET toty = %s WHERE idx = %s", (str(today), idx, ))
            mysql.connection.commit()
            mysql.connection.commit()
            mcur.close()
        except:
            pass
        return redirect(url_for('tyhistory', id = id, login_status = login_status))
    else:
        login_status = False
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/TyHistory/adding_ty', methods = ['POST', 'GET'])
def adding_ty(id):
    if 'O_No' in session:
        if request.method =='POST':
            try:
                req = request.form
                mcur = mysql.connection.cursor()
                mcur.execute("insert into TY (fromty, toty , tybillet , purpose , duration , securityclearence , O_No) values (%s, %s, %s, %s, %s, %s, %s)", (req['fromty'], req['toty'], req['tybillet'], req['purpose'], req['duration'], req['securityclearence'], id,))
                mysql.connection.commit()
                mcur.close()
            except:
                pass
            return redirect(url_for('tyhistory', id = id))
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/LeaveHistory/adding_leave', methods = ['POST', 'GET'])
def adding_leave(id):
    if 'O_No' in session:
        if request.method =='POST':
            try:
                req = request.form
                mcur = mysql.connection.cursor()
                mcur.execute("insert into LeaveHistory (type, froml , tol , O_No ) values (%s, %s, %s, %s)", (req['type'], req['froml'], req['tol'], id,))
                mysql.connection.commit()
                mcur.close()
            except:
                pass
            return redirect(url_for('leavehistory', id = id))
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/LeaveHistory')
def leavehistory(id):
    if('O_No' in session):
        cur = mysql.connection.cursor()
        cur.execute('select DateofJoiningService from Sailor where O_No = %s',(id, ))
        rows_cur = cur.fetchall()
        cur.execute('select * from LeaveHistory where O_No = %s',(id, ))
        print("date: ")
        print(session['O_No'])
        print(rows_cur)
        print("hello")
        if rows_cur[0][0] is None:
            rows_cur[0][0]=''
        if(rows_cur[0][0]==""):
            print("Here")
            servicejoindate = "NONE"
        else:
            servicejoindate = str(rows_cur[0][0])
        print("sjskfjs: ",servicejoindate)
        rows = cur.fetchall()
        ret = []
        extra = {}
        extra['P Leave Availed'] = 0
        extra['P Due'] = 60
        extra['Recreation Leave'] = 0
        extra['Recreation Leave Due'] = 0
        extra['C Leave Availed'] = 0
        extra['C Leave Due'] = 20
        if servicejoindate=="NONE" :
            extra['Recreation Leave Due'] = "N/A"
        else:
            temp = datetime.strptime(servicejoindate,'%Y-%m-%d')
            temp = addyearmonth(temp,3,0)
            extra['Recreation Leave Due']=str(temp.strftime('%Y-%m-%d'))
        print(extra)
        for row in rows:
            temp = {}
            temp['idx'] = row[0]
            temp['type'] = row[1]
            temp['froml'] = row[2]
            temp['tol'] = row[3]
            d1 = datetime.strptime(temp['tol'], "%Y-%m-%d")
            d2 = datetime.strptime(temp['froml'], "%Y-%m-%d")
            dif = abs((d2 - d1).days)
            temp['duration'] = dif
            ret.append(temp)
            
            if row[1] == 'P Leave':
                extra['P Leave Availed'] += dif
            if row[1] == 'C Leave':
                extra['C Leave Availed'] += dif
            if row[1] == 'Recreation Leave':
                extra['Recreation Leave'] = 0
            
            extra['C Leave Due'] = 20 - extra['C Leave Availed']
            extra['Recreation Leave Due'] =  0
            extra['P Due'] = 60 - extra['P Leave Availed']


        return render_template('leavehistory.html',rows =ret,Leave_Category = Leave_Category, login_status = True, id = id, extra = extra)
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/Remarks')
def remarks(id):
    if 'O_No' in session:
        cur = mysql.connection.cursor()
        cur.execute("Select idx, O_No_to, O_No_from, remarks, date, Branch, Rank, name from ADO_Remark join ADO ON O_No_from = O_No WHERE O_No_to = %s ORDER BY idx DESC", (id,))
        ADO_Remark = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("Select idx, O_No_to, O_No_from, remarks, date, Branch, Rank, name from DO_Remark join Divisional ON O_No_from = O_No WHERE O_No_to = %s ORDER BY idx DESC", (id,))
        
        #cur.execute("Select * from DO_Remark WHERE O_No_to = %s ORDER BY idx DESC", (id,))
        DO_Remark = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("Select idx, O_No_to, O_No_from, remarks, date, Branch, Rank, name from CO_Remark join Commanding ON O_No_from = O_No WHERE O_No_to = %s ORDER BY idx DESC", (id,))
        
        #cur.execute("Select * from CO_Remark WHERE O_No_to = %s ORDER BY idx DESC", (id,))
        CO_Remark = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("Select idx, O_No_to, O_No_from, remarks, date, Branch, Rank, name from Area_Remark join Comflot ON O_No_from = O_No WHERE O_No_to = %s ORDER BY idx DESC", (id,))
        
        #cur.execute("Select * from Area_Remark WHERE O_No_to = %s ORDER BY idx DESC", (id,))
        Area_Remark = cur.fetchall()
        cur.close()

        return render_template('remarks.html', login_status = True, id = id, rowsado = ADO_Remark, rowsdo = DO_Remark, rowsco = CO_Remark, rowsarea = Area_Remark)
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/Remarks/updateremark/<string:postid>/<string:admintype>', methods = ['POST', 'GET'])
def updateremark(id, postid, admintype):
    if 'O_No' in session:
        if request.method == 'POST':
            req = request.form.to_dict(flat=False)
            mcur = mysql.connection.cursor()
            if admintype == '1':
                mcur.execute('UPDATE ADO_Remark SET remarks = %s WHERE idx = %s', (req['remarkado'][0], postid, ))
            if admintype == '2':
                mcur.execute('UPDATE DO_Remark SET remarks = %s WHERE idx = %s', (req['remarkdo'][0], postid, ))
            if admintype == '3':
                mcur.execute('UPDATE CO_Remark SET remarks = %s WHERE idx = %s', (req['remarkco'][0], postid, ))
            if admintype == '5':
                mcur.execute('UPDATE Area_Remark SET remarks = %s WHERE idx = %s', (req['remarkarea'][0], postid, ))
            
            mysql.connection.commit()
            mcur.close()
                
            return redirect(url_for('remarks', id = id))
    return redirect(url_for('home'))

@app.route('/profile/<string:id>/Remarks/posting', methods = ['POST', 'GET'])
def posting(id):        
    if('O_No' in session):
        if request.method == 'POST':
            try:
                req = request.form
                today = date.today()
                mcur = mysql.connection.cursor()
                if session['usertype'] == '1':
                    remarktext = req['remarkado']
                    mcur.execute("INSERT INTO ADO_Remark (O_No_to, O_No_from, remarks, date) values (%s, %s, %s, %s)",(id, session['O_No'], remarktext, today,))
                if session['usertype'] == '2':
                    remarktext = req['remarkdo']
                    mcur.execute("INSERT INTO DO_Remark (O_No_to, O_No_from, remarks, date) values (%s, %s, %s, %s)",(id, session['O_No'], remarktext, today,))
                if session['usertype'] == '3':
                    remarktext = req['remarkco']
                    mcur.execute("INSERT INTO CO_Remark (O_No_to, O_No_from, remarks, date) values (%s, %s, %s, %s)",(id, session['O_No'], remarktext, today,))
                if session['usertype'] == '5':
                    remarktext = req['remarkarea']
                    mcur.execute("INSERT INTO Area_Remark (O_No_to, O_No_from, remarks, date) values (%s, %s, %s, %s)",(id, session['O_No'], remarktext, today,))
                mysql.connection.commit()
                mcur.close()
            except:
                pass
            return redirect(url_for('remarks', id = id))
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/Evaluation')
def evaluation(id):
    if 'O_No' in session:
        cur = mysql.connection.cursor()
        cur.execute('select * from Evaluation where O_No = %s',(id, ))
        rows = cur.fetchall()
        ret1 = [[] for i in range(13)]
        ret2 = [[] for i in range(13)]
        current_year = datetime.today().year
        
        for row in rows:
            temp = {}
            temp['idx'] = row[0]
            temp['dateofevaluation'] = row[1]
            date_object = datetime.strptime(temp['dateofevaluation'], '%Y-%m-%d').date()
            eva_year = date_object.year
            month = date_object.month
            temp['nameoftask'] = row[2]
            temp['performance'] = row[3]
            temp['achivementpoint'] = row[4]
            temp['special'] = row[5]
            temp['duration'] = row[6]
            temp['O_No'] = id
            if(eva_year==current_year):
                ret1[month].append(temp)
            elif(eva_year==current_year-1):
                ret2[month].append(temp)


        prevavg = [0]
        totalsum = 0
        totalcnt = 0
        for m in range(1, 13):
            sum = 0
            cnt = 0
            for row in ret2[m]:
                sum += int(row['achivementpoint'])
                cnt = cnt + 1
            totalsum += sum
            totalcnt += cnt
            if cnt == 0:
                prevavg.append(0)
            else:
                sum = sum / cnt
                prevavg.append(round(sum, 2))
        print(totalsum, totalcnt)
        if totalcnt == 0:
            prevavg.append(0)
        else:
            prevavg.append(round(totalsum/totalcnt, 2))


        curavg = [0]
        totalsum = 0
        totalcnt = 0
        for m in range(1, 13):
            sum = 0
            cnt = 0
            for row in ret1[m]:
                sum += int(row['achivementpoint'])
                cnt = cnt + 1
            totalsum += sum
            totalcnt += cnt
            if cnt == 0:
                curavg.append(0)
            else:
                sum = sum / cnt
                x = round(sum, 2)
                print(x)
                curavg.append(x)
        if totalcnt == 0:
            curavg.append(0)
        else:
            curavg.append(round(totalsum/totalcnt, 2))
        
        return render_template('monthlyevaluation.html',login_status=True,id=id, cur = ret1, prev = ret2, prevavg = prevavg, curavg = curavg, )
    else:
        return redirect(url_for('home'))

@app.route('/profile/<string:id>/Evaluation/adding_monthly', methods = ['POST', 'GET'])
def adding_monthly(id):
    if 'O_No' in session:
        if request.method == 'POST':
            try:
                req = request.form
                mcur = mysql.connection.cursor()
                mcur.execute("insert into Evaluation (dateofevaluation, nameoftask , performance ,achivementpoint, special , O_No) values (%s, %s, %s, %s, %s, %s)", (req['dateofevaluation'], req['nameoftask'], req['performance'],req['achivementpoint'], req['special'], id,))
                mysql.connection.commit()
                mcur.close()
            except:
                pass
            return redirect(url_for('evaluation', id = id))

    else:
        return redirect(url_for('home'))

@app.route('/search/SailorDataSearch', methods = ['POST', 'GET'])
def SailorDataSearch():
    if 'O_No' in session:
        login_status = True
        if request.method == 'POST':
            req = {}
            req['Rank'] = '- - -'
            req['Branch'] = '- - -'
            req = request.form.to_dict(flat=False)
            if 'Rank' not in req:
                req['Rank'] = ['- - -']
            if 'Branch' not in req:
                req['Branch'] = ['- - -']
                 
            if req['Branch'] == ['- - -']:
                req['Branch'] = ['']
            if req['Rank'] == ['- - -']:
                req['Rank'] = ['']

            e_list = eligiblelist_to_dictionary(eligiblelist())
            # print(req)
            result = []
            for row in e_list:
                ok = True
                
                for key in req:
                    if row[key] is None or row[key] == '':
                        row[key] = ''

                    if req[key][0].lower() not in row[key].lower():
                        ok = False
                        break
                if ok == True:
                    result.append(row)
            result = eligiblelist_to_list(result)
            return render_template("show.html",static_on = 0, rows = result,login_status=login_status)
        else:
            return redirect(url_for('search'))
    else:
        login_status = False
        return redirect(url_for('home'))

@app.route('/search/BloodDonationSearch', methods = ['POST', 'GET'])
def BloodDonationSearch():
    if 'O_No' in session:
        login_status = True
        if request.method == 'POST':
            req = request.form.to_dict(flat=False)
            print(req)
            for key in req:
                if req[key] == ['-']:
                    req[key] = ['']
            e_list = eligiblelist_to_dictionary(eligiblelist())
            result = []
            for row in e_list:
                ok = True
                for key in req:
                    if row[key] is None:
                        row[key] = ''
                
                #bloodgroup
                if req['BloodGroup'][0] != '':
                    if req['BloodGroup'][0] != row['BloodGroup']:
                        ok = False 
                #last date
                if req['LastDateofBloodDonation'][0] != '':
                    curdate = ''
                    for c in req['LastDateofBloodDonation'][0]:
                        if c != '-':
                            curdate += c
                    lastdate = ''
                    if row['LastDateofBloodDonation'] is None or row['LastDateofBloodDonation'] == '':
                        lastdate = str(int(curdate) + 1)
                    else:
                        for c in row['LastDateofBloodDonation']:
                            if c != '-':
                                lastdate += c
                    
                    print(int(lastdate) - int(curdate))
                    if int(lastdate) - int(curdate) > 0:
                        ok = False
                #category
                if req['Medicalcategory'][0] != '':
                    if req['Medicalcategory'][0] != row['Medicalcategory']:
                        ok = False
                if ok == True:
                    result.append(row)
            result = eligiblelist_to_list(result)
            print(result)
            return render_template("show.html",static_on = 0, rows = result,login_status=login_status)
    else:
        login_status = False
        return redirect(url_for('home'))

@app.route('/search/SelectPersonnelForTY',methods = ['POST','GET'])
def SelectPersonnelForTY():
    if 'O_No' in session:
        login_status = True
        if request.method == 'POST':
            req = request.form.to_dict(flat=False)
            for key in req:
                if req[key] == ['-']:
                    req[key] = ['']
            print(req)
            e_list = eligiblelist_to_dictionary(eligiblelist())
            # print(e_list)
            result = []
            for row in e_list: 
                ok = True
                if row['Branch'] is None:
                    row['Branch'] = ''
                if row['Rank'] is None:
                    row['Rank'] = ''
                if row['Height'] is None:
                    row['Height'] = ''
                if row['SpecialQualification'] is None:
                    row['SpecialQualification'] = ''
                if row['NameofImportantCourses'] is None:
                    row['NameofImportantCourses'] = ''
                if row['ForeignCourse'] is None:
                    row['ForeignCourse'] = ''
                if row['Medicalcategory'] is None:
                    row['Medicalcategory'] = ''
                if req['Branch'][0] =='- - -':
                    req['Branch'][0]=''
                if req['Branch'][0]!= '':
                    print(req['Branch'][0],"   ",row['Branch'])
                    if req['Branch'][0]!= row['Branch']:
                        ok = False
                    if 'Rank' in req:
                        if req['Rank'][0]=='- - -':
                            req['Rank'][0] = ''
                        if req['Rank'][0] != '':
                            if req['Rank'][0] != row['Rank']:
                                ok = False
                print("before: ",ok)
                if req['Height'][0]!='':
                    row_height = row['Height']
                    if(row_height==''):
                        row_height = 0
                    else:
                        row_height = int(row_height)
                    req_height = req['Height'][0]
                    if int(req_height) > row_height :
                        ok = False 
                print("After Height: ",ok)  
                if req['Medicalcategory'][0]!='':
                    if row['Medicalcategory'] != req['Medicalcategory'][0]:
                        ok = False   
                print("after medi: ",ok) 
                if req['Course'][0]!='':
                    if (req['Course'][0].lower() not in row['NameofImportantCourses'].lower()) or (req['Course'][0].lower() not in row['ForeignCourse'].lower()):
                        ok = False
                print("After Course: ",ok)
                if req['SpecialQualification'][0]!='':
                    if req['SpecialQualification'][0].lower() not in row['SpecialQualification'].lower():
                        ok = False
                temp_id = row['O_No']
                cur = mysql.connection.cursor()
                sql_select_query = """select * from TY where O_No = %s"""
                cur.execute(sql_select_query, (temp_id,))
                rows = cur.fetchall()
                l = len(rows)
                print("l     :         ",l)
                cnt = 0
                for r in rows:
                    if r[1] is None:
                        r[1]=''
                    if req['DateoflastTY'][0]!='':
                        if req['DateoflastTY'][0]!=r[1]:
                            print(req['DateoflastTY'])
                            cnt+=1
                print(cnt)
                
                if cnt == l:
                    ok = False
                print("After Date of Last TY: ",ok)
                cnt = 0
                for r in rows:
                    if r[6] is None:
                        r[6]=''
                    if req['LastDateofSecurityClearance'][0]!='':
                        if req['LastDateofSecurityClearance'][0]!= r[6]:
                            cnt+=1
                print(cnt,"         ",l)
                if cnt == l:
                    ok = False
                print("After Security Clearance: ",ok)
                cnt = 0
                for r in rows:
                    if req['Exclusion'][0]!='':
                        req_date = str(req['Exclusion'][0])
                        intdate=''
                        for i in range(len(req_date)):
                            if req_date[i]!='-':
                                intdate+=req_date[i]
                        intdate=int(intdate)
                        if r[1] is '' or r[2] is '':
                            cnt+=1
                        else:
                            from_date = r[1]
                            to_date = r[2]
                            f=''
                            t=''
                            for i in range(len(from_date)):
                                if from_date[i]!='-':
                                    f+=from_date[i]
                            f=int(f)
                            for i in range(len(to_date)):
                                if to_date[i]!='-':
                                    t+=to_date[i]
                            t=int(t)
                            if (f>intdate) or (t>intdate):
                                cnt+=1
                            print(f,"                 ",t)
                if cnt == l:
                    ok = False
                if ok == True:
                    result.append(row)
            cur.close()
            result = eligiblelist_to_list(result)
            return render_template("show.html",static_on = 0,rows = result,login_status = login_status)
    else:
        login_status = False
        return redirect(url_for('home'))

@app.route('/search/NoOfDaysatSea',methods = ['POST','GET'])
def NoOfDaysatSea():
    if 'O_No' in session:
        if request.method == 'POST':
            req = request.form.to_dict(flat=False)
            print(req)
            for key in req:
                if req[key] == ['-']:
                    req[key] = ['']
            e_list = eligiblelist_to_dictionary(eligiblelist())
            result = []
            # print(e_list)
            for row in e_list:
                if row['Rank']=='OD' or row['Rank'] == 'AB':   
                    ok = True
                    for key in req:
                        if row[key] is None:
                            row[key] = ''
                    if req['NameofShip'][0] != '':
                        if req['NameofShip'][0] != row['NameofShip']:
                            ok = False 
                    if ok == True:
                        result.append(row)
            result = eligiblelist_to_list(result)
            # print(result)
            return render_template("show.html",static_on = 0, rows = result)
    else:
        return redirect(url_for('home'))

@app.route('/search/TYMovement',methods = ['POST','GET'])
def TYMovement():
    if 'O_No' in session:
        login_status = True
        if request.method == 'POST':
            req = request.form.to_dict(flat=False)
            for key in req:
                if req[key] == ['-']:
                    req[key] = ['']
            print(req)
            e_list = eligiblelist_to_dictionary(eligiblelist())
            # print(e_list)
            result = []
            for row in e_list: 
                ok = True
                if row['Branch'] is None:
                    row['Branch'] = ''
                if row['Rank'] is None:
                    row['Rank'] = ''
                if req['Branch'][0] =='- - -':
                    req['Branch'][0]=''
                if req['Branch'][0] != '':
                    print(req['Branch'][0])
                    if req['Rank'][0]=='- - -':
                        req['Rank'][0] = ''
                    if req['Branch'][0] != row['Branch']:
                        ok = False
                    if 'Rank' in req:
                        if req['Rank'][0] != '':
                            if req['Rank'][0] != row['Rank']:
                                ok = False
                temp_id = row['O_No']
                cur = mysql.connection.cursor()
                sql_select_query = """select * from TY where O_No = %s"""
                cur.execute(sql_select_query, (temp_id,))
                rows = cur.fetchall()
                l = len(rows)
                cnt = 0
                for r in rows:
                    if r[5] is None:
                        r[5]=''
                    if req['duration'][0] !='':
                        print("duration: ",req['duration'][0],type(req['duration'][0]))
                        if int(req['duration'][0]) <= int(r[5]):
                            cnt = cnt+1
                if cnt == 0 and req['duration'][0]!='':
                    ok = False
                if req['totalnooftymovement'][0]!='':
                    if int(req['totalnooftymovement'][0])>l:
                        ok = False
                if ok == True:
                    result.append(row)
            cur.close()
            result = eligiblelist_to_list(result)
            return render_template("show.html",static_on = 0, rows = result,login_status = login_status)
    else:
        login_status = False
        return redirect(url_for('home'))
        
@app.route('/search')
def search():
    if 'O_No' in session:
        if('O_No' in session):
            login_status = True
        else:
            login_status = False
        return render_template("search.html",Name_of_Ship = Name_of_Ship ,Blood_Group = Blood_Group,Medical_Category = Medical_Category,login_status=login_status,Branch_key = Branch, Branch = json.dumps(Branch))
    else:
        return redirect(url_for('home'))

@app.route('/search_result',methods=['POST','GET'])
def search_result():
    if('O_No' in session):
        login_status = True
    else:
        login_status = False
        return redirect(url_for('home'))
    if request.method == 'POST':
        result = request.form
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        usertype = int(session['usertype'])
    
        if(usertype == 0):
            cur.execute('SELECT * from UserInfo')
        elif(usertype==3):
            cur.execute('SELECT NameofShip from UserInfo where O_No = ?',[session['O_No']])
            temp = cur.fetchall()
            ans = 0 
            for row in temp:
                ans = row['NameofShip']
            cur.execute('SELECT * from UserInfo where NameofShip = ? ',[ans])
        temp = cur.fetchall()
        #print(result)
        name = result['name']
        shipname = result['shipname']
        O_No = result['O_No']
        cur.close()
        con.close()
        #print(temp)
        l = []
        for row in temp:
            ans_ship_name=row['NameofShip']
            ans_name = row['name']
            ans_O_No = row['O_No']
            if(name!='' and shipname!='' and O_No!=''):
                if(name==ans_name and shipname == ans_ship_name and O_No==ans_O_No):
                    l.append(row['O_No'])
            elif(name!='' and shipname!='' and O_No==''):
                if(name==ans_name and shipname == ans_ship_name):
                    l.append(row['O_No'])
            elif(name!='' and shipname=='' and O_No!=''):
                if(name==ans_name and O_No==ans_O_No):
                    l.append(row['O_No'])
            elif(name!='' and shipname=='' and O_No==''):
                if(name==ans_name):
                    l.append(row['O_No'])
            elif(name=='' and shipname!='' and O_No!=''):
                if(shipname == ans_ship_name and O_No==ans_O_No):
                    l.append(row['O_No'])
            elif(name=='' and shipname!='' and O_No==''):
                if(shipname == ans_ship_name):
                    l.append(row['O_No'])
            elif(name=='' and shipname=='' and O_No!=''):
                if(O_No==ans_O_No):
                    l.append(row['O_No'])

    return render_template("search_result.html", rows = l,login_status=login_status)


@app.route('/debug')
def debug():
    return render_template('debug.html')

if __name__ == '__main__':
    app.secret_key = '123456'
    app.run(host='0.0.0.0',debug=True)