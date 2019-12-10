from flask import *
from datetime import datetime
from datetime import timedelta
import sqlite3 as sql
import json

app = Flask(__name__, template_folder='template')
app.secret_key = "123456"

Blood_Group = ['O+Ve','O-Ve','A+Ve','A-Ve','AB+Ve','AB-Ve','B+Ve','B-Ve']
Home_District = [ 'Bagerhat','Bandarban','Barguna','Barisal','Bhola','Bogra','Brahmanbaria','Chandpur','Chittagong','Chuadanga','Comilla','Cox\'\s Bazar','Dhaka','Dinajpur','Faridpur','Feni','Gaibandha','Gazipur','Gopalganj','Habiganj','Jaipurhat','Jamalpur','Jessore','Jhalakati','Jhenaidah','Khagrachari','Khulna','Kishoreganj','Kurigram','Kushtia','Lakshmipur','Lalmonirhat','Madaripur','Magura','Manikganj','Meherpur','Moulvibazar','Munshiganj','Mymensingh','Naogaon','Narail','Narayanganj','Narsingdi','Natore','Nawabganj','Netrakona','Nilphamari','Noakhali','Pabna','Panchagarh','Parbattya Chattagram','Patuakhali','Pirojpur','Rajbari','Rajshahi','Rangpur','Satkhira','Shariatpur','Sherpur','Sirajganj','Sunamganj','Sylhet','Tangail','Thakurgaon']
Highest_Education = ['Class 8','SSC','HSC','B.Sc','BA','M.Sc','Diploma']
Ongoing_Education = ['SSC','HSC','B.Sc','BA','M.Sc']
Service_Category = ['Continuous','Non-Continuous']
Present_Engagement = ['Intial','1st','2nd','3rd','4th','5th']
Number_of_GCB = ['1st GCB','2nd GCB','3rd GCB']
Choice_of_Area_for_drafting = ['Dhaka','Khulna','Chattogram','Mongla','Patuakhali','Kaptai']
Choice_of_Next_Appointment = ['Instructor','Sea Service','Shore Service']
YesNo = ['No','Yes']

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

Marital_Status = ['Single', 'Married', 'Divorced']
User_Type = ['System Administrator', 'ADO', 'Divisional Officer', 'Commanding Officer', 'Staff Officer', 'Comflot']


Column = [ 'O_No' , 'usertype' , 'password' , 'name' , 'slist1' , 'slist2' , 'MobileNo_1' , 'MobileNo_2' , 'DateofBith' , 'PresentAddress' , 'PermanentAddress' , 'marrital_status' , 'DateofMarriage' , 'ServiceIdCardNo' , 'NIDCardNo' , 'DrivingLicenseNo' , 'BloodGroup' , 'Height' , 'Weight' , 'StateofOverWeight' , 'FacebookAccount' , 'Emailaddress' , 'home_district' , 'NextofKin' , 'Relationship' , 'ContactNumberofNextofKin' , 'NameofWife' , 'AddressofWife' , 'MobileNo' , 'Anyspecialinfowife' , 'ChildrenNumber' , 'ChildrenName' , 'DOBofChildren' , 'Anyspecialinfochildren' , 'FathersName' , 'FathersMobileNo' , 'FathersAddress' , 'MothersName' , 'MothersMobileNo' , 'MothersAddress' , 'FamilyCrisis' , 'SiblingNumber' , 'BrothersName' , 'BrothersMobileNo' , 'BrothersAddress' , 'highestEducation' , 'OngoingcivilEducation' , 'DateofJoiningService' , 'ServiceCategory' , 'Medicalcategory' , 'DateofLastPromotion' , 'DateofNextPromotion' , 'PresentEngagement' , 'NextREEngagementDue' , 'DateofNextIncrement' , 'NumberofGCB' , 'EffectivedateofexistingGCB' , 'DateofNextGCB' , 'DateofJoiningShip' , 'NameofShip' , 'UNMission' , 'GoodWillMission' , 'DAONumber' , 'PLeaveAvailed' , 'LastDateofPL' , 'PLeaveDue' , 'RecreationLeaveDue' , 'CLeaveAvailed' , 'CLeaveDue' , 'SickLeave' , 'ExBangladeshLeave' , 'Rl' , 'Sourceofdebt' , 'Amountofdebt' , 'ChoiceofAreaForPosting' , 'ChoiceofNextAppointment' , 'NameofImportantCourses' , 'NameofNextCourse' , 'ForeignCourse' , 'SpecialQualification' , 'ChoiceofNextCourse' , 'DateoflastSecurityClearance' , 'ExtraCurricularActivities' , 'GamesAndSports','DateofProceedinginTyDuty' , 'TyBillet' ,'PurposetofTy' ,'TyDuration' ,'DateofreturnfromTY', 'IfNotReturn' ,'TotalTyDuration' , 'TyHistorySummary','ADOsRemark','DivisionalOfficersRemark','COsSpecialRemark','AreaCommanderRemark' ]



