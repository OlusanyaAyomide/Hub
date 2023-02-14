from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cloudinary.models import CloudinaryField
from .helper import QuestionAnswer,generator,QuestionYear as Qs,slugGenerator,MessageslugGenerator,customgenerator
from django.utils.text import slugify


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)
        

class UserData(AbstractUser):

    username = models.CharField(max_length = 200,null = True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

class Instituition(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="",blank=True)

    def __str__(self):
        return  f'{self.name}'

    def save(self,*args,**kwargs):
        if self.slug == "":
            passed = False
            value = ""
            while not passed:
                value = slugify(f"institution {self.name} {slugGenerator()}")
                if not Instituition.objects.filter(slug = value).exists():
                    passed = True
            self.slug = value
        super().save(*args,**kwargs)


class Subject(models.Model):
    name = models.CharField(max_length= 200)

    def __str__(self):
        return  f'{self.name}'




class Topic(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    



class Question(models.Model):
    questionText = models.TextField()
    optionA = models.CharField(max_length=500)
    optionB = models.CharField(max_length=500)
    optionC = models.CharField(max_length=500)
    optionD = models.CharField(max_length=500)
    answer = models.CharField(max_length=20,choices=QuestionAnswer)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null = True)
    Instituition = models.ManyToManyField(Instituition,related_name="question_inst")
    subject = models.ForeignKey(Subject,related_name="question_subject",on_delete=models.CASCADE)
    questionId = models.CharField(max_length = 10,editable=False,default = "")
    correctionImage = CloudinaryField("image",blank = True,null = True)
    correctionText = models.TextField(max_length=2000,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    questionYear = models.CharField(max_length=200,choices=Qs)
  

    def save(self,*args,**kwargs):
        if self.questionId == "":
            passed = False
            value = ""
            while not passed:
                value = generator()
                if not Question.objects.filter(questionId = value).exists():
                    passed = True
            self.questionId = value
        super().save(*args,**kwargs)

    def __str__(self):
        return  f'question {self.questionId}'

class PublicQuestion(models.Model):
    questionText = models.TextField()
    created = models.DateField(auto_now_add=True)
    createdBy = models.ForeignKey(UserData,on_delete=models.CASCADE,related_name="publicQuestion")
    isActive = models.BooleanField(default=True)
    title = models.CharField(max_length=2000)
    image = CloudinaryField("image",blank = True,null = True)
    slug = models.SlugField(default="",blank=True)
    
    def save(self,*args,**kwargs):
        if self.slug == "":
            passed = False
            value = ""
            while not passed:
                value = slugify(f"{self.title} public question {slugGenerator()}")
                if not PublicQuestion.objects.filter(slug = value).exists():
                    passed = True
            self.slug = value
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.questionText} {self.id}' 

class QuestionReply(models.Model):
    question = models.ForeignKey(PublicQuestion,on_delete=models.CASCADE,related_name="questionReply")
    replyBy = models.ForeignKey(UserData,on_delete=models.CASCADE,related_name="replies")
    upvotes = models.ManyToManyField(UserData,related_name="upvotes")
    downVotes = models.ManyToManyField(UserData,related_name="downvotes")
    isActive = models.BooleanField(default=False)
    replyText = models.CharField(max_length = 2000)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default="",blank=True)

    def __str__(self):
        return f'reply {self.replyText} {self.id}'

    class Meta:
        ordering = ("-created",)

    
    def save(self,*args,**kwargs):
        if self.slug == "":
            passed = False
            value = ""
            while not passed:
                value = slugify(f"{self.question.title} reply {slugGenerator()}")
                if not QuestionReply.objects.filter(slug = value).exists():
                    passed = True
            self.slug = value
        super().save(*args,**kwargs)


class InstitutionChat(models.Model):
    institution = models.OneToOneField(Instituition,related_name="instituteChat",on_delete=models.CASCADE)
    roomDescription = models.CharField(max_length=2000,null=True) 
    members = models.ManyToManyField(UserData,related_name="comMembers")
    groupAdmins = models.ManyToManyField(UserData,related_name="admin",blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="",blank=True)

    def __str__(self):
        return f'{self.institution} room chat' 

    def save(self,*args,**kwargs):
        if self.slug == "":
            passed = False
            value = ""
            while not passed:
                value = slugify(f"{self.name} chat room {slugGenerator()}")
                if not InstitutionChat.objects.filter(slug = value).exists():
                    passed = True
            self.slug = value
        super().save(*args,**kwargs)


class InstitutionMessage(models.Model):
    messageText = models.TextField(null = True)
    roomName = models.ForeignKey(InstitutionChat,on_delete=models.CASCADE,related_name="messages")
    messageBy = models.ForeignKey(UserData,on_delete=models.CASCADE,related_name="roomMessages")
    MessageTags = models.ForeignKey("self",null = True,on_delete=models.SET_NULL,blank = True)
    created = models.DateTimeField(auto_now_add=True)
    reactions = models.ManyToManyField(UserData,related_name="reactions",blank=True)
    slug = models.SlugField(default="",blank=True)

    def __str__(self):
        return self.messageText

    
    def save(self,*args,**kwargs):
        if self.slug == "":
            passed = False
            value = ""
            while not passed:
                value = slugify(f"{self.roomName.name} message {MessageslugGenerator()}")
                if not InstitutionMessage.objects.filter(slug = value).exists():
                    passed = True
            self.slug = value
        super().save(*args,**kwargs)


class FileList(models.Model):
    Instituition = models.ManyToManyField(Instituition,related_name="fileList")
    description = models.CharField(max_length = 200,null = True,blank = True)
    timeAdded = models.DateField(auto_now=True)
    file = models.FileField(upload_to="store/pdf")
    downloads = models.PositiveIntegerField(default=0)

class Userverify(models.Model):
    user = models.ForeignKey(UserData,on_delete=models.CASCADE)
    resetPassword = models.IntegerField()

