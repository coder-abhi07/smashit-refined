import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from .forms import UserUpdateForm, CustomUserSignupForm

def textResponse(request):
    """Extract text using OCR.space, apply clustering, and display the result."""
    if request.method == 'POST' and request.FILES.getlist('myfile'):
        parsed_text = extract_text_from_files(request.FILES.getlist('myfile'))
        if not parsed_text:
            return custom_error_view(request)

        ocr_text = "\n".join(parsed_text).strip()
        if not ocr_text:
            return custom_error_view(request)

        clustered_text = cluster_with_gemini(ocr_text)
        return render(request, "result.html", {"clustered_text": clustered_text})
    
    return custom_bad_request_view(request)

def extract_text_from_files(files):
    """Extract text from uploaded files using OCR.space."""
    api_key = settings.OCR_API_KEY
    payload = {"apikey": api_key, "OCREngine": 2, "isTable": True}
    parsed_text = []
    
    for file in files:
        response = requests.post("https://api.ocr.space/parse/image", files={file.name: file}, data=payload)
        if response.status_code != 200:
            return None
        
        results = response.json()
        if results.get("IsErroredOnProcessing", False):
            return None
        
        for result in results.get("ParsedResults", []):
            parsed_text.append(result.get("ParsedText", "").strip())
    
    return parsed_text

def cluster_with_gemini(text):
    """Send extracted text to Gemini API and get clustered questions."""
    api_key = settings.GEMINI_API_KEY
    if not text.strip():
        return "No text available for clustering."

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    data = {
        "contents": [{"parts": [{"text": f"Cluster the following questions into relevant categories:\n\n{text}\n\nGroup them under appropriate topics."}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        return format_clustered_text(result)
    except requests.exceptions.RequestException as e:
        return f"<div>Error processing with Gemini: {str(e)}</div>"

def format_clustered_text(result):
    """Format the clustered text received from the Gemini API."""
    raw_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No clustering result.")
    clustered_text = '<div id="clustered-text">'
    clusters = raw_text.split("\n\n")

    for i, cluster in enumerate(clusters):
        lines = cluster.split("\n")
        if lines:
            clustered_text += f'<div class="cluster"><h2>Cluster {i+1}</h2><p>'
            clustered_text += "<br>".join(lines)
            clustered_text += "</p></div>"

    clustered_text += "</div>"
    return clustered_text

def custom_error_view(request, exception=None):
    return render(request, "500.html")

def custom_bad_request_view(request, exception=None):
    return render(request, "400.html")

def about(request):
    return render(request, "about.html")

def index(request):
    return render(request, "index.html")
@login_required
def change_password(request):
    return handle_password_change(request, PasswordChangeForm, 'change_password.html')
@login_required
def set_password(request):
    return handle_password_change(request, SetPasswordForm, 'set_password.html')

def handle_password_change(request, form_class, template_name):
    """Handle password change and set password functionality."""
    if request.method == 'POST':
        form = form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('user_profile')
        messages.error(request, 'Please correct the error below.')
    else:
        form = form_class(request.user)
    return render(request, template_name, {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserSignupForm()
    return render(request, 'signup.html', {'form': form})

def dashboard(request):
    if request.method == "POST":
        return redirect("textResponse")
    return render(request, "dashboard.html")

def user_login(request):
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')
@login_required
def user_profile(request):
    return render(request, 'profile.html', {'user': request.user})
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})
