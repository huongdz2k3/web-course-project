import django.db.models.deletion
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
import random

class Categories(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_all_category(self):
        return Categories.objects.all().order_by('id')

class Author(models.Model):
    author_profile = models.ImageField(upload_to="Media/author")
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language

class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )
    COURSE_TYPE = (
        ('FREE', 'FREE'),
        ('PAID', 'PAID'),
    )
    featured_image = models.FileField(upload_to="Media/featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    course_type = models.CharField(choices=COURSE_TYPE,max_length=4, default='FREE')
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
    deadline = models.CharField(max_length=100,null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    has_certificate = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})
    
    def instructor_get_absolute_url(self):
        from django.urls import reverse
        return reverse("instructor_course_details", kwargs={'slug': self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


USER_ROLE = (
        ('Learner','Learner'),
        ('Instructor', 'Instructor'),
    )
class Role(models.Model):
    role = models.CharField(choices=USER_ROLE, blank=False, max_length=10, null=False)
    
    def __str__(self):
        return self.role

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course_review = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.course_review + " - " + self.comment

class What_you_learn(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points

class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " -  " + self.course.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("lesson_details", kwargs={'slug': self.id})

class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail",null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lessson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    description = models.TextField(null=True)
    youtube_id = models.CharField(max_length=200, null=True, blank=True)
    video_file = models.FileField(upload_to='ProtectedVideoLectures', null=True, blank=True)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("video_lecture_details", kwargs={'slug': self.youtube_id})

# class PUBLIC_VIDEO(Video):
#         youtube_id = models.CharField(max_length=200, null=True)
#
#         def get_absolute_url(self):
#             from django.urls import reverse
#             return reverse("video_lecture_details", kwargs={'slug': self.youtube_id})

# class PROTECTED_VIDEO(Video):
#         video_file = models.FileField(upload_to='/ProtectedVideoLectures')

class UserCourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title


    
class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

    print(role)

    def __str__(self):
        return self.user.username + " - " + self.role.role


class Payment(models.Model):
    order_id = models.CharField(max_length=100,null=True,blank=True)
    user_course = models.ForeignKey(UserCourse,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    country = models.CharField(max_length=100, default="")
    address_1 = models.CharField(max_length=255, default="")
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    postcode = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=100, default="")
    order_comments = models.TextField(blank=True)
    total = models.IntegerField(null=False, default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " -- " + self.course.title

difficulties = (
    ('Easy','Easy'),
    ('Medium','Medium'),
    ('Hard','Hard'),
)
class Quizzes(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE, null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    topic = models.CharField(max_length=100)
    number_of_questions = models.IntegerField(null=True)
    time_duration = models.IntegerField(null=True)
    require_passing_score = models.IntegerField(null=True)
    status = models.BooleanField(default=False)
    total_attempts = models.IntegerField(null=True)
    difficulty_level = models.CharField(choices=difficulties,max_length=100,null=True)

    def __str__(self):
        return self.topic + " - " + self.course.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("quiz_details", kwargs={'slug': self.slug})
    
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]


def create_slug_quizzes(instance, new_slug=None):
    slug = slugify(instance.topic)
    if new_slug is not None:
        slug = new_slug
    qs = Quizzes.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug_quizzes(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver_quizzes(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_quizzes(instance)

pre_save.connect(pre_save_post_receiver_quizzes, Quizzes)

class Question(models.Model):
    text = models.CharField(max_length=1000)
    quizzes = models.ForeignKey(Quizzes,on_delete=models.CASCADE)
    point = models.IntegerField(default=25)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.text
    
    def get_answers(self):
        return self.answer_set.all()

    def get_question_with_answers(self):
        answers = self.get_answers()
        question_info = {
            "question_text": self.text,
            "point": self.point,
            "status": self.status,
            "answers": [
                {"text": answer.text, "correct": answer.correct}
                for answer in answers
            ]
        }
        return question_info

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("question_details", kwargs={'slug': self.id})
class Answer(models.Model):
    text = models.CharField(max_length=100)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizzes,on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    attempt = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " - " + self.quiz.topic

class Watch_Duration(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    time_duration = models.IntegerField(null=True)
    is_done = models.BooleanField(default=False)

class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50] + " " + str(self.updated)
    
GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

LEVEL = (
    ("Fresher", "Fresher"),
    ("Junior", "Junior"),
    ("Senior", "Senior"),
)

LEVEL = (
    ("Fresher", "Fresher"),
    ("Junior", "Junior"),
    ("Senior", "Senior"),
)

POSITION = (
    ("Software Engineer", "Software Engineer"),
    ("AI Engineer", "AI Engineer"),
    ("Data Scientist", "Data Scientist"),
    ("IOS Developer", "IOS Developer"),
    ("Android Developer", "Android Developer"),
    ("UI/UX Designer", "UI/UX Designer"),
)

#LEARNER
class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='Media/avatar',default='Media/avatar/default_avatar.png')
    First_Name = models.CharField(max_length=50, default="")
    Last_Name = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=6, choices=GENDER)
    status = models.BooleanField(default=False)                        
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


    @property
    def get_name(self):
        return self.First_Name+" "+self.Last_Name

    @property
    def get_id(self):
        return self.id

    def __str__(self):
        return self.First_Name+" "+self.Last_Name

#INSTRUCTOR
class Instructor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=50, default="")
    Last_Name = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=6, choices=GENDER)
    position = models.CharField(max_length=50, choices=POSITION, default="")
    phone = models.CharField(max_length=10, null=True)
    status = models.BooleanField(default=False)
    level= models.CharField(max_length=50,choices=LEVEL)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    cv = models.FileField(upload_to="Media/authorCV")
    avatar = models.ImageField(upload_to='Media/avatar', default='Media/avatar/default_avatar.png')

    @property
    def get_name(self):
        return self.First_Name+" "+self.Last_Name
    
    @property
    def get_id(self):
        return self.id

    def __str__(self):
        return "{} ({})".format(self.First_Name+" "+self.Last_Name,self.level)
    
class Certificate(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    userID = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')
    courseID = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')

# class Room(models.Model):
#     host = models.ForeignKey(User,on_delete=models.CASCADE)
#     topic =  models.ForeignKey(Categories,on_delete=models.CASCADE)
#     course = models.ForeignKey(Course,on_delete=models.CASCADE)
#     description = models.TextField(null=True, blank=True)
#     name = models.CharField(max_length=200, default="Room")
#     participants = models.ManyToManyField(User, related_name='participants', blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-updated', '-created']
#
#     def __str__(self):
#         return self.topic.name
#
#
# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-updated', '-created']
#
#     def __str__(self):
#         return self.body[0:50]
#
# class UserRoom(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.first_name + " - " + self.room.name