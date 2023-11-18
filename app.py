from flask import Flask
import requests
# import mysql.connector
import psycopg2
import json
import os

app = Flask(__name__)
app.secret_key = "secret"


def get_id(rollno):

    mydb = psycopg2.connect(
        host=os.environ['PGHOST'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT'],
        database=os.environ['PGDATABASE'],
        sslmode="require",
    )

    mycursor = mydb.cursor()
    get_user_query = "select unified_id from users where rollno=%s"
    user_data = (rollno,)
    mycursor.execute(get_user_query, user_data)
    person_id = mycursor.fetchone()
    if person_id:
        print(f"person '{person_id}' exists.")
        mydb.close()
    else:
        print(f"person '{person_id}' does not exist.")
    mydb.close()

    print(person_id[0])
    return person_id[0]

@app.route('/')
def home():
    return "welcome to the home page hopefully this fucking thing works"


@app.route('/internal-marks/<int:rollno>')
def internal_marks(rollno):
    person_id = get_id(rollno)
    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '10%2C12',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonId': person_id,
        'Semester': 0,
        'Category': 0,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/HRMS/ManageStaffStudent/UniPersonInfo.asmx/BindInternalMarks',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    data = response.json()
    data = json.loads(data['d'])

    return data



@app.route('/sem-marks/<int:rollno>')
def sem_marks(rollno):
    """
    app route: http://localhost/<rollno>/<sem>
    default sem: 0 -> gives the possible semesters
    """
    person_id = get_id(rollno)

    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '0000000',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonId': person_id,
        'Semester': 0,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/HRMS/ManageStaffStudent/UniPersonInfo.asmx/BindSemester',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    data = response.json()
    data = json.loads(data['d'])

    return data

@app.route('/grade/<int:rollno>/')
@app.route('/grade/<int:rollno>/<int:sem>')
def grade(rollno, sem=0):
    """
    app route: https://loalhost/<rollno>/<sem>
    <roll_no> user roll number is provided them their unified id is retrived from database
    <sem>
        0 - to retrieve all
        1 - semester 1
        .
        .
        .

    """
    person_id = get_id(rollno)
    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '0000000',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'PersonId': person_id,
        'Semester': sem,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/HRMS/ManageStaffStudent/UniPersonInfo.asmx/BindGrade',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    data = response.json()
    data = json.loads(data['d'])

    return data

# two app.route()
# to make the <int:sem> optional
@app.route('/attendance/<int:rollno>/')
def get_attendance(rollno):
    person_id = get_id(rollno)

    cookies = {
        'G_ENABLED_IDPS': 'google',
        'ASP.NET_SessionId': '000000000000000000000000',
        'dcjq-accordion': '10%2C12',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'http://rajalakshmi.in',
        'Referer': 'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx?FormHeading=myProfile',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'StartDate': '01-10-2023',
        'EndDate': '01-11-2023',
        'PersonID': person_id,
    }

    response = requests.post(
        'http://rajalakshmi.in/UI/Modules/Profile/Profile.aspx/GetStudentAttendanceDetail',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    data = response.json()['d']
    data = json.loads(data)
    return data

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
