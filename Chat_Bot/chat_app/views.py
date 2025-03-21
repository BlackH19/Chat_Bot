from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai

# Create your views here.
# add here to your generated API key
genai.configure(api_key="AIzaSyBQDk4DvtyKXSv41X5JAeKG8ODKhXPoeow")

@login_required
def ask_question(request):
    print("fonction utilisé")
    if request.method == "POST":
        text = request.POST.get("messageText")
        try:
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(text)
            user = request.user
            ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
            response_data = {
                "text": response.text,
                "date": response.date
            }
            return JsonResponse({"data": response_data})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
        print(response)
    else:
        return HttpResponseRedirect(reverse("chat")) # Redirect to chat page for GET requests

@login_required
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chat_bot.html", {"chats": chats})