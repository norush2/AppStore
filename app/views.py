from django.shortcuts import render, redirect
from django.db import connection
import logging

logger = logging.getLogger("logger")

def index(request):
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
    """Shows the main page"""
    context = {}
    status = ''
    if request.POST:
        ## Check if user already a tutor
        with connection.cursor() as cursor:
            query = "SELECT * FROM tutors WHERE student_id = %s AND module_code = %s"
            cursor.execute(query, [request.POST['student_id'], request.POST['module_code']])
            tutor = cursor.fetchone()
            
            # User is not a tutor
            if not tutor:
                make_tutor_op = "INSERT INTO tutors VALUES (%s, %s, %s, %s, %s, %s, %s)"
                tutor_values = [request.POST['student_id'], request.POST['name'], request.POST['module_code']
                        , request.POST['grade'], request.POST['fee'], request.POST['unit_time'], request.POST['year']]
                cursor.execute(make_tutor_op, tutor_values)
                status = 'User is now a tutor!'
                return redirect('index')    
            else:
                status = 'User is already a tutor. Add new listing instead!'
                """add_listing"""
                #status = 'Customer with ID %s already exists' % (request.POST['customerid'])
    context['status'] = status
    return render(request, "app/add_tutor.html", context)

# Create your views here.
def add_user(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('index')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add_user.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

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
    """Shows the main page"""

    # Delete tutor not user
    if request.POST:
        student_id, password = request.POST['student_id'], request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE student_id = %s AND password =  %s", [student_id, password])
            user = cursor.fetchone()
            if user:
                status = "Logged in"
                return redirect('index')
            else:
                status = "Login failed"
                context = {"status": status}
                return render(request, "app/login.html", context)

    return render(request,'app/login.html')

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