from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3 as sql
from flask_mysqldb import MySQL
import MySQLdb
from flask_fontawesome import FontAwesome
from datetime import datetime, timedelta
import time
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
User_Type = ['System Administrator', 'ADO', 'Divisional Officer', 'Commanding Officer', 'Staff Officer', 'Comflot']
Column = ['O_No' , 'usertype' , 'pass' , 'name' , 'Branch' , 'Rank' , 'MobileNo_1' , 'MobileNo_2' , 'DateofBirth' , 'PresentAddress' , 'PermanentAddress' , 'marrital_status' , 'DateofMarriage' , 'ServiceIdCardNo' , 'NIDCardNo' , 'DrivingLicenseNo' , 'BloodGroup' ,'LastDateofBloodDonation', 'Height' , 'Weight' , 'StateofOverWeight' , 'FacebookAccount' , 'Emailaddress' , 'home_district' , 'NextofKin' , 'Relationship' , 'ContactNumberofNextofKin' , 'NameofWife' , 'AddressofWife' , 'MobileNo' , 'Anyspecialinfowife' , 'ChildrenNumber' , 'ChildrenName' , 'DOBofChildren' , 'Anyspecialinfochildren' , 'FathersName' , 'FathersMobileNo' , 'FathersAddress' , 'MothersName' , 'MothersMobileNo' , 'MothersAddress' , 'FamilyCrisis' , 'SiblingNumber' , 'BrothersName' , 'BrothersMobileNo' , 'BrothersAddress' , 'highestEducation' , 'OngoingcivilEducation' , 'DateofJoiningService' , 'ServiceCategory' , 'Medicalcategory' , 'DateofLastPromotion' , 'DateofNextPromotion' , 'PresentEngagement' , 'NextREEngagementDue' , 'DateofNextIncrement' , 'NumberofGCB' , 'EffectivedateofexistingGCB' , 'DateofNextGCB' , 'DateofJoiningShip' , 'NameofShip' , 'UNMission' , 'GoodWillMission' , 'DAONumber' , 'PLeaveAvailed' , 'LastDateofPL' , 'PLeaveDue' , 'RecreationLeaveDue' , 'CLeaveAvailed' , 'CLeaveDue' , 'SickLeave' , 'ExBangladeshLeave' , 'Rl' , 'Sourceofdebt' , 'Amountofdebt' , 'ChoiceofAreaForPosting' , 'ChoiceofNextAppointment' , 'NameofImportantCourses' , 'NameofNextCourse' , 'ForeignCourse' , 'SpecialQualification' , 'ChoiceofNextCourse' , 'DateoflastSecurityClearance' , 'ExtraCurricularActivities' , 'GamesAndSports' , 'DateofProceedinginTyDuty' , 'TyBillet' , 'PurposetofTy' , 'TyDuration' , 'DateofreturnfromTY' , 'IfNotReturn' , 'TotalTyDuration' , 'TyHistorySummary' , 'ADOsRemark' , 'DivisionalOfficersRemark' , 'COsSpecialRemark' , 'AreaCommanderRemark']


