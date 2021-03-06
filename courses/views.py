from django.shortcuts import render,redirect,get_object_or_404
from .models import Course,OrderCourse,Order,Payment,PaymentInfo,Wishlist,CourseSections,SectionVideos, Review
from .models import Course,OrderCourse,Order,Payment,PaymentInfo,Wishlist,CourseSections,SectionVideos,Review
from .forms import (CheckoutForm,CourseForm1,CourseForm2,CourseForm3,
                   CourseForm4,SectionForm,SectionVideoForm, 
                   SearchStudentForm,ReviewForm)

# from notifications.signals import notify
from users.decorators import teacher_required
from django.contrib.auth.decorators import login_required
from .decorators import course_tutor
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import View,ListView,RedirectView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from guardian.shortcuts import assign_perm
from users.models import CustomUser
from django.contrib.postgres.search import SearchVector
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .documents import CourseDocument
from .filters import CourseFilter 
from django.db.models import Count
import os
import stripe



# Create your views here.


def section_delete_course(request, slug, id):
    course  = get_object_or_404(Course,slug=slug)
    course_section = CourseSections.objects.get(course=course, id=id)
    course_section.delete()
    return HttpResponseRedirect("/courses/creation_content/")
    

def delete_course(request, slug):
    course  = get_object_or_404(Course, slug=slug)
    course.delete()
    return HttpResponseRedirect("/")



def creation_course_content(request, slug):
    course = get_object_or_404(Course, slug=slug)
    section_form = SectionForm(**{'user': request.user})
    video_form = SectionVideoForm(**{'user': request.user})
    if request.method == 'POST':
        section_form = SectionForm(request.POST,request.FILES,user=request.user)
        video_form = SectionVideoForm(request.POST,request.FILES,user=request.user)

        if section_form.is_valid():
            new_section = section_form.save()
            new_section.creator = request.user
            new_section.course = course
            new_section.save()
            return redirect('/')

        if video_form.is_valid():
            new_video = video_form.save()
            new_video.save()
            return redirect(new_video.get_absolute_url())
    else:
        section_form = SectionForm(user=request.user)
        video_form = SectionVideoForm(user=request.user)

    return render(request, 'courses/creation_course_content.html',{'section_form':section_form,'video_form':video_form})


def CourseView(request,slug):
    course = get_object_or_404(Course,slug=slug)
    sections = CourseSections.objects.filter(course__title=course.title)
    videos = SectionVideos.objects.filter(section__course__title=course.title)
    reviews = course.reviews.filter(active=True)
    post_commented =  Review.objects.filter(reviewer=request.user)

    new_review = None
    if request.method == 'POST':    
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.course = course
            new_review.reviewer = request.user
            new_review.save()    
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        review_form = ReviewForm()
    context = {'course':course,'sections':sections,'videos':videos,
                               'reviews':reviews,'new_review':new_review,
                               'review_form':review_form,
                               'post_commented':post_commented,
              }
    return render(request,'courses/course_detail.html', context)

# def delete_comment(request, slug):
#     course = get_object_or_404(Course,slug=slug)
    





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


class CoursesList(ListView):
    model = Course
    template_name='courses/courses.html'
    context_object_name = 'courses'

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

            return render(self.request,'courses/cart.html',{'object':order})

        except ObjectDoesNotExist:
            # messages.error(self.request,"You do not have an active order")
            return render(self.request,'courses/cart.html')
@login_required
def add_to_cart(request,pk):
    course = get_object_or_404(Course,pk=pk)

    order_course, created = OrderCourse.objects.get_or_create(
        course=course,
        user=request.user,
        ordered = False,
    )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.courses.filter(course__pk=course.pk).exists():
            messages.info(request, "You already have this course in the cart")
            return redirect("courses:cart")
        else:
            order.courses.add(order_course)
            messages.info(request, "This course was added to your cart.")
            return redirect("courses:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        messages.info(request, "You already have this course in the cart")
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
            return render(self.request,"courses/checkout.html",context)
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
                return redirect('courses:payment')
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
            # user =  self.request.user.username
            print("user", payment.user)
            print("order", order)
            assign_perm('perm_payment', payment.user, order)

            
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
            messages.warning(self.request,"A serious error occurred. We have been notifed.")
            return redirect("/")

class MyCourses(LoginRequiredMixin,ListView):
    model = Course
    paginate_by = 10
    template_name = 'courses/my_courses.html'
    context_object_name = 'mygroups'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist'] = Wishlist.objects.all()
        context['wuser'] = Wishlist.objects.filter(user=self.request.user)
        return context

    def get_queryset(self,**kwargs):
        user = get_object_or_404(CustomUser,username=self.request.user.username)
        return user.tutor_courses.all()

def course_filter(request):
    f = CourseFilter(request.GET, queryset=Course.objects.all())
    return render(request, 'courses/course_filter.html',{'filter':f})

@login_required
def add_to_wishlist(request,slug):
    data = dict()
    user = request.user
    course = get_object_or_404(Course,slug=slug)
    # wished_course,created = Wishlist.objects.get_or_create(wished_course=course,slug=course.slug,user=request.user,)
    if course in user.wish_courses.all():
        course.wish_course.remove(user)
        data['is_wished'] = False
    else:
        course.wish_course.add(user)
        data['is_wished'] = True
    data['total_points'] = course.wish_course.count()
    return JsonResponse(data)

class WishListView(ListView):
    model = Course
    template_name = 'courses/wishlist.html'
    paginate_by = 10
    context_object_name = 'wishlist'

    def get_queryset(self):
        # return Wishlist.objects.filter(user=self.request.user)
        user = self.request.user 
        return user.wish_courses.all() 
        
class FormWizardView(SessionWizardView):
    template_name = 'courses/create_course.html'
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'courses'))
    form_list = (CourseForm1,CourseForm2,CourseForm3,CourseForm4)

    def done(self,form_list,form_dict,**kwargs):
        instance = Course()
        instance.tutor = self.request.user
        for form in form_list:
            for field, value in form.cleaned_data.items():
                setattr(instance, field, value)
        instance.save()
        return redirect('courses:my_courses',username=self.request.user.username)


@login_required
def add_section_to_course(request, slug):
    course  = get_object_or_404(Course, slug=slug)
    section_form = SectionForm(**{'user': request.user})
    if request.method == 'POST':
        section_form = SectionForm(request.POST,request.FILES,user=request.user)
        if section_form.is_valid():
            new_section = section_form.save()
            new_section.creator = request.user
            new_section.course = course
            new_section.save()
            return redirect(new_section.get_absolute_url())
    else:
        section_form = SectionForm(user=request.user)
    return render(request,'courses/create_section.html',{'section_form':section_form})


def course_search(request):
    f = CourseFilter(request.GET, queryset=Course.objects.all())
    return render(request,'courses/student_course_search.html', {'filter':f})

def course_search_teacher(request):
    user = get_object_or_404(CustomUser,username=request.user.username)
    f = CourseFilter(request.GET, queryset=user.tutor_courses.all())
    return render(request,'courses/teacher_search.html', {'filter':f})


@login_required
def add_video_to_section(request):
    video_form = SectionVideoForm(**{'user': request.user})
    if request.method == 'POST':
        video_form = SectionVideoForm(request.POST,request.FILES,user=request.user)
        if video_form.is_valid():
            new_video = video_form.save()
            new_video.save()
            return redirect(new_video.get_absolute_url())
    else:
        video_form = SectionVideoForm(user=request.user)
    return render(request,'courses/create_video.html',{'video_form':video_form})

@login_required
def VideoView(request,pk,slug):
    course = get_object_or_404(Course,slug=slug)
    sections = CourseSections.objects.filter(course__title=course.title)
    videos = SectionVideos.objects.filter(section__course__title=course.title).order_by('created')
    wishlist = Wishlist.objects.all()
    video = get_object_or_404(SectionVideos,pk=pk)
    if video.watched == False:
        video.watched = True
        video.save()
    return render(request,'courses/video_detail.html',{'video':video,'course':course,'wishlist':wishlist})

@login_required
def delete_review(reuqest,pk):
    review = get_object_or_404(Review,pk=pk)
    review.delete()
    return HttpResponse('This review has been deleted.')