data_with_datatpe=[['O_No','text'],['usertype','text'],['password','text'],['name','text'],['slist1','INTEGER'],['slist2','INTEGER,'],['MobileNo_1','text'],['MobileNo_2','text'],['DateofBith','Date'],['PresentAddress','text'],['PermanentAddress','text'],['marrital_status','INTEGER'],['DateofMarriage','Date'],['ServiceIdCardNo','text'],['NIDCardNo','text'],['DrivingLicenseNo','text'],['BloodGroup','INTEGER'],['Height','Float'],['Weight','FLoat,'],['StateofOverWeight','INTEGER'],['FacebookAccount','text'],['Emailaddress','text'],['home_district','INTEGER'],['NextofKin','text'],['Relationship','text'],['ContactNumberofNextofKin','text'],['NameofWife','text'],['AddressofWife','text'],['MobileNo','text'],['Anyspecialinfowife','text'],['ChildrenNumber','INTEGER'],['ChildrenName','text'],['DOBofChildren','date'],['Anyspecialinfochildren','text'],['FathersName','text'],['FathersMobileNo','text'],['FathersAddress','text'],['MothersName','text'],['MothersMobileNo','text'],['MothersAddress','text'],['FamilyCrisis','text'],['SiblingNumber','INTEGER'],['BrothersName','text'],['BrothersMobileNo','text'],['BrothersAddress','text'],['highestEducation','INTEGER'],['OngoingcivilEducation','INTEGER'],['DateofJoiningService','date'],['ServiceCategory','INTEGER'],['Medicalcategory','text'],['DateofLastPromotion','date'],['DateofNextPromotion','date'],['PresentEngagement','INTEGER'],['NextREEngagementDue','date'],['DateofNextIncrement','date'],['NumberofGCB','INTEGER'],['EffectivedateofexistingGCB','text'],['DateofNextGCB','date'],['DateofJoiningShip','date'],['NameofShip','text'],['UNMission','text'],['GoodWillMission','text'],['DAONumber','text'],['PLeaveAvailed','INTEGER'],['LastDateofPL','date'],['PLeaveDue','INTEGER'],['RecreationLeaveDue','date'],['CLeaveAvailed','INTEGER'],['CLeaveDue','INTEGER'],['SickLeave','text'],['ExBangladeshLeave','text'],['Rl','text'],['Sourceofdebt','text'],['Amountofdebt','float'],['ChoiceofAreaForPosting','INTEGER'],['ChoiceofNextAppointment','INTEGER'],['NameofImportantCourses','text'],['NameofNextCourse','text'],['ForeignCourse','text'],['SpecialQualification','text'],['ChoiceofNextCourse','text'],['DateoflastSecurityClearance','text'],['ExtraCurricularActivities','text'],['GamesAndSports','text'],['DateofProceedinginTyDuty','date'], ['TyBillet' , 'text'] ,['PurposetofTy', 'text'] ,['TyDuration','INTEGER'],['DateofreturnfromTY','date'] ,['IfNotReturn','INTEGER'], ['TotalTyDuration','INTEGER'], ['TyHistorySummary','Text'],['ADOsRemark','text'],['DivisionalOfficersRemark','text'],['COsSpecialRemark','text'],['AreaCommanderRemark','text']]