#mysql database creation and connection
with app.app_context():
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'hello'
    cur = mysql.connection.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS navy")
    mysql.connection.commit()
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_DB'] = 'navy'
    cur.execute('use navy')
    #cur.execute('CREATE TABLE IF NOT EXISTS UserInfo ( O_No varchar(30) PRIMARY KEY, usertype int, pass text, name text, Branch int, Rank int, MobileNo_1 text, MobileNo_2 text, DateofBirth date, PresentAddress text, PermanentAddress text, marrital_status int, DateofMarriage date, ServiceIdCardNo text, NIDCardNo text, DrivingLicenseNo text, BloodGroup int, Height int, Weight int, StateofOverWeight text, FacebookAccount text, Emailaddress text, home_district int, NextofKin text, Relationship text, ContactNumberofNextofKin text, NameofWife text, AddressofWife text, MobileNo text, Anyspecialinfowife text, ChildrenNumber int, ChildrenName text, DOBofChildren date, Anyspecialinfochildren text, FathersName text, FathersMobileNo text, FathersAddress text, MothersName text, MothersMobileNo text, MothersAddress text, FamilyCrisis text, SiblingNumber int, BrothersName text, BrothersMobileNo text, BrothersAddress text, highestEducation int, OngoingcivilEducation int, DateofJoiningService date, ServiceCategory int, Medicalcategory int, DateofLastPromotion date, DateofNextPromotion date, PresentEngagement int, NextREEngagementDue date, DateofNextIncrement date, NumberofGCB int, EffectivedateofexistingGCB date, DateofNextGCB date, DateofJoiningShip date, NameofShip int, UNMission text, GoodWillMission text, DAONumber text, PLeaveAvailed int, LastDateofPL date, PLeaveDue int, RecreationLeaveDue date, CLeaveAvailed int, CLeaveDue int, SickLeave text, ExBangladeshLeave text, Rl text, Sourceofdebt text, Amountofdebt int, ChoiceofAreaForPosting int, ChoiceofNextAppointment int, NameofImportantCourses text, NameofNextCourse text, ForeignCourse text, SpecialQualification text, ChoiceofNextCourse text, DateoflastSecurityClearance date, ExtraCurricularActivities text, GamesAndSports text, DateofProceedinginTyDuty date, TyBillet text, PurposetofTy text, TyDuration int, DateofreturnfromTY date, IfNotReturn int, TotalTyDuration int, TyHistorySummary text, ADOsRemark text, DivisionalOfficersRemark text, COsSpecialRemark text, AreaCommanderRemark text ) ')
    #cur.execute('')


    cur.execute('CREATE TABLE IF NOT EXISTS UserInfo ( O_No varchar(30) PRIMARY KEY, usertype text, pass text, name text, Branch text, Rank text, MobileNo_1 text, MobileNo_2 text, DateofBirth text, PresentAddress text, PermanentAddress text, marrital_status text, DateofMarriage text, ServiceIdCardNo text, NIDCardNo text, DrivingLicenseNo text, BloodGroup text,LastDateofBloodDonation text, Height text, Weight text, StateofOverWeight text, FacebookAccount text, Emailaddress text, home_district text, NextofKin text, Relationship text, ContactNumberofNextofKin text, NameofWife text, AddressofWife text, MobileNo text, Anyspecialinfowife text, ChildrenNumber text, ChildrenName text, DOBofChildren text, Anyspecialinfochildren text, FathersName text, FathersMobileNo text, FathersAddress text, MothersName text, MothersMobileNo text, MothersAddress text, FamilyCrisis text, SiblingNumber text, BrothersName text, BrothersMobileNo text, BrothersAddress text, highestEducation text, OngoingcivilEducation text, DateofJoiningService text, ServiceCategory text, Medicalcategory text, DateofLastPromotion text, DateofNextPromotion text, PresentEngagement text, NextREEngagementDue text, DateofNextIncrement text, NumberofGCB text, EffectivedateofexistingGCB text, DateofNextGCB text, DateofJoiningShip text, NameofShip text, UNMission text, GoodWillMission text, DAONumber text, PLeaveAvailed text, LastDateofPL text, PLeaveDue text, RecreationLeaveDue text, CLeaveAvailed text, CLeaveDue text, SickLeave text, ExBangladeshLeave text, Rl text, Sourceofdebt text, Amountofdebt text, ChoiceofAreaForPosting text, ChoiceofNextAppointment text, NameofImportantCourses text, NameofNextCourse text, ForeignCourse text, SpecialQualification text, ChoiceofNextCourse text, DateoflastSecurityClearance text, ExtraCurricularActivities text, GamesAndSports text, DateofProceedinginTyDuty text, TyBillet text, PurposetofTy text, TyDuration text, DateofreturnfromTY text, IfNotReturn text, TotalTyDuration text, TyHistorySummary text, ADOsRemark text, DivisionalOfficersRemark text, COsSpecialRemark text, AreaCommanderRemark text ) ')
    try:
        cur.execute("INSERT INTO UserInfo(O_No, usertype , pass) VALUES (%s, %s, %s)", ("admin",0,'123456'))
    except:
        pass
    mysql.connection.commit()
    cur.close()
