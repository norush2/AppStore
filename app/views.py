from django.shortcuts import render, redirect
from django.db import connection
import logging

logger = logging.getLogger("logger")

def index(request):
    """Shows the main page"""

    ## Delete tutor
    if request.POST:
        if request.POST['action'] == 'delete':
            student_id, module_code = request.POST['student_id_mod_code'].split('_')
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tutors WHERE student_id = %s AND module_code =  %s", [student_id, module_code])
    elif request.GET:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tutors WHERE module_code = %s", [request.GET['module_code']])
            tutors = cursor.fetchall()
        result_dict = {'records': tutors}
        return render(request,'app/index.html', result_dict)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tutors ORDER BY name")
        tutors = cursor.fetchall()
    result_dict = {'records': tutors}
    return render(request,'app/index.html', result_dict)

def view(request, student_id_mod_code):
    """Shows the view of a tutor"""
    logger.info("Hello")
    student_id, module_code = student_id_mod_code.split('_')
    ## Use raw query to get a tutor
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tutors WHERE student_id = %s AND module_code = %s", [student_id, module_code])
        tutor = cursor.fetchone()
        cursor.execute("SELECT module_name FROM modules WHERE module_code = %s", [module_code])
        module = cursor.fetchone()
        
    result_dict = {'record': tutor, 'module': module} # not sure whats this gonna be like
    return render(request, 'app/view.html', result_dict)

# Create your views here.
def add_tutor(request):
    """Shows the add_tutor page"""
    context = {"status": 0}
    if request.POST:
        ## Check if user already a tutor
        with connection.cursor() as cursor:
            query = "SELECT * FROM tutors WHERE student_id = %s AND module_code = %s"
            cursor.execute(query, [request.POST['student_id'], request.POST['module_code']])
            tutor = cursor.fetchone()
            if not tutor:
                make_tutor_op = "INSERT INTO tutors VALUES (%s, %s, %s, %s, %s, %s, %s)"
                tutor_values = [request.POST['student_id'], request.POST['name'], request.POST['module_code']
                        , request.POST['grade'], request.POST['fee'], request.POST['unit_time'], request.POST['year']]
                cursor.execute(make_tutor_op, tutor_values)
                context["status"] = 1
                # return redirect('index')    
            else:
                context["status"] = 2
    with connection.cursor() as cursor:
        cursor.execute("SELECT module_code, module_name FROM modules")
        modules = cursor.fetchall()
        context["modules"] = modules
    return render(request, "app/add_tutor.html", context)

# Create your views here.
def add_user(request):
    """Shows the add_user page"""
    context = {"status": 0}
    if request.POST:
        ## Check if student_id is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE student_id = %s", [request.POST['student_id']])
            user = cursor.fetchone()
            if not user:
                cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s)",
                    [request.POST['student_id'], request.POST['name'],
                    True if request.POST['is_admin'] == 'True' else False,
                    request.POST['password']])
                context["status"] = 1
                # return redirect('index')    
            else:
                context["status"] = 2
                status = 'User with ID %s already exists' % (request.POST['student_id']) 
    return render(request, "app/add_user.html", context)

# Create your views here.
def edit(request, id):
    """Shows the edit page"""

    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)

def login(request):
    """Shows the login page"""
    context = {"status": 0}
    # Delete tutor not user
    if request.POST:
        student_id, password = request.POST['student_id'], request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE student_id = %s", [student_id])
            user = cursor.fetchone()
            if user:
                if user[3] == password:
                    context["status"] = 1   #logged in
                    return redirect('index')
                else:
                    context["status"] = 2   #wrong password                
            else:
                context["status"] = 3       #user not found
    return render(request,'app/login.html', context)

def index_pre_login(request):
    """Shows the main page"""

    ## Delete tutor not user
    if request.POST:
        if request.POST['action'] == 'delete':
            student_id, module_code = request.POST['student_id_mod_code'].split('_')
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tutors WHERE student_id = %s AND module_code =  %s", [student_id, module_code])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tutors ORDER BY name")
        tutors = cursor.fetchall()

    result_dict = {'records': tutors}
    return render(request,'app/index_pre_login.html', result_dict)