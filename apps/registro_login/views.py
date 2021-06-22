from django.http.request import HttpRequest
from django.http.response import HttpResponse
from apps.registro_login.utils import login_required
from django.shortcuts import render, redirect
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request,"index.html")

def registro(request):
    errores = User.objects.validacion_registro(request.POST)
    if len(errores)>0:
        context = {
            'errors' : errores
        }
        return render(request,"index.html", context)
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user_nuevo = User.objects.create(name=request.POST['name'],alias= request.POST['alias'], email= request.POST['email'], password= hash1)
        request.session['id']= user_nuevo.id
        return redirect(f'/wall/{user_nuevo.id}')

def login(request):
    errores = User.objects.validacion_login(request.POST)
    if len(errores)>0:
        context = {
            'errors' : errores
        }
        return render(request,"index.html", context)
    else:
        usuario = User.objects.get(email=request.POST["email"])
        request.session["id"]=usuario.id
        return redirect(f'/wall/{usuario.id}')

@login_required
def wall(request, id_user):
    context = {
        'usuario': User.objects.get(id = id_user),
        'libros': Book.objects.all(),
        'reviews': Review.objects.all()[:3]
    }
    return render(request,"wall.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

@login_required
def agregar_libro(request):
    if request.method=="GET":
        autores = set()
        libros = Book.objects.all()
        for i in libros:
            autores.add(i.author)

        context = {
            'usuario': User.objects.get(id=request.session['id']),
            'libros': libros,
            'autores': autores
        }
        return render(request, "add.html", context)
    if request.method == "POST":
        errors = Book.objects.validacion_libro(request.POST)
        errors.update(Review.objects.validacion_review(request.POST))
        if len(errors)>0:
            context = {
                'usuario': User.objects.get(id=request.session['id']),
                'libros': Book.objects.all(),
                'errors': errors
            }
            return render(request, "add.html", context)
        else:
            if len(request.POST['author_exist'])<1:
                author = request.POST['author']
            else:
                author = request.POST['author_exist']
            libro_nuevo = Book.objects.create(
                title=request.POST['title'],
                author=author,
                )
            review_nueva = Review.objects.create(
                book = libro_nuevo,
                user = User.objects.get(id=request.session['id']),
                review = request.POST['review'],
                rating = request.POST['rating']
            )
            return redirect(f"/detalle_libro/{libro_nuevo.id}")

@login_required
def detalle_libro(request, id_book):
    if request.method == "GET":
        context = {
            'usuario': User.objects.get(id=request.session['id']),
            'libro': Book.objects.get(id=id_book),
            'reviews': Review.objects.filter(book=id_book),
        }
        return render(request,"detalle_libro.html", context)
    if request.method == "POST":
        errors = Review.objects.validacion_review(request.POST)
        review = Review.objects.filter(book=id_book)

        if len(errors)>0:
            context = {
            'usuario': User.objects.get(id=request.session['id']),
            'libro': Book.objects.get(id=id_book),
            'reviews': Review.objects.filter(book=id_book),
            'errors': errors,

            }
            return render(request,"detalle_libro.html", context)
        else:
            review_nueva = Review.objects.create(
                book = Book.objects.get(id=id_book),
                user = User.objects.get(id=request.session['id']),
                review = request.POST['review'],
                rating = request.POST['rating']
            )
            return redirect(f"/detalle_libro/{id_book}")

@login_required
def eliminar_review(request, id_review):
    review = Review.objects.get(id=id_review)
    libro = review.book
    review.delete()
    return redirect(f"/detalle_libro/{libro.id}")

@login_required
def perfil_usuario(request, id_user):
    context = {
        'usuario': User.objects.get(id=id_user)
    }
    return render(request,"perfil_user.html",context)