#mysql database creation end

@app.context_processor
def inject_user():
    id = ''
    if 'O_No' in session:
        id = session['O_No']
    return dict(user=id)


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

@app.route('/')
def home():
    if('O_No' in session):
        login_status = True
    else:
        login_status = False
    return render_template("index.html",login_status=login_status)

@app.route('/login_page')
def login_page():
    if 'O_No' in session:
        return redirect(url_for('home'))
    else:
        return render_template('login_page.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = request.form
        #mysql login 
        with app.app_context():
            app.config['MYSQL_USER'] = 'root'
            app.config['MYSQL_PASSWORD'] = 'hello'
            cur = mysql.connection.cursor()
            app.config['MYSQL_HOST'] = 'localhost'
            app.config['MYSQL_DB'] = 'navy'
            cur.execute('use navy')
            sql_select_query = """select * from UserInfo where O_No = %s"""
            cur.execute(sql_select_query, (result['O_No'],))
            rows = cur.fetchall()
            cur.close()
            dic=dict()
            for row in rows:
                for i in range(len(row)):
                    dic[Column[i]] = row[i]
            if dic['pass'] == result['password']:
                session['usertype'] = dic['usertype']
                session['O_No'] = result['O_No']
                return redirect(url_for('home'))
    return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    if 'O_No' in session:
        session.pop('O_No', None)
        session.pop('usertype', None)
        session['logged_in']=False
    return redirect(url_for('home'))


def eligiblelist():
    ret = []
    if('O_No' in session):
        if session['usertype'] == '0':
            with app.app_context():
                app.config['MYSQL_USER'] = 'root'
                app.config['MYSQL_PASSWORD'] = 'hello'
                cur = mysql.connection.cursor()
                app.config['MYSQL_HOST'] = 'localhost'
                app.config['MYSQL_DB'] = 'navy'
                cur.execute('use navy')
                sql_select_query = """select * from UserInfo"""
                cur.execute(sql_select_query)
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
        return render_template("show.html", rows = e_list,login_status=login_status)

    else:
        login_status = False

@app.route('/profile/<string:id>')
def profile(id):
    if('O_No' in session):
        login_status = True
    else:
        login_status = False
    e_list = eligiblelist()
    ok = False
    for row in e_list:
        if row[0] == id:
            ok = True
    if 'O_No' in session and ok == True:
        with app.app_context():
                app.config['MYSQL_USER'] = 'root'
                app.config['MYSQL_PASSWORD'] = 'hello'
                cur = mysql.connection.cursor()
                app.config['MYSQL_HOST'] = 'localhost'
                app.config['MYSQL_DB'] = 'navy'
                cur.execute('use navy')
                sql_select_query = """select * from UserInfo where O_No = %s"""
                cur.execute(sql_select_query, (id, ))
                rows = cur.fetchall()
                cur.close()
        usertype = int(session['usertype'])
        temprow = {}
        for i in range(len(rows[0])):
            #temprow.append(rows[0][i])
            temprow[Column[i]] = rows[0][i]
        return render_template('profile.html',Column = Column,usertype = usertype,rows=temprow,Name_of_Ship = Name_of_Ship, Medical_Category = Medical_Category,YesNo = YesNo,Home_District = Home_District, Marital_Status = Marital_Status,Branch_key = Branch, Branch = json.dumps(Branch), Blood_Group = Blood_Group, Highest_Education = Highest_Education, Ongoing_Education = Ongoing_Education, Service_Category = Service_Category, Present_Engagement = Present_Engagement, Number_of_GCB = Number_of_GCB, Choice_of_Area_for_drafting = Choice_of_Area_for_drafting, Choice_of_Next_Appointment = Choice_of_Next_Appointment, User_Type = User_Type, login_status=login_status)
    else:
        return redirect(url_for('home'))


@app.route('/adduser')
def adduser():
    if 'O_No' in session:
        if('O_No' in session):
            login_status = True
        else:
            login_status = False
        if int(session['usertype']) == 0:
            return render_template('adduser.html',Name_of_Ship = Name_of_Ship, Medical_Category = Medical_Category,YesNo = YesNo,Home_District = Home_District, Marital_Status = Marital_Status,Branch_key = Branch, Branch = json.dumps(Branch), Blood_Group = Blood_Group, Highest_Education = Highest_Education, Ongoing_Education = Ongoing_Education, Service_Category = Service_Category, Present_Engagement = Present_Engagement, Number_of_GCB = Number_of_GCB, Choice_of_Area_for_drafting = Choice_of_Area_for_drafting, Choice_of_Next_Appointment = Choice_of_Next_Appointment, User_Type = User_Type, login_status=login_status)
    return redirect(url_for('home'))


@app.route('/adduser/adding_user',methods=['POST','GET'])
def adding_user():
     if 'O_No' in session:
        if int(session['usertype']) == 0:
            if request.method =='POST':
                req = request.form.to_dict(flat=False)
                #print(req)
                dic=dict()
                for col in Column:
                    if col in req:
                        #print(req[col])
                        if(req[col][0]=='- - -'):
                            req[col][0]=''
                        if(req[col][0]!=''):
                            dic[col]=req[col][0]
                    
                    
            # cur.close()
            # print(len(dic))
            # print(dic)
            debug_var = 0
        # try:
            dic['StateofOverWeight']=0
            #nextreengagement calculation
            if('DateofJoiningShip' in dic):
                dateofjoiningship = dic['DateofJoiningShip']
                if('PresentEngagement' in dic):
                    presentengagement = int(dic['PresentEngagement'])
                    if('ServiceCategory' in dic):
                        servicecategory = int(dic['ServiceCategory'])
                        dateofjoiningship = datetime.strptime(dateofjoiningship,'%Y-%m-%d')
                        dic['NextREEngagementDue']=calculateReEngagement(dateofjoiningship,presentengagement,servicecategory)
                        dic['NextREEngagementDue'] = dic['NextREEngagementDue'].strftime("%Y-%m-%d")
            debug_var+=1        
            if('EffectivedateofexistingGCB' in dic):
                effectivedateofexistinggcb = dic['EffectivedateofexistingGCB']
                effectivedateofexistinggcb = datetime.strptime(effectivedateofexistinggcb,'%Y-%m-%d')
                dic['DateofNextGCB'] = addyearmonth(effectivedateofexistinggcb,4,0)
                dic['DateofNextGCB'] = dic['DateofNextGCB'].strftime("%Y-%m-%d")
                print(dic['DateofNextGCB'])
            debug_var+=1 
            if('PLeaveAvailed' in dic):
                PLeaveAvailed = dic['PLeaveAvailed']
                PLeaveDue = 60 - int(PLeaveAvailed)
                dic['PLeaveDue'] = PLeaveDue
            debug_var+=1 

            #RL Due Calculation
            if('DateofJoiningService' in dic):
                DateofJoiningService = dic['DateofJoiningService']
                DateofJoiningService = datetime.strptime(DateofJoiningService,'%Y-%m-%d')
                dic['RecreationLeaveDue'] = addyearmonth(DateofJoiningService,3,0)
                dic['RecreationLeaveDue'] = dic['RecreationLeaveDue'].strftime("%Y-%m-%d")
            debug_var+=1 

            #C leave due
            if('CLeaveAvailed' in dic):
                CLeaveAvailed = dic['CLeaveAvailed']
                dic['CLeaveDue'] = 20 - int(CLeaveAvailed)
            debug_var+=1 
            #Date of return from ty
            if('DateofProceedinginTyDuty' in dic):
                DateofProceedinginTyDuty = dic['DateofProceedinginTyDuty']
                if('TyDuration' in dic):
                    dic['DateofreturnfromTY'] = datetime.strptime(DateofProceedinginTyDuty,'%Y-%m-%d').date() + timedelta(days=int(dic['TyDuration']))
                    dic['DateofreturnfromTY'] = dic['DateofreturnfromTY'].strftime("%Y-%m-%d")
            debug_var+=1 
            if('TyDuration' in dic):
                tyduration = int(dic['TyDuration'])
                if('IfNotReturn' in dic):
                    ifnotreturn = dic['IfNotReturn']
                    if(ifnotreturn=="0"):
                        tyduration+=1
                    dic['TyDuration']=tyduration
            debug_var+=1 
            #date of next increment
            if('DateofJoiningShip' in dic):
                DateofJoiningShip = dic['DateofJoiningShip']
                DateofJoiningShip = datetime.strptime(DateofJoiningShip,'%Y-%m-%d')
                dic['DateofNextIncrement'] = addyearmonth(DateofJoiningShip,0,11)
                dic['DateofNextIncrement'] = dic['DateofNextIncrement'].strftime("%Y-%m-%d")
            debug_var+=1 

            for col in Column:
                if(col not in dic):
                    dic[col]=''
                else:
                    dic[col]=str(dic[col])
            
            conn = sql.connect("database.db")
            cur = conn.cursor()

            #main insert sqlite
            #cur.execute("INSERT INTO UserInfo (O_No , usertype , password , name , Branch , Rank , MobileNo_1 , MobileNo_2 , DateofBirth , PresentAddress , PermanentAddress , marrital_status , DateofMarriage , ServiceIdCardNo , NIDCardNo , DrivingLicenseNo , BloodGroup , Height , Weight , StateofOverWeight , FacebookAccount , Emailaddress , home_district , NextofKin , Relationship , ContactNumberofNextofKin , NameofWife , AddressofWife , MobileNo , Anyspecialinfowife , ChildrenNumber , ChildrenName , DOBofChildren , Anyspecialinfochildren , FathersName , FathersMobileNo , FathersAddress , MothersName , MothersMobileNo , MothersAddress , FamilyCrisis , SiblingNumber , BrothersName , BrothersMobileNo , BrothersAddress , highestEducation , OngoingcivilEducation , DateofJoiningService , ServiceCategory , Medicalcategory , DateofLastPromotion , DateofNextPromotion , PresentEngagement , NextREEngagementDue , DateofNextIncrement , NumberofGCB , EffectivedateofexistingGCB , DateofNextGCB , DateofJoiningShip , NameofShip , UNMission , GoodWillMission , DAONumber , PLeaveAvailed , LastDateofPL , PLeaveDue , RecreationLeaveDue , CLeaveAvailed , CLeaveDue , SickLeave , ExBangladeshLeave , Rl , Sourceofdebt , Amountofdebt , ADOsRemark , DivisionalOfficersRemark , COsSpecialRemark , AreaCommanderRemark , ChoiceofAreaForPosting , ChoiceofNextAppointment , NameofImportantCourses , NameofNextCourse , ForeignCourse , SpecialQualification , ChoiceofNextCourse , DateofProceedinginTyDuty , TyBillet , PurposetofTy , TyDuration , IfNotReturn , DateofreturnfromTY, TotalTyDuration , TyHistorySummary , DateoflastSecurityClearance , ExtraCurricularActivities , GamesAndSports) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (dic['O_No'],dic['usertype'],dic['password'],dic['name'],dic['Branch'],dic['Rank'],dic['MobileNo_1'],dic['MobileNo_2'],dic['DateofBirth'],dic['PresentAddress'],dic['PermanentAddress'],dic['marrital_status'],dic['DateofMarriage'],dic['ServiceIdCardNo'],dic['NIDCardNo'],dic['DrivingLicenseNo'],dic['BloodGroup'],dic['Height'],dic['Weight'],dic['StateofOverWeight'],dic['FacebookAccount'],dic['Emailaddress'],dic['home_district'],dic['NextofKin'],dic['Relationship'],dic['ContactNumberofNextofKin'],dic['NameofWife'],dic['AddressofWife'],dic['MobileNo'],dic['Anyspecialinfowife'],dic['ChildrenNumber'],dic['ChildrenName'],dic['DOBofChildren'],dic['Anyspecialinfochildren'],dic['FathersName'],dic['FathersMobileNo'],dic['FathersAddress'],dic['MothersName'],dic['MothersMobileNo'],dic['MothersAddress'],dic['FamilyCrisis'],dic['SiblingNumber'],dic['BrothersName'],dic['BrothersMobileNo'],dic['BrothersAddress'],dic['highestEducation'],dic['OngoingcivilEducation'],dic['DateofJoiningService'],dic['ServiceCategory'],dic['Medicalcategory'],dic['DateofLastPromotion'],dic['DateofNextPromotion'],dic['PresentEngagement'],dic['NextREEngagementDue'],dic['DateofNextIncrement'],dic['NumberofGCB'],dic['EffectivedateofexistingGCB'],dic['DateofNextGCB'],dic['DateofJoiningShip'],dic['NameofShip'],dic['UNMission'],dic['GoodWillMission'],dic['DAONumber'],dic['PLeaveAvailed'],dic['LastDateofPL'],dic['PLeaveDue'],dic['RecreationLeaveDue'],dic['CLeaveAvailed'],dic['CLeaveDue'],dic['SickLeave'],dic['ExBangladeshLeave'],dic['Rl'],dic['Sourceofdebt'],dic['Amountofdebt'],dic['ADOsRemark'],dic['DivisionalOfficersRemark'],dic['COsSpecialRemark'],dic['AreaCommanderRemark'],dic['ChoiceofAreaForPosting'],dic['ChoiceofNextAppointment'],dic['NameofImportantCourses'],dic['NameofNextCourse'],dic['ForeignCourse'],dic['SpecialQualification'],dic['ChoiceofNextCourse'],dic['DateofProceedinginTyDuty'],dic['TyBillet'],dic['PurposetofTy'],dic['TyDuration'],dic['DateofreturnfromTY'] ,dic['IfNotReturn'],dic['TotalTyDuration'],dic['TyHistorySummary'],dic['DateoflastSecurityClearance'],dic['ExtraCurricularActivities'],dic['GamesAndSports']))
            
            
            
            conn.commit()
            cur.close()
            conn.close()
            mcur = mysql.connection.cursor()
            mcur.execute("INSERT INTO UserInfo (O_No , usertype , pass , name , Branch , Rank , MobileNo_1 , MobileNo_2 , DateofBirth , PresentAddress , PermanentAddress , marrital_status , DateofMarriage , ServiceIdCardNo , NIDCardNo , DrivingLicenseNo , BloodGroup , LastDateofBloodDonation, Height , Weight , StateofOverWeight , FacebookAccount , Emailaddress , home_district , NextofKin , Relationship , ContactNumberofNextofKin , NameofWife , AddressofWife , MobileNo , Anyspecialinfowife , ChildrenNumber , ChildrenName , DOBofChildren , Anyspecialinfochildren , FathersName , FathersMobileNo , FathersAddress , MothersName , MothersMobileNo , MothersAddress , FamilyCrisis , SiblingNumber , BrothersName , BrothersMobileNo , BrothersAddress , highestEducation , OngoingcivilEducation , DateofJoiningService , ServiceCategory , Medicalcategory , DateofLastPromotion , DateofNextPromotion , PresentEngagement , NextREEngagementDue , DateofNextIncrement , NumberofGCB , EffectivedateofexistingGCB , DateofNextGCB , DateofJoiningShip , NameofShip , UNMission , GoodWillMission , DAONumber , PLeaveAvailed , LastDateofPL , PLeaveDue , RecreationLeaveDue , CLeaveAvailed , CLeaveDue , SickLeave , ExBangladeshLeave , Rl , Sourceofdebt , Amountofdebt , ADOsRemark , DivisionalOfficersRemark , COsSpecialRemark , AreaCommanderRemark , ChoiceofAreaForPosting , ChoiceofNextAppointment , NameofImportantCourses , NameofNextCourse , ForeignCourse , SpecialQualification , ChoiceofNextCourse , DateofProceedinginTyDuty , TyBillet , PurposetofTy , TyDuration , IfNotReturn , DateofreturnfromTY, TotalTyDuration , TyHistorySummary , DateoflastSecurityClearance , ExtraCurricularActivities , GamesAndSports) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (dic['O_No'],dic['usertype'],dic['pass'],dic['name'],dic['Branch'],dic['Rank'],dic['MobileNo_1'],dic['MobileNo_2'],dic['DateofBirth'],dic['PresentAddress'],dic['PermanentAddress'],dic['marrital_status'],dic['DateofMarriage'],dic['ServiceIdCardNo'],dic['NIDCardNo'],dic['DrivingLicenseNo'],dic['BloodGroup'],dic['LastDateofBloodDonation'],dic['Height'],dic['Weight'],dic['StateofOverWeight'],dic['FacebookAccount'],dic['Emailaddress'],dic['home_district'],dic['NextofKin'],dic['Relationship'],dic['ContactNumberofNextofKin'],dic['NameofWife'],dic['AddressofWife'],dic['MobileNo'],dic['Anyspecialinfowife'],dic['ChildrenNumber'],dic['ChildrenName'],dic['DOBofChildren'],dic['Anyspecialinfochildren'],dic['FathersName'],dic['FathersMobileNo'],dic['FathersAddress'],dic['MothersName'],dic['MothersMobileNo'],dic['MothersAddress'],dic['FamilyCrisis'],dic['SiblingNumber'],dic['BrothersName'],dic['BrothersMobileNo'],dic['BrothersAddress'],dic['highestEducation'],dic['OngoingcivilEducation'],dic['DateofJoiningService'],dic['ServiceCategory'],dic['Medicalcategory'],dic['DateofLastPromotion'],dic['DateofNextPromotion'],dic['PresentEngagement'],dic['NextREEngagementDue'],dic['DateofNextIncrement'],dic['NumberofGCB'],dic['EffectivedateofexistingGCB'],dic['DateofNextGCB'],dic['DateofJoiningShip'],dic['NameofShip'],dic['UNMission'],dic['GoodWillMission'],dic['DAONumber'],dic['PLeaveAvailed'],dic['LastDateofPL'],dic['PLeaveDue'],dic['RecreationLeaveDue'],dic['CLeaveAvailed'],dic['CLeaveDue'],dic['SickLeave'],dic['ExBangladeshLeave'],dic['Rl'],dic['Sourceofdebt'],dic['Amountofdebt'],dic['ADOsRemark'],dic['DivisionalOfficersRemark'],dic['COsSpecialRemark'],dic['AreaCommanderRemark'],dic['ChoiceofAreaForPosting'],dic['ChoiceofNextAppointment'],dic['NameofImportantCourses'],dic['NameofNextCourse'],dic['ForeignCourse'],dic['SpecialQualification'],dic['ChoiceofNextCourse'],dic['DateofProceedinginTyDuty'],dic['TyBillet'],dic['PurposetofTy'],dic['TyDuration'],dic['DateofreturnfromTY'] ,dic['IfNotReturn'],dic['TotalTyDuration'],dic['TyHistorySummary'],dic['DateoflastSecurityClearance'],dic['ExtraCurricularActivities'],dic['GamesAndSports']))
            mysql.connection.commit()
            mcur.close()
            # except:
            #     print("nothing")
            #     pass

            #print("ok")
        # except:
            #print("Error in inserting")
        
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
            return render_template("show.html", rows = result,login_status=login_status)
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
            return render_template("show.html", rows = result,login_status=login_status)
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