@app.route('/')
def signin():
    try:
        conn = sql.connect("database.db")
        conn.execute('CREATE TABLE IF NOT EXISTS UserInfo (O_No text Primary key ,usertype text ,password text ,name text ,slist1 INTEGER ,slist2 INTEGER,MobileNo_1 text ,MobileNo_2 text ,DateofBith Date ,PresentAddress text ,PermanentAddress text ,marrital_status INTEGER ,DateofMarriage Date ,ServiceIdCardNo text ,NIDCardNo text ,DrivingLicenseNo text ,BloodGroup INTEGER ,Height Float ,Weight FLoat,StateofOverWeight INTEGER ,FacebookAccount text ,Emailaddress text ,home_district INTEGER ,NextofKin text ,Relationship text ,ContactNumberofNextofKin text ,NameofWife text ,AddressofWife text ,MobileNo text ,Anyspecialinfowife text ,ChildrenNumber INTEGER ,ChildrenName text ,DOBofChildren date ,Anyspecialinfochildren text ,FathersName text ,FathersMobileNo text ,FathersAddress text ,MothersName text ,MothersMobileNo text ,MothersAddress text ,FamilyCrisis text ,SiblingNumber INTEGER ,BrothersName text ,BrothersMobileNo text ,BrothersAddress text ,highestEducation INTEGER ,OngoingcivilEducation INTEGER ,DateofJoiningService date ,ServiceCategory INTEGER ,Medicalcategory text ,DateofLastPromotion date ,DateofNextPromotion date ,PresentEngagement INTEGER ,NextREEngagementDue date ,DateofNextIncrement date ,NumberofGCB INTEGER ,EffectivedateofexistingGCB text ,DateofNextGCB date ,DateofJoiningShip date ,NameofShip text ,UNMission text ,GoodWillMission text ,DAONumber text ,PLeaveAvailed INTEGER ,LastDateofPL date ,PLeaveDue INTEGER ,RecreationLeaveDue date ,CLeaveAvailed INTEGER ,CLeaveDue INTEGER ,SickLeave text ,ExBangladeshLeave text ,Rl text ,Sourceofdebt text ,Amountofdebt float ,ChoiceofAreaForPosting INTEGER ,ChoiceofNextAppointment INTEGER ,NameofImportantCourses text ,NameofNextCourse text ,ForeignCourse text ,SpecialQualification text ,ChoiceofNextCourse text ,DateoflastSecurityClearance text ,ExtraCurricularActivities text ,GamesAndSports text,DateofProceedinginTyDuty date, TyBillet text , PurposetofTy text ,TyDuration INTEGER , DateofreturnfromTY date,IfNotReturn INTEGER, TotalTyDuration INTEGER, TyHistorySummary Text,ADOsRemark text,DivisionalOfficersRemark text,COsSpecialRemark text,AreaCommanderRemark text )')
    except:
        return "There is an error (i.e. Read Only file system)"
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO UserInfo (O_No, password, usertype) VALUES (?, ?, ?)",('admin', '123456', 0))
        cur.execute("INSERT INTO UserInfo (O_No, password, usertype) VALUES (?, ?, ?)",('temp', 'temp', 1))
        conn.commit() 
    except:
        pass
    
        
    if 'O_No' in session:
        return redirect(url_for('profile', id = session['O_No']))
    else:
        return render_template("signin.html")

@app.route('/search')
def search():
    if 'O_No' in session:
        return render_template("search.html")
    else:
        return "false page"
    
