import redis
from celery import shared_task
from .models import Word, Language, User

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@shared_task
def save_word_task(text, definition, language_code, user_id, sentences=None, translations=None):
    try:
        language = Language.objects.get(code=language_code)
        user = User.objects.get(id=user_id)
        Word.objects.create(
            text=text,
            definition=definition,
            language=language,
            user=user,
            sentences=sentences or [],
            translations=translations or {}
        )
    except Exception as e:
        # Log or handle error here
        print(f"Failed to save word: {e}")
