from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
import stripe
from django.conf import settings  # Import Django settings
from stripe.error import StripeError, CardError
import googlemaps









# Create your views here.
def About(request):
    return render(request,"about.html")

def Home(request):
    return render(request,"home.html")


def Contact(request):
    return render(request,"contact.html")

def Index(request):
    if not request.user.is_staff:
        return redirect("login")
    doctors=Doctor.objects.all()
    patients=Patient.objects.all()
    appointments=Appointment.objects.all()
    d=0
    p=0
    a=0
    for i in doctors:
        d+=1
    for i in patients:
        p+=1
    for i in appointments:
        a+=1
    db={"d":d,"p":p,"a":a}
    return render(request,"index.html",db)

def Login(request):
    # error= ""
    if request.method == "POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(request,username=u,password=p)
        if user is not None and user.is_staff :
            login(request,user)
            return redirect("index")
    try:
        if user.is_staff:
            Login(request,user)
            error="No"
            
        else:
            error="yes"
    except:

        error="yes"
    d={"error":error}
    return render(request,"login.html",d)
    # else:
   
        # messages.error(request,"Invalid user")
        # return render(request,"login.html")
    #     try:
    #         if user.is_staff:
    #             Login(request,user)
    #             error="No"
            
    #         else:
    #             error="yes"
    #     except:

    #         error="yes"
    # d={"error":error}
    # return render(request,"login.html",d)

def Logout(request):
    if not request.user.is_staff:
        return redirect("login")
    
    logout(request)
    return redirect("login")

def ViewDoctor(request):
    if not request.user.is_staff:
        return redirect("login")
    doc=Doctor.objects.all()
    d={"doc":doc}
    return render(request,"view_doctor.html",d)

def DeleteDoctor(request,pid):
    if not request.user.is_staff:
        return redirect("login")
    # doctor=Doctor.Objects.get(id=pid)
    doctor=Doctor(id=pid)


    doctor.delete()
    
    return redirect("viewdoctor")

def AddDoctor(request):
    error= ""
    if not request.user.is_staff:
        return redirect("login")
    if request.method == "POST":
        n=request.POST['doctor']
        m=request.POST['mobile']
        sp=request.POST['special']

        
        try:
            # Doctor.objects.create(Name=n,mobile=m,special=sp)
            query=Doctor(Name=n,mobile=m,special=sp)
            query.save()
            return redirect("viewdoctor")


            error="no"
        except:
            error="yes"
    d={"error":error}
            # query.save()
    return render(request,"adddoctor.html", d)
        
    
            # error="No"
            
    
        # except:
        #     error="yes"
        #     d={"error":error}

def ViewPatient(request):
    if not request.user.is_staff:
        return redirect("login")
    pat=Patient.objects.all()
    p={"pat":pat}
    return render(request,"viewpatient.html",p)
        
def DeletePatient(request,pid):
    if not request.user.is_staff:
        return redirect("login")
    # doctor=Doctor.Objects.get(id=pid)
    patient=Patient(id=pid)


    patient.delete()
    
    return redirect("viewpatient")

def AddPatient(request):
    error= ""
    if not request.user.is_staff:
        return redirect("login")
    if request.method == "POST":
        n=request.POST['patient']
        g=request.POST['gender']

        m=request.POST['mobile']
        a=request.POST['address']

        
        try:
            # Doctor.objects.create(Name=n,mobile=m,special=sp)
            query=Patient(Name=n,gender=g,mobile=m,address=a)
            query.save()
            return redirect("viewpatient")


            error="no"
        except:
            error="yes"
    d={"error":error}
            # query.save()
    return render(request,"addpatient.html",d)

def ViewAppointment(request):
    if not request.user.is_staff:
        return redirect("login")
    app=Appointment.objects.all()
    a={"app":app}
    return render(request,"viewappointments.html",a)

def DeleteAppointment(request,pid):
    if not request.user.is_staff:
        return redirect("login")
    # doctor=Doctor.Objects.get(id=pid)
    appointment=Appointment(id=pid)


    appointment.delete()
    
    return redirect("viewappointment")

def AddAppointment(request):
    error= ""
    if not request.user.is_staff:
        return redirect("login")
    doctor1=Doctor.objects.all()
    patient1=Patient.objects.all()

    if request.method == "POST":
        d=request.POST["doctor"]
        p=request.POST["patient"]

        date=request.POST["date"]
        time=request.POST["time"]
        doctor=Doctor.objects.filter(Name=d).first()
        patient=Patient.objects.filter(Name=p).first()
        # query=Appointment(doctor=d,patient=p,date=date,time=time)
        # query.save()
        # return redirect("viewappointment")
        

        
        try:

            Appointment.objects.create(Doctor=doctor,Patient=patient,date=date,time=time)
            # return redirect("viewappointment")


            # query=Appointment(doctor=d,patient=p,date=da,time=t)
            # query.save()
            # return redirect("viewappointment")


            error="no"

        except:

            error="yes"
    a={"doctor":doctor1,"patient":patient1,"error":error}
    #         # query.save()
    return render(request,"addappointments.html",a)




@login_required
def add_appointment_request(request):
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            appointment_request = form.save(commit=False)
            appointment_request.user = request.user
            appointment_request.save()
            return redirect('user_dashboard')
            # return redirect(reverse('approve_appointment_request', kwargs={'request_id': appointment_request.id}))
 
    else:
        form = AppointmentRequestForm()
    return render(request, 'add_appointment_request.html', {'form': form})

