import os
import django


# Налаштування Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_project.settings")
django.setup()
import mongoengine
from quotes.models import Author, Quote
from django.contrib.auth.models import User
# Створення користувача з ідентифікатором 1
User.objects.create_user(username='admin', password='admin_password', email='admin@example.com', id=1)

# Підключення до MongoDB
mongoengine.connect(
    db="cluster0",
    username="kiril4a",
    password="matador1983",
    host="mongodb+srv://kiril4a:matador1983@cluster0.t1m9ifp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Визначення моделі MongoDB для авторів
class MongoAuthor(mongoengine.Document):
    meta = {'collection': 'author'}  # Назва колекції
    fullname = mongoengine.StringField()
    born_date = mongoengine.StringField()
    born_location = mongoengine.StringField()
    description = mongoengine.StringField()

# Визначення моделі MongoDB для цитат
class MongoQuote(mongoengine.Document):
    meta = {'collection': 'quote'}  # Назва колекції
    tags = mongoengine.ListField(mongoengine.StringField())
    author = mongoengine.ReferenceField(MongoAuthor)
    quote = mongoengine.StringField()

# Міграція авторів з MongoDB до Django
def migrate_authors():
    print("=== Authors Migration ===")
    for mongo_author in MongoAuthor.objects:
        print(f"MongoDB Author: {mongo_author.fullname}")
        author, created = Author.objects.get_or_create(
            fullname=mongo_author.fullname,
            defaults={
                'born_date': mongo_author.born_date,
                'born_location': mongo_author.born_location,
                'description': mongo_author.description
            }
        )
        if created:
            print(f"Created Django Author: {author.fullname}")
        else:
            print(f"Found Existing Django Author: {author.fullname}")

# Міграція цитат з MongoDB до Django
def migrate_quotes():
    print("=== Quotes Migration ===")
    for mongo_quote in MongoQuote.objects:
        print(f"MongoDB Quote: {mongo_quote.quote}")
        try:
            author = Author.objects.get(fullname=mongo_quote.author.fullname)
            # Зберігаємо теги як рядок з комами
            tags_str = ", ".join(mongo_quote.tags)
            
            # Знайдіть відповідного користувача Django, якщо він є
            user = User.objects.first()
            if user:
                quote, created = Quote.objects.get_or_create(
                    text=mongo_quote.quote,
                    tags=tags_str,
                    author=author,
                    user=user  # Призначення користувача для цитати
                )
                if created:
                    print(f"Created Django Quote: {quote.text}")
                else:
                    print(f"Found Existing Django Quote: {quote.text}")
            else:
                print("No Django users found. Cannot migrate quotes.")
        except Author.DoesNotExist:
            print(f"Author '{mongo_quote.author.fullname}' does not exist in Django. Skipping quote.")

# Виклик функцій міграції
if __name__ == "__main__":
    migrate_authors()
    migrate_quotes()
