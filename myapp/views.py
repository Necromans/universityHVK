from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .chatbot import get_chatbot_response
from .models import ChatMessage, Article

# Create your views here.
def home(request):
    # Получаем все статьи из базы данных
    articles = Article.objects.all()
    
    # Если статей нет, создаем несколько демо-статей
    if not articles.exists():
        # Создаем демо-статьи
        demo_articles = [
            {
                'title': 'Искусственный интеллект в современном мире',
                'description': 'Как ИИ меняет нашу повседневную жизнь и какие перспективы открывает для человечества в ближайшем будущем.',
                'url': 'https://example.com/ai-modern-world',
                'image_url': 'https://via.placeholder.com/350x200?text=Искусственный+интеллект',
                'category': 'tech',
            },
            {
                'title': 'Квантовые компьютеры: революция в вычислениях',
                'description': 'Что такое квантовые компьютеры и как они могут изменить мир технологий и криптографии.',
                'url': 'https://example.com/quantum-computers',
                'image_url': 'https://via.placeholder.com/350x200?text=Квантовые+компьютеры',
                'category': 'tech',
            },
            {
                'title': 'Блокчейн: не только для криптовалют',
                'description': 'Применение технологии блокчейн в различных отраслях: от финансов до здравоохранения.',
                'url': 'https://example.com/blockchain-beyond-crypto',
                'image_url': 'https://via.placeholder.com/350x200?text=Блокчейн',
                'category': 'tech',
            },
            {
                'title': 'Исследование Марса: новые открытия',
                'description': 'Последние данные с марсоходов и планы по колонизации Красной планеты в ближайшие десятилетия.',
                'url': 'https://example.com/mars-exploration',
                'image_url': 'https://via.placeholder.com/350x200?text=Космос',
                'category': 'science',
            },
            {
                'title': 'Генетика: прорыв в лечении заболеваний',
                'description': 'Как CRISPR и другие генетические технологии помогают в борьбе с наследственными заболеваниями.',
                'url': 'https://example.com/genetics-breakthrough',
                'image_url': 'https://via.placeholder.com/350x200?text=Генетика',
                'category': 'science',
            },
            {
                'title': 'Изменение климата: факты и прогнозы',
                'description': 'Анализ последних исследований по изменению климата и возможные сценарии развития ситуации.',
                'url': 'https://example.com/climate-change',
                'image_url': 'https://via.placeholder.com/350x200?text=Климат',
                'category': 'science',
            },
            {
                'title': 'Здоровый сон: секреты качественного отдыха',
                'description': 'Научные исследования о важности сна и практические советы для улучшения его качества.',
                'url': 'https://example.com/healthy-sleep',
                'image_url': 'https://via.placeholder.com/350x200?text=Сон',
                'category': 'health',
            },
            {
                'title': 'Правильное питание: основы здорового рациона',
                'description': 'Как составить сбалансированный рацион и какие продукты необходимы для здоровья.',
                'url': 'https://example.com/healthy-nutrition',
                'image_url': 'https://via.placeholder.com/350x200?text=Питание',
                'category': 'health',
            },
            {
                'title': 'Онлайн-образование: будущее обучения',
                'description': 'Как онлайн-платформы меняют традиционное образование и какие навыки будут востребованы.',
                'url': 'https://example.com/online-education',
                'image_url': 'https://via.placeholder.com/350x200?text=Образование',
                'category': 'education',
            },
        ]
        
        # Создаем статьи в базе данных
        for article_data in demo_articles:
            Article.objects.create(**article_data)
        
        # Получаем созданные статьи
        articles = Article.objects.all()
    
    return render(request, 'myapp/home.html', {'articles': articles})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'myapp/profile.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')

@login_required
def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        bot_mode = request.POST.get('bot_mode', 'system')
        
        try:
            # Получаем ответ от чат-бота в зависимости от выбранного режима
            if bot_mode == 'gpt':
                # Используем только ChatGPT
                response = get_chatbot_response(message, use_gpt_only=True)
            else:
                # Используем гибридный режим (сначала проверяем простые ответы)
                response = get_chatbot_response(message, use_gpt_only=False)
            
            # Сохраняем сообщение и ответ в базу данных
            ChatMessage.objects.create(
                user=request.user,
                message=message,
                response=response
            )
            
            return JsonResponse({
                'response': response,
                'status': 'success'
            })
        except Exception as e:
            # В случае ошибки возвращаем сообщение об ошибке
            return JsonResponse({
                'response': "Извините, произошла ошибка при обработке вашего запроса. Попробуйте задать другой вопрос.",
                'status': 'error'
            })
    
    # Получаем историю сообщений пользователя
    chat_history = ChatMessage.objects.filter(user=request.user)
    return render(request, 'myapp/chat.html', {'chat_history': chat_history})