@app.route('/logout')
def logout():
    if 'O_No' in session:
        session.pop('O_No', None)
        session.pop('usertype', None)
    return redirect(url_for('signin'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = request.form
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * from UserInfo where O_No = ?' , [result['O_No']])
        rows = cur.fetchall()
        for row in rows:
            if row['password'] == result['password']:
                session['usertype'] = row['usertype']
                session['O_No'] = result['O_No']
                break
    return redirect(url_for('signin'))

@app.route('/profile/<string:id>')
def profile(id):
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    #cur.execute('SELECT * from UserInfo where O_No = ?' , [result['O_No']])
    cur.execute('SELECT * from UserInfo where O_No = ?' , [id])
    rows = cur.fetchall()
    if 'O_No' in session:
        usertype = int(session['usertype'])
        return render_template('profile.html',Column = Column,usertype = usertype,rows=rows)
    else:
        return redirect(url_for('signin'))

@app.route('/debug')
def debug():
    return "This page is under mantainance"

@app.route('/adduser/adding_user',methods=['POST','GET'])
def adding_user():
    if 'O_No' in session:
        if int(session['usertype']) == 0:
            conn = sql.connect("database.db")
            cur = conn.cursor()
            if request.method =='POST':
                mp = request.form
                dic = {}
                for col in Column:
                    try:
                        val = mp[col]
                    except:
                        val = ""
                    dic[col] = val
            try:
                dic['StateofOverWeight']=0
                #nextreengagement calculation
                dateofjoiningship = dic['DateofJoiningShip']
                presentengagement = int(dic['PresentEngagement'])
                servicecategory = int(dic['ServiceCategory'])
                dateofjoiningship = datetime.strptime(dateofjoiningship,'%Y-%m-%d')
                dic['NextREEngagementDue']=calculateReEngagement(dateofjoiningship,presentengagement,servicecategory)

                #calculation of EffectivedateofexistingGCB
                effectivedateofexistinggcb = dic['EffectivedateofexistingGCB']
                effectivedateofexistinggcb = datetime.strptime(effectivedateofexistinggcb,'%Y-%m-%d')
                dic['DateofNextGCB'] = addyearmonth(effectivedateofexistinggcb,4,0)
                #print(dic['DateofNextGCB'])

                #pleave due calculation
                PLeaveAvailed = dic['PLeaveAvailed']
                PLeaveDue = 60 - int(PLeaveAvailed)
                dic['PLeaveDue'] = PLeaveDue

                #print(dic['PLeaveDue'])

                #RL Due Calculation
                DateofJoiningService = dic['DateofJoiningService']
                DateofJoiningService = datetime.strptime(DateofJoiningService,'%Y-%m-%d')
                dic['RecreationLeaveDue'] = addyearmonth(DateofJoiningService,3,0)
                #print(dic['RecreationLeaveDue'])

                #C leave due
                CLeaveAvailed = dic['CLeaveAvailed']
                dic['CLeaveDue'] = 20 - int(CLeaveAvailed)
                #print(dic['CLeaveDue'])

                #Date of return from ty
                DateofProceedinginTyDuty = dic['DateofProceedinginTyDuty']
                dic['DateofreturnfromTY'] = datetime.strptime(DateofProceedinginTyDuty,'%Y-%m-%d').date() + timedelta(days=int(dic['TyDuration']))
                #print(dic['DateofreturnfromTY'])
                
                tyduration = int(dic['TyDuration'])
                ifnotreturn = dic['IfNotReturn']
                if(ifnotreturn=="0"):
                    tyduration+=1
                dic['TyDuration']=tyduration
                #print(dic['TyDuration'])

                #date of next increment
                DateofJoiningShip = dic['DateofJoiningShip']
                DateofJoiningShip = datetime.strptime(DateofJoiningShip,'%Y-%m-%d')
                dic['DateofNextIncrement'] = addyearmonth(DateofJoiningShip,0,11)
                #print(dic['DateofJoiningShip'])
                cur.execute("INSERT INTO UserInfo (O_No , usertype , password , name , slist1 , slist2 , MobileNo_1 , MobileNo_2 , DateofBith , PresentAddress , PermanentAddress , marrital_status , DateofMarriage , ServiceIdCardNo , NIDCardNo , DrivingLicenseNo , BloodGroup , Height , Weight , StateofOverWeight , FacebookAccount , Emailaddress , home_district , NextofKin , Relationship , ContactNumberofNextofKin , NameofWife , AddressofWife , MobileNo , Anyspecialinfowife , ChildrenNumber , ChildrenName , DOBofChildren , Anyspecialinfochildren , FathersName , FathersMobileNo , FathersAddress , MothersName , MothersMobileNo , MothersAddress , FamilyCrisis , SiblingNumber , BrothersName , BrothersMobileNo , BrothersAddress , highestEducation , OngoingcivilEducation , DateofJoiningService , ServiceCategory , Medicalcategory , DateofLastPromotion , DateofNextPromotion , PresentEngagement , NextREEngagementDue , DateofNextIncrement , NumberofGCB , EffectivedateofexistingGCB , DateofNextGCB , DateofJoiningShip , NameofShip , UNMission , GoodWillMission , DAONumber , PLeaveAvailed , LastDateofPL , PLeaveDue , RecreationLeaveDue , CLeaveAvailed , CLeaveDue , SickLeave , ExBangladeshLeave , Rl , Sourceofdebt , Amountofdebt , ADOsRemark , DivisionalOfficersRemark , COsSpecialRemark , AreaCommanderRemark , ChoiceofAreaForPosting , ChoiceofNextAppointment , NameofImportantCourses , NameofNextCourse , ForeignCourse , SpecialQualification , ChoiceofNextCourse , DateofProceedinginTyDuty , TyBillet , PurposetofTy , TyDuration , IfNotReturn , DateofreturnfromTY, TotalTyDuration , TyHistorySummary , DateoflastSecurityClearance , ExtraCurricularActivities , GamesAndSports) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (dic['O_No'],dic['usertype'],dic['password'],dic['name'],dic['slist1'],dic['slist2'],dic['MobileNo_1'],dic['MobileNo_2'],dic['DateofBith'],dic['PresentAddress'],dic['PermanentAddress'],dic['marrital_status'],dic['DateofMarriage'],dic['ServiceIdCardNo'],dic['NIDCardNo'],dic['DrivingLicenseNo'],dic['BloodGroup'],dic['Height'],dic['Weight'],dic['StateofOverWeight'],dic['FacebookAccount'],dic['Emailaddress'],dic['home_district'],dic['NextofKin'],dic['Relationship'],dic['ContactNumberofNextofKin'],dic['NameofWife'],dic['AddressofWife'],dic['MobileNo'],dic['Anyspecialinfowife'],dic['ChildrenNumber'],dic['ChildrenName'],dic['DOBofChildren'],dic['Anyspecialinfochildren'],dic['FathersName'],dic['FathersMobileNo'],dic['FathersAddress'],dic['MothersName'],dic['MothersMobileNo'],dic['MothersAddress'],dic['FamilyCrisis'],dic['SiblingNumber'],dic['BrothersName'],dic['BrothersMobileNo'],dic['BrothersAddress'],dic['highestEducation'],dic['OngoingcivilEducation'],dic['DateofJoiningService'],dic['ServiceCategory'],dic['Medicalcategory'],dic['DateofLastPromotion'],dic['DateofNextPromotion'],dic['PresentEngagement'],dic['NextREEngagementDue'],dic['DateofNextIncrement'],dic['NumberofGCB'],dic['EffectivedateofexistingGCB'],dic['DateofNextGCB'],dic['DateofJoiningShip'],dic['NameofShip'],dic['UNMission'],dic['GoodWillMission'],dic['DAONumber'],dic['PLeaveAvailed'],dic['LastDateofPL'],dic['PLeaveDue'],dic['RecreationLeaveDue'],dic['CLeaveAvailed'],dic['CLeaveDue'],dic['SickLeave'],dic['ExBangladeshLeave'],dic['Rl'],dic['Sourceofdebt'],dic['Amountofdebt'],dic['ADOsRemark'],dic['DivisionalOfficersRemark'],dic['COsSpecialRemark'],dic['AreaCommanderRemark'],dic['ChoiceofAreaForPosting'],dic['ChoiceofNextAppointment'],dic['NameofImportantCourses'],dic['NameofNextCourse'],dic['ForeignCourse'],dic['SpecialQualification'],dic['ChoiceofNextCourse'],dic['DateofProceedinginTyDuty'],dic['TyBillet'],dic['PurposetofTy'],dic['TyDuration'],dic['DateofreturnfromTY'] ,dic['IfNotReturn'],dic['TotalTyDuration'],dic['TyHistorySummary'],dic['DateoflastSecurityClearance'],dic['ExtraCurricularActivities'],dic['GamesAndSports']))
                #cur.execute("INSERT INTO UserInfo (O_No, name, usertype) VALUES (?, ?, ?)",(dic['O_No'],dic['name'], dic['usertype']))
                conn.commit()
                #print("ok")
            except:
                print("Error in inserting")
            #return dic
    return redirect(url_for('profile', id = session['O_No']))

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




@app.route('/adduser')
def adduser():
    if 'O_No' in session:
        if int(session['usertype']) == 0:
            return render_template('adduser.html',YesNo = YesNo,Home_District = Home_District, Marital_Status = Marital_Status,Branch_key = Branch, Branch = json.dumps(Branch), Blood_Group = Blood_Group, Highest_Education = Highest_Education, Ongoing_Education = Ongoing_Education, Service_Category = Service_Category, Present_Engagement = Present_Engagement, Number_of_GCB = Number_of_GCB, Choice_of_Area_for_drafting = Choice_of_Area_for_drafting, Choice_of_Next_Appointment = Choice_of_Next_Appointment, User_Type = User_Type)
    return "False page"

@app.route('/show')
def show():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    usertype = int(session['usertype'])
    if(usertype == 0 or usertype == 1 or usertype==4 or usertype==4 or usertype==5):
        cur.execute('SELECT O_No from UserInfo')
    elif(usertype==3):
        cur.execute('SELECT NameofShip from UserInfo where O_No = ?',[session['O_No']])
        temp = cur.fetchall()
        ans = 0 
        for row in temp:
            ans = row['NameofShip']
        cur.execute('SELECT O_No from UserInfo where NameofShip = ? ',[ans])
    rows = cur.fetchall(); 
    #cur.execute('SELECT O_No from UserInfo where usertype >= ?' , session['usertype'])
    return render_template("show.html", rows = rows)
@app.route('/search_result',methods=['POST','GET'])
def search_result():
    if request.method == 'POST':
        result = request.form
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        usertype = int(session['usertype'])
    
        if(usertype == 0 or usertype == 1 or usertype==4 or usertype==4 or usertype==5):
            cur.execute('SELECT * from UserInfo')
        elif(usertype==3):
            cur.execute('SELECT NameofShip from UserInfo where O_No = ?',[session['O_No']])
            temp = cur.fetchall()
            ans = 0 
            for row in temp:
                ans = row['NameofShip']
            cur.execute('SELECT * from UserInfo where NameofShip = ? ',[ans])
        temp = cur.fetchall()
        name = result['name']
        shipname = result['shipname']
        O_No = result['O_No']
        #print(temp)
        l = []
        for row in temp:
            ans_ship_name=row['NameofShip']
            ans_name = row['name']
            ans_O_No = row['O_No']
            print(ans_O_No,O_No)
            print(ans_name,name)
            print(ans_ship_name,shipname)
            if(ans_ship_name==shipname or ans_name == name or O_No == ans_O_No):
                l.append(row['O_No'])

        #     print(ans_name)
        #     print(row)
        #     cur.execute('SELECT O_No from UserInfo where NameofShip = ? or name = ? or O_No = ?',([shipname,name,O_No]))
        # rows = cur.fetchall()
        print(l)

    return render_template("search_result.html", rows = l)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)