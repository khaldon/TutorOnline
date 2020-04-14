from django.core.exceptions import PermissionDenied
from .models import Course

def course_tutor(f):
    def wrap(request, *args, **kwargs):
        course = Course.objects.get(slug=kwargs['course'])
        if request.user == course.tutor:
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap