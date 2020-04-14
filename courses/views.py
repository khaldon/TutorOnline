from django.shortcuts import render,redirect,get_object_or_404
from .models import Course,OrderCourse,Order,Payment,PaymentInfo
from .forms import CourseForm,CheckoutForm,CourseForm1,CourseForm2,CourseForm3,CourseForm4
from users.decorators import teacher_required
from django.contrib.auth.decorators import login_required
from .decorators import course_tutor
from django.http import HttpResponseRedirect
from django.views.generic import View,ListView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import stripe
from users.models import CustomUser
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# Create your views here.

@login_required
@course_tutor
def edit_course(request,course):
    course = get_object_or_404(Course,slug=course)
    if request.method == 'POST':
        course_form = CourseForm(instance=course,data=request.POST,files=request.FILES)
        if course_form.is_valid():
            course_form.save()
            return redirect(course.get_absolute_url())
        else:
            course_form = CourseForm(instance=course)
    else:
        course_form = CourseForm(instance=course)
    return render(request,'courses/edit_course.html',{'course_form':course_form})

@login_required
def enroll_to_free_course(request,course):
    course = get_object_or_404(Course,slug=course)
    user = request.user
    course.students.add(user)
    return HttpResponseRedirect(Course.get_absolute_url(course))

@login_required
def enroll_to_paid_course(request,course):
    course = get_object_or_404(Course,slug=course)

class CartView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object':order
            }
            return render(self.request,'courses/cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect("/")

@login_required
def add_to_cart(request,pk):
    course = get_object_or_404(Course,pk=pk)
    order_course = OrderCourse.objects.get_or_create(
        course=course,
        user=request.user,
        ordered = False,
    )
    ordered_date = timezone.now()
    order = Order.objects.create(user=request.user,ordered_date=ordered_date)
    order.courses.add(order_course)
    messages.info(request,"This course was added to your cart.")
    return redirect("courses:cart")

@login_required
def remove_from_cart(request,pk):
    course = get_object_or_404(Course,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.courses.filter(course__pk=course.pk).exists():
            order_course = OrderCourse.objects.filter(
                course=course,
                user=request.user,
                ordered = False,
            )[0]
            order.courses.remove(order_course)
            messages.info(request,"This course was removed from your cart.")
            return redirect("courses:cart")
        else:
            messages.info(request,"This product was not in your cart.")
            return redirect("courses:courses")
    else:
        messages.info(request,"You do not have an active order.")
        return redirect("courses:courses")

stripe.api_key = "sk_test_LV84oXAHus7lmnQAluhvBNhD007lApVItl"

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            form = CheckoutForm()
            context = {
                'form':form,
                'order':order,
            }
            return render(self.request,"checkout.html",context)
        except ObjectDoesNotExist:
            messages.info(self.request,"You do not have an active order")
            return redirect("core:checkout")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                firstname = form.cleaned_data.get('first_name')
                lastname = form.cleaned_data.get('last_name')
                if is_valid_form([firstname,lastname]):
                    payment_info = PaymentInfo(
                        user=self.request.user,
                        first_name=firstname,
                        last_name=lastname
                    )
                    payment_info.save()
                    order.payment_info = payment_info
                    order.save()
                else:
                    messages.info(
                        self.request, "Please fill in the required fields")
                return redirect('courses:payment',payment_option='stripe')
        except ObjectDoesNotExist:
            messages.warning(self.request,"You do not have an active order")
            return redirect("courses:cart")

class PaymentView(View):
    def get(self,*args,**kwargs):
        return render(self.request,"courses/payment.html")

    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order_courses = order.courses.all()
            order_courses.update(ordered=True)
            for course in order_courses:
                course.save()
            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request,"Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.warning(self.request,F"{e.error.message}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            messages.warning(self.request,"Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request,"Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            messages.warning(self.request,"Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            messages.warning(self.request,"Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            messages.warning(self.request,"Something went wrong. Your were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            messages.warning    (self.request,"A serious error occurred. We have been notifed.")
            return redirect("/")

class MyCourses(LoginRequiredMixin,ListView):
    model = Course
    paginate_by = 10
    template_name = 'courses/my_courses.html'
    context_object_name = 'mygroups'

    def get_queryset(self,**kwargs):
        user = get_object_or_404(CustomUser,username=self.request.user.username)
        return user.course_students.all()

class CourseWishlistAdd(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        slug = self.kwargs.get("slug")
        course = get_object_or_404(Course,slug=slug)
        url_ = course.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in course.wishlist.all():
                course.wishlist.remove(user)
            else:
                course.wishlist.add(user)
        return url_

class Wishlist(LoginRequiredMixin,ListView):
    model = CustomUser
    paginate_by = 10
    template_name = 'courses/wishlist.html'
    context_object_name = 'wishlist'

    def get_queryset(self,**kwargs):
        user = get_object_or_404(CustomUser,username=self.request.user.username)
        return user.wcourses.all()
        
class FormWizardView(SessionWizardView):
    template_name = 'courses/create_course.html'
    form_list = [CourseForm1,CourseForm2,CourseForm3,CourseForm4]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'courses'))

    def done(self, form_list, **kwargs):
        return render(self.request, 'courses/done.html',{'form_data': [form.cleaned_data for form in form_list],})