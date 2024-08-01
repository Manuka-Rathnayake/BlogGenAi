from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai  as aai
#import openai
import yt_dlp
from openai import OpenAI
from .models import BlogPost


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
        

        title = yt_title(yt_link)
        print(title)

        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': 'Failed to get video transcript'}, status=400)
        
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': 'No blog content generated'}, status=404)
        
        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content
        )
        new_blog_article.save()

        return JsonResponse({'content': blog_content}) 
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

   # return JsonResponse({'message': 'Blog generated successfully'}, status=200)


def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
            base, ext = os.path.splitext(filename)
            new_file = f"{base}.mp3"
            return new_file
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None
"""
def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='settings.MEDIA_ROOT')
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file


def download_audio(link):
    try:
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()
        if not video:
            print("No audio stream found")
            return None
        out_file = video.download(output_path=settings.MEDIA_ROOT)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None
"""
def get_transcription(link):
   audio = download_audio(link)
   aai.settings.api_key = settings.ASSEMBLYAI_API_KEY

   transcriber = aai.Transcriber()
   transcript =  transcriber.transcribe(audio)

   return transcript.text
"""
def generate_blog_from_transcription(transcription):
    openai.api_key = ""
    prompt = f"Generate a blog post based on the following transcription, but dont make it look like a youtube video, make it look like a proper article:\n\n{transcription}\n\nArticle:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        max_tokens = 1000 
    )

    generated_content = response.choices[0].text.strip()

    return generated_content
"""
def generate_blog_from_transcription(transcription):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"Generate a blog post based on the following transcription, but dont make it look like a youtube video, make it look like a proper article:\n\n{transcription}\n\nArticle:"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates blog posts from transcriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        generated_content = response.choices[0].message.content.strip()
        return generated_content
    except Exception as e:
        print(f"Error generating blog content: {str(e)}")
        return None
    

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "blogs.html", {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article_details = BlogPost.objects.get(id=pk)
    if request.user == blog_article_details.user:
        return render(request, 'blog_details.html', {'blog_article': blog_article_details})
    else:
        return redirect('/')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatpassword = request.POST.get('repeatpassword')

        if password == repeatpassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = "Error creating account"
        else:
            error_message = "Password and Repeat Password does not match"
            return render(request, 'signup.html', {'error': error_message})
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)    
    return redirect('/')