def appointment_request_success(request):
    return render(request, 'appointment_request_success.html')

# from django.shortcuts import render, redirect
# from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to user dashboard or any other page
                return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'user_login.html', {'form': form})

@login_required
def user_dashboard(request):
    user = request.user

    # Fetch appointment requests for the current user
    appointment_requests = AppointmentRequest.objects.filter(user=user)

    return render(request, 'user_dashboard.html', {'appointment_requests': appointment_requests})

def create_payment(request, request_id):
    appointment_request = get_object_or_404(AppointmentRequest, id=request_id)

    paypal_client_id = settings.PAYPAL_CLIENT_ID
    paypal_client_secret = settings.PAYPAL_CLIENT_SECRET

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment', kwargs={'request_id': appointment_request.id})),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancelled'))
        },
        "transactions": [{
            "amount": {
                "total": str(appointment_request.amount),
                "currency": "USD"
            },
            "description": "Payment for appointment request."
        }]
    })

    if payment.create():
        appointment_request.payment_id = payment.id
        appointment_request.save()
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        messages.error(request, "Failed to process payment.")
        return redirect('appointment_request_detail', request_id=appointment_request.id)

def execute_payment(request, request_id):
    appointment_request = get_object_or_404(AppointmentRequest, id=request_id)
    payment_id = appointment_request.payment_id

    payment = Payment.find(payment_id)
    if payment.execute({"payer_id": request.GET.get('PayerID')}):
        appointment_request.is_approved = True  # Mark request as approved
        appointment_request.save()
        messages.success(request, "Payment successfully processed.")
        return redirect('appointment_request_detail', request_id=appointment_request.id)
    else:
        messages.error(request, "Failed to execute payment.")
        return redirect('appointment_request_detail', request_id=appointment_request.id)

def payment_cancelled(request):
    messages.info(request, "Payment was cancelled.")
    return redirect('appointment_request_list')


def appointment_request_detail(request, request_id):
    appointment_request = get_object_or_404(AppointmentRequest, id=request_id)
    context = {
        'appointment_request': appointment_request,
    }
    return render(request, 'appointment_request_detail.html', context)

@login_required
def approve_appointment_request(request, request_id):
    appointment_request = get_object_or_404(AppointmentRequest, id=request_id)

    # Check if the request is already approved
    if appointment_request.is_approved:
        # Redirect or handle case where it's already approved
        return redirect('appointment_request_detail', request_id=appointment_request.id)

    # Process approval (could involve more business logic)
    appointment_request.is_approved = True
    appointment_request.save()

    # Redirect or show success message
    return redirect('appointment_request_detail', request_id=appointment_request.id)

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment(request):
    if request.method == 'POST':
        # Get the token submitted by the form
        token = request.POST.get('stripeToken')

        try:
            # Create a charge: this will charge the user's card
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents, change as needed
                currency='usd',
                description='Example charge',
                source=token,
            )
        except stripe.error.CardError as e:
            # Display error message in case of card error
            return render(request, 'payment_error.html', {'error': e})

        # Payment successful
        return render(request, 'payment_success.html')

    # Render the payment form template
    return render(request, 'payment.html')

# stripe.api_key = settings.STRIPE_SECRET_KEY

# def charge(request):
#     if request.method == 'POST':
#         token = request.POST['stripeToken']

#         try:
#             # Use Stripe's library to make requests...
#             charge = stripe.Charge.create(
#                 amount=1000,  # Amount in cents
#                 currency='usd',
#                 description='Example charge',
#                 source=token,
#             )
#         except stripe.error.CardError as e:
#             # Since it's a decline, stripe.error.CardError will be caught
#             body = e.json_body
#             err = body.get('error', {})
#             return render(request, 'payment_error.html', {'error': err['message']})

#         return render(request, 'payment_success.html')

#     return render(request, 'payment.html')

stripe.api_key = settings.STRIPE_SECRET_KEY

def charge(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')

        try:
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency='usd',
                description='Example charge',
                source=token,  # Use the token as the payment source
            )
            # Payment successful - render success page or redirect
            return redirect('payment_success')

        except CardError as e:
            # Since it's a decline, CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            return render(request, 'payment_error.html', {'error': err.get('message')})

        except StripeError as e:
            # Display error message in payment form
            return render(request, 'payment_error.html', {'error': str(e)})

        except Exception as e:
            # Handle other exceptions
            return render(request, 'payment_error.html', {'error': str(e)})

    # Render the payment form template for GET requests
    return render(request, 'payment.html')


def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST['card_number']
        card_expiry = request.POST['expiry']
        card_cvv = request.POST['cvv']

        try:
            # Create a Stripe token for the card details
            token = stripe.Token.create(
                card={
                    'number': card_number,
                    'exp_month': card_expiry.split('/')[0].strip(),
                    'exp_year': card_expiry.split('/')[1].strip(),
                    'cvc': card_cvv,
                },
            )

            # Now charge the Stripe token
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency='usd',
                description='Example charge',
                source=token.id,  # Use the token as the payment source
            )

            # Payment successful - render success page or redirect
            return redirect('payment_success')

        except CardError as e:
            # Since it's a decline, CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            return render(request, 'payment_error.html', {'error': err.get('message')})

        except Exception as e:
            # Handle other exceptions
            return render(request, 'payment_error.html', {'error': str(e)})

    # Render the payment form template for GET requests
    return render(request, 'payment.html')

def payment_success(request):
    return render(request, 'payment_success.html')


def payment_error(request):
    return render(request, 'payment_error.html')

