
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from .forms import *
from .models import *

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
from Admin_Login_App.serializers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes

import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image as PILImage
import requests
from datetime import datetime
import os

# Create your views here.
# ----------------------------- Admin Login ----------------------------
def admin_login_view(request):
    return render(request, 'Admin_Login_App/AdminLogin.html')

def dashboard_view(request):
    return render(request, 'Admin_Login_App/Admin_Body.html')

# admin login api

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_login_api(request):    
    un = request.data.get('username')
    pw = request.data.get('password')

    try:
        admin_login = AdminLogin.objects.get(username=un)
    except AdminLogin.DoesNotExist:
        return Response({'error': 'Username does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=un, password=pw)
    
    if user is None or not user.is_staff:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, created = Token.objects.get_or_create(user=user)

    
    return Response({
            'user_info': {
                'id' : user.id,
                'username' : user.username,
                'email' : user.email,
            },
            'token' : token.key
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_admin_usernames(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info': {
                'id' : user.id,
                'username' : user.username,
                'email' : user.email,
            },
        })

    return Response({'error': 'not authenticated'}, status=400)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('admin_login')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

# ---------------------------- admin login end ----------------------------------

# ---------------------------- course api ---------------------------------------

def course_view(request):
    data = courses.objects.order_by('Title').all()
    paginator = Paginator(data, 5)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'Admin_Login_App/courses.html', {'page_obj': page_obj})

def course_page_view(request):
    data = CoursesForm()
    return render(request, 'Admin_Login_App/course_page.html', {'form':data})

def navbar_save_view(request):
    return render(request, 'Admin_Login_App/navbar_save_course.html')

# courses update
def update_course(request, id):
    course = courses.objects.get(id=id)
    form = UpdataCourseForm(instance=course)
    return render(request, 'Admin_Login_App/course_update.html', {'form': form, 'datas': course})

# delete course
def delete_course(request, id):
    obj = courses.objects.get(id=id)    
    return render(request, 'Admin_Login_App/navbar.html', {'datas': obj})

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def courseApi(request, id=0):
    # Check authentication
    if not request.user.is_authenticated:
        return Response({'error': 'not authenticated'}, status=400)
    
    if request.method == 'POST':
        course_serializer = CourseSerializer(data=request.data)
        if course_serializer.is_valid():
            course_serializer.save()
            return Response("Added Successfully")
        return Response(course_serializer.errors, status=400)

    elif request.method == 'GET':
        if id == 0:
            course = courses.objects.all()
            course_serializer = CourseSerializer(course, many=True)
            return Response(course_serializer.data)
        else:
            try:
                course = courses.objects.get(id=id)
                course_serializer = CourseSerializer(course)
                return Response(course_serializer.data)
            except courses.DoesNotExist:
                return Response("Course does not exist", status=404)

    elif request.method == 'PUT':
        try:
            course = courses.objects.get(id=id)
            course_serializer = CourseSerializer(course, data=request.data)
            if course_serializer.is_valid():
                course_serializer.save()
                return Response("Updated Successfully")
            return Response(course_serializer.errors, status=400)
        except courses.DoesNotExist:
            return Response("Course does not exist", status=404)

    elif request.method == 'DELETE':
        if id == 0:
            ids = request.data.get('ids', [])
            if not isinstance(ids, list):
                return Response({"error": "Invalid data format. 'ids' should be a list."}, status=400)
            
            non_existent_ids = []
            for course_id in ids:
                try:
                    course = courses.objects.get(id=course_id)
                    course.delete()
                except courses.DoesNotExist:
                    non_existent_ids.append(course_id)

            if non_existent_ids:
                return Response({"message": "Some courses do not exist", "non_existent_ids": non_existent_ids}, status=404)
            
            return Response({"message": "Deleted Successfully"}, status=200)
        else:
            try:
                course = courses.objects.get(id=id)
                course.delete()
                return Response({"message": "Deleted Successfully"}, status=200)
            except courses.DoesNotExist:
                return Response({"error": "Course does not exist"}, status=404)
       
        
# -------------------------------- course api end ---------------------------------

# Placement Partners Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def placementPartnersApi(request, id=0):
    
    if request.method == 'POST':
        placement_partners_serializer = PlacementPartnersSerializer(data = request.data)
        if placement_partners_serializer.is_valid():
            placement_partners_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        partners = partners_logo.objects.all()
        placement_partners_serializer = PlacementPartnersSerializer(partners, many=True)
        return JsonResponse(placement_partners_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        partners_data = request.data
        partners = partners_logo.objects.get(id=id)
        placement_partners_serializer = PlacementPartnersSerializer(partners, data=partners_data)
        if placement_partners_serializer.is_valid():
            placement_partners_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            partners = partners_logo.objects.get(id=id)
            partners.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)


# Testimonial Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def testimonialApi(request, id=0):
    
    if request.method == 'POST':
        testimonial_serializer = TestimonialSerializer(data = request.data)
        if testimonial_serializer.is_valid():
            testimonial_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial, many=True)
        return JsonResponse(testimonial_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        testimonial_data = request.data
        testimonial = Testimonial.objects.get(id=id)
        testimonial_serializer = TestimonialSerializer(testimonial, data=testimonial_data)
        if testimonial_serializer.is_valid():
            testimonial_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            testimonial = Testimonial.objects.get(id=id)
            testimonial.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# PlacementStories Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def placementStoriesApi(request, id=0):
    
    if request.method == 'POST':
        placement_stories_serializer = PlacementStoriesSerializer(data = request.data)
        if placement_stories_serializer.is_valid():
            placement_stories_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        placement_stories = PlacementStories.objects.all()
        placement_stories_serializer = PlacementStoriesSerializer(placement_stories, many=True)
        return JsonResponse(placement_stories_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        placement_stories_data = request.data
        placement_stories = PlacementStories.objects.get(id=id)
        placement_stories_serializer = PlacementStoriesSerializer(placement_stories, data=placement_stories_data)
        if placement_stories_serializer.is_valid():
            placement_stories_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            placement_stories = PlacementStories.objects.get(id=id)
            placement_stories.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# FAQ Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def FaqApi(request, id=0):
    
    if request.method == 'POST':
        faq_serializer = FaqSerializer(data = request.data)
        if faq_serializer.is_valid():
            faq_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        faq = FAQ.objects.all()
        faq_serializer = FaqSerializer(faq, many=True)
        return JsonResponse(faq_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        faq_data = request.data
        faq = FAQ.objects.get(id=id)
        faq_serializer = FaqSerializer(faq, data=faq_data)
        if faq_serializer.is_valid():
            faq_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            faq_serializer = FAQ.objects.get(id=id)
            faq_serializer.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# Blog Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def BlogApi(request, id=0):
    
    if request.method == 'POST':
        blog_serializer = BlogSerializer(data = request.data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        blog = Blog.objects.all()
        blog_serializer = BlogSerializer(blog, many=True)
        return JsonResponse(blog_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        blog_data = request.data
        blog = Blog.objects.get(id=id)
        blog_serializer = BlogSerializer(blog, data=blog_data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            blog_serializer = Blog.objects.get(id=id)
            blog_serializer.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# Careers Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def CareerApi(request, id=0):
    
    if request.method == 'POST':
        career_serializer = CareerSerializer(data = request.data)
        if career_serializer.is_valid():
            career_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        career = Careers.objects.all()
        career_serializer = CareerSerializer(career, many=True)
        return JsonResponse(career_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        career_data = request.data
        career = Careers.objects.get(id=id)
        career_serializer = CareerSerializer(career, data=career_data)
        if career_serializer.is_valid():
            career_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            career_serializer = Careers.objects.get(id=id)
            career_serializer.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)
        

# PDF file creation

def pdf(request):
    data = courses.objects.all()
    field_count = 6  # Assuming you have 6 fields initially
    field_height = 20  # Height of each field
    total_height = len(data) * field_count * field_height

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=(letter[0], total_height))
    p.setFont('Times-Roman', 14)
    y_position = total_height - 20  # Starting from the top of the page
    
    for courses_obj in data:
        # Calculate the dynamic height required for the course title
        name_height = 20 + (len(courses_obj.Title) // 20) * 20 

        # Draw course details
        data_row = f"Course Name: {courses_obj.Title}, Technologies: {courses_obj.Technologies}, Description: {courses_obj.Description}, Status: {courses_obj.status}"
        p.drawString(20, y_position, data_row)
        y_position -= 20 + name_height  # Adjust for the title height

        # Draw the image
        try:
            response = requests.get(courses_obj.Images, stream=True)
            if response.status_code == 200:
                image = PILImage.open(response.raw)
                image_path = f"image_{courses_obj.id}.png"  # Example: Use some unique identifier in the filename
                image.save(image_path)
                p.drawImage(image_path, 20, y_position - 100, width=100, height=100)
                y_position -= 120  # Adjust for the image height plus some spacing
        except Exception as e:
            p.drawString(20, y_position, f"Image could not be loaded: {str(e)}")
            y_position -= 20  # Space for the error message

        # Check if a new page is required
        if y_position <= 50:
            p.showPage()
            p.setFont('Times-Roman', 14)  # Reset font for the new page
            y_position = total_height - 20
    
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    
    # Save the file
    buffer.seek(0)
    x = datetime.now()
    date_format = x.strftime("%Y-%m-%d")
    time_format = x.strftime("%Hhr-%Mm-%Ss")
    save_path = 'pdf/formapp_{}_{}.pdf'.format(date_format, time_format)
    
    with open(save_path, 'wb') as f:
        f.write(buffer.getbuffer())
    
    return HttpResponse(f"PDF file has been generated and saved at: {save_path}")
