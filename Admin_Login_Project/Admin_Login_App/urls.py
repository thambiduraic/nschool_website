from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_login', views.admin_login_view, name='admin_login'),
    path('dashboard', views.dashboard_view, name='dashboard'),

    path('courses', views.course_view, name='courses'),
    path('course_page', views.course_page_view, name='course_page'),
    path('navbar_save_course', views.navbar_save_view, name='navbar_save_course'),
    path('update_course/<id>', views.update_course, name='update_course'),
    path('delete_course/<id>', views.delete_course),
    path('pdf', views.pdf, name='pdf'),
    

    # api urls

    # admin login
    path('admin_login_api', views.admin_login_api, name='admin_login_api'),
    path('get_admin_usernames', views.get_admin_usernames, name='get_admin_usernames'),

    # admin logout
    path('logout', views.logout_view),

    # course api
    path('course_api', views.courseApi, name='course_api'),
    path('course_api/<int:id>', views.courseApi, name='course_api'),

    # placement partners api
    path('partners_api', views.placementPartnersApi, name='partners_api'),
    path('update_partners_api/<int:id>', views.placementPartnersApi, name='update_partners_api'),
    path('delete_partners_api/<int:id>', views.placementPartnersApi, name='delete_partners_api'),

    # testimonial api
    path('testimonial_api', views.testimonialApi, name='testimonial_api'),
    path('update_testimonial_api/<int:id>', views.testimonialApi, name='update_testimonial_api'),
    path('delete_testimonial_api/<int:id>', views.testimonialApi, name='delete_testimonial_api'),

    # placement stories api
    path('placement_stories_api', views.placementStoriesApi, name='placement_stories_api'),
    path('update_placement_stories_api/<int:id>', views.placementStoriesApi, name='update_placement_stories_api'),
    path('delete_placement_stories_api/<int:id>', views.placementStoriesApi, name='delete_placement_stories_api'),

    # faq api
    path('faq_api', views.FaqApi, name='faq_api'),
    path('update_faq_api/<int:id>', views.FaqApi, name='update_faq_api'),
    path('delete_faq_api/<int:id>', views.FaqApi, name='delete_faq_api'),

    # blog api
    path('blog_api', views.BlogApi, name='blog_api'),
    path('update_blog_api/<int:id>', views.BlogApi, name='update_blog_api'),
    path('delete_blog_api/<int:id>', views.BlogApi, name='delete_blog_api'),

    # career api
    path('career_api', views.CareerApi, name='career_api'),
    path('update_career_api/<int:id>', views.CareerApi, name='update_career_api'),
    path('delete_career_api/<int:id>', views.CareerApi, name='delete_career_api'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)