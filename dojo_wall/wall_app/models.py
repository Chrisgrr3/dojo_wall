from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'The first name must be at least two characters long.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'The last name must be at least two characters long.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if len(postData['password']) < 8:
            errors['password'] = 'The password must contain at least eight characters.'
        if postData['password'] != postData['confirm_password']:
            errors['no_match_pass'] = 'Error. Please ensure to confirm your password correctly.'
        if len(User.objects.filter(email = postData['email'])) > 0:
            if postData['email'] == User.objects.filter(email = postData['email']).first().email:
                errors['duplicate_user'] = 'This user is already in the database. Please use your own, unique email.'
        return errors
    def validate_login(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])) == 0:
            errors['email_existence'] = 'This user is not currently in our database. Please register first.'
            return errors
        user = User.objects.filter(email = postData['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                print('Password correct. Directing to next page...')
            else:
                errors['password'] = 'Incorrect password, please try again.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    creator = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.ManyToManyField(Message, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
