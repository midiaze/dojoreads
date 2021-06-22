from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validacion_registro(self, post_data):
        errors = {}
        if len(post_data['name'])<2:
            errors['name'] = "El largo del nombre debe tener al menos 2 caracteres"
        if len(post_data['alias'])<2:
            errors['alias'] = "El largo del alias debe tener al menos 2 caracteres"
        if len (post_data['email']) <1:
            errors['email']= "Email es necesario"
        if post_data['password'] != post_data['confirm_password']:
            errors['password'] = 'Contraseñas no coinciden'
        if len(post_data['password']) < 8:
            errors['password']='Password debe tener al menos 8 caracteres'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email']= "Email no es válido"
        else:
            usuario = User.objects.filter(email=post_data['email'])
            if len(usuario)>0:
                errors['email'] = 'Email ya registrado, porfavor intentar otro email'
        return errors

    def validacion_login(self, post_data):
        login_errores = {}
        if len(post_data['email']) < 1:
            login_errores['email_login'] = 'Email es necesario'
        elif not EMAIL_REGEX.match(post_data['email']):
            login_errores['email_login']= "Email no es válido"
        else:
            email_existente = User.objects.filter(email=post_data['email'])
            if len(email_existente) == 0:
                login_errores['email_login'] = 'Este correo no está registrado'
                return login_errores
            else:
                usuario = email_existente[0]
            if not bcrypt.checkpw(post_data['password'].encode(), usuario.password.encode()):
                login_errores['password_login']='Password incorrecta'
        return login_errores

class BookManager(models.Manager):
    def validacion_libro(self, post_data):
        libro_errores = {}
        if len(post_data['title']) < 2:
            libro_errores['title'] = "El titulo debe tener al menos 2 caracteres"
        if len(post_data["author_exist"])<1:
            if len(post_data['author']) < 2:
                libro_errores['author'] = f"El autor debe tener al menos 2 caracteres, [ {post_data['author_exist']} ]"
            else:
                libro_existe = Book.objects.filter(title=post_data['title'], author=post_data['author'])
                if len(libro_existe) > 0:
                    libro_errores['title'] = 'Este libro ya está creado'
        else:
            libro_existe = Book.objects.filter(title=post_data['title'], author=post_data['author_exist'])
            if len(libro_existe) > 0:
                libro_errores['title'] = 'Este libro ya está creado'
        return libro_errores

class ReviewManager(models.Manager):
    def validacion_review(self, post_data):
        review_errores = {}
        if len(post_data['review'])<5:
            review_errores['review'] = 'La review debe tener al menos 5 caracteres'
        if not post_data['rating']:
            review_errores['rating'] = 'Seleccione un rating'
        return review_errores


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    class Meta:
        ordering = ['title']

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews_libro', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews_usuario', on_delete=models.CASCADE )
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

    class Meta:
        ordering = ['-updated_at']