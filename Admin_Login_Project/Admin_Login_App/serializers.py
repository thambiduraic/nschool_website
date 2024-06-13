from rest_framework import serializers
from Admin_Login_App.models import *

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses
        fields = ['id', 'Title', 'Description', 'Technologies', 'Images', 'status']

    def create(self, validated_data):
        Title = validated_data.get('id')
        Title = validated_data.get('Title')
        Description = validated_data.get('Description')
        Technologies = validated_data.get('Technologies')
        Images = validated_data.get('Images')
        status = validated_data.get('status')

        return courses.objects.create(
            Title = Title,
            Description = Description,
            Technologies = Technologies,
            Images = Images,
            status = status,
        )

class PlacementPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = partners_logo
        fields = ['name', 'logo']

    def create(self, validated_data):
        name = validated_data.get('name')
        logo = validated_data.get('logo')

        return partners_logo.objects.create(
            name = name,
            logo = logo,
        )

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['student_name', 'picture', 'course', 'date', 'testimonial']
    
    def create(self, validated_data):
        student_name = validated_data.get('student_name')
        picture = validated_data.get('picture')
        course = validated_data.get('course')
        date = validated_data.get('date')
        testimonial = validated_data.get('testimonial')

        return Testimonial.objects.create(
            student_name = student_name,
            picture = picture,
            course = course,
            date = date,
            testimonial = testimonial,
        )

class PlacementStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementStories
        fields = ['student_name', 'course', 'testimonial_video', 'date']


    def create(self, validated_data):
        student_name = validated_data.get('student_name')
        course = validated_data.get('course')
        testimonial_video = validated_data.get('testimonial_video')
        date = validated_data.get('date')

        return PlacementStories.objects.create(
            student_name = student_name,
            course = course,
            testimonial_video = testimonial_video,
            date = date,
        )

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
    
    def create(self, validated_data):
        question = validated_data.get('question')
        answer = validated_data.get('answer')

        return FAQ.objects.create(
            question = question,
            answer = answer,
        )

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['images', 'title', 'description', 'course']
    
    def create(self, validated_data):
        images = validated_data.get('images')
        title = validated_data.get('title')
        description = validated_data.get('description')
        course = validated_data.get('course')

        return Blog.objects.create(
            images = images,
            title = title,
            description = description,
            course = course,
        )

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = ['Logo', 'Job_Heading', 'Location', 'Experience', 'No_Of_Openings', 'Salary', 'Status', 'Job_Type', 'Qualification', 'Job_Description', 'Skills_Required']

    def create(self, validated_data):
        Logo = validated_data.get('Logo')
        Job_Heading = validated_data.get('Job_Heading')
        Location = validated_data.get('Location')
        Experience = validated_data.get('Experience')
        No_Of_Openings = validated_data.get('No_Of_Openings')
        Salary = validated_data.get('Salary')
        Status = validated_data.get('Status')
        Job_Type = validated_data.get('Job_Type')
        Qualification = validated_data.get('Qualification')
        Job_Description = validated_data.get('Job_Description')
        Skills_Required = validated_data.get('Skills_Required')

        return Careers.objects.create(
            Logo = Logo,
            Job_Heading = Job_Heading,
            Location = Location,
            Experience = Experience,
            No_Of_Openings = No_Of_Openings,
            Salary = Salary,
            Status = Status,
            Job_Type = Job_Type,
            Qualification = Qualification,
            Job_Description = Job_Description,
            Skills_Required = Skills_Required,
        )