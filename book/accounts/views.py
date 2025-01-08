


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UploadedFiles
from .forms import UploadedFilesForm
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from functools import wraps
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializer import userserializer,LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializer import UploadedFilesSerializer



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = CustomUser.objects.create_user(username=username, password=password)
            return redirect('login')
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Check if user has uploaded books
            if has_uploaded_books(user):
                return redirect('upload_file')
            else:
                
                return redirect('upload_form')
        else:
            return HttpResponse("Invalid credentials! <br> <a href='/signup/'>Signup here</a>")
    
    return render(request, 'login.html')

def authors_and_sellers(request):
    users = CustomUser.objects.filter(public_visibility=True)
    users = users.order_by('username')
    return render(request, 'authors_and_sellers.html', {'users': users})

def has_uploaded_books(user):
    """
    Helper function to check if a user has uploaded any books
    """
    return UploadedFiles.objects.filter(user=user).exists()

def upload_form(request):
    """
    View to check if user has books and redirect accordingly
    """
    if not has_uploaded_books(request.user):
        # User has no books - show the no_books.html page with upload form
        if request.method == 'POST':
            form = UploadedFilesForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.save(commit=False)
                uploaded_file.user = request.user
                uploaded_file.save()
                messages.success(request, 'First book uploaded successfully!')
                return redirect('upload_file')
        else:
            form = UploadedFilesForm()
        
        return render(request, 'no_books.html', {'form': form})
    
    # User has books - redirect to regular upload page
    return redirect('upload_file')
@login_required
def upload_file(request):
    """
    Main dashboard view - only accessible if user has uploaded books
    """
    if not has_uploaded_books(request.user):
        messages.warning(request, "You need to upload at least one book first!")
        return redirect('upload_form')
    
    files = UploadedFiles.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = UploadedFilesForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            messages.success(request, 'Book uploaded successfully!')
            return redirect('upload_file')
    else:
        form = UploadedFilesForm()
    
    context = {
        'form': form,
        'files': files,
        'user': request.user
    }
    
    return render(request, 'uploadfiles.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    """
    View to check and redirect based on user's book status
    """
    if not has_uploaded_books(request.user):
        messages.warning(request, "You need to upload at least one book first!")
        return render(request, 'no_books.html')
    return redirect('upload_file')

class userApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset=CustomUser.objects.all()
        serializer=userserializer(queryset,many=True)
        return Response({
            "status": True,
            "data":serializer.data

        })
class LoginAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if  not serializer.is_valid():
             return Response({
            "status": False,
            "data":serializer.errors

        })
        username=serializer.data['username']
        password=serializer.data['password']
        
        user_obj=authenticate(username=username, password=password)
        if user_obj:
             token , _=Token.objects.get_or_create(user=user_obj)
             
             return Response({
            "status": True,
            "data":{'token':str(token)}

        })


        return Response({
            "status": False,
            "data":{},
            "message":"invalid credentials"

        })
    





class UserFilesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Fetch files uploaded by the authenticated user
        files = UploadedFiles.objects.filter(user=request.user)
        
        # Serialize the files
        serializer = UploadedFilesSerializer(files, many=True)
        
        return Response({
            'status': 'success',
            'count': files.count(),
            'files': serializer.data
        })  
