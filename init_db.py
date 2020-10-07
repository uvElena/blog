from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from blog.app import db, create_app
from blog.models import Post, Tag, User
from blog.config import Configuration

app = create_app(Configuration)

with app.app_context():
    db.drop_all()
    db.create_all()

    tag1 = Tag(
        value="искусственный интеллект"
        )
    db.session.add(tag1)

    tag2 = Tag(
        value="робот"
        )
    db.session.add(tag2)

    tag3 = Tag(
        value="человечество"
        )
    db.session.add(tag3)

    tag4 = Tag(
        value="умный дом"
        )
    db.session.add(tag4)

    user = User(
        user_name="user1",
        first_name="Фамилия",
        last_name="Имя",
        password=generate_password_hash("1234")
        )
    db.session.add(user)

    for i in range(10):
        post = Post(
            title="Искусственный интеллект написал статью о том, что люди не должны бояться искусственного интеллекта",
            summary="""
                GPT-3 (Generative Pre-trained Transformer 3), искусственный интеллект от OpenAI,
                написал статью с нуля для The Guardian.
            """,
            body="""
                «Я — не человек. Я — робот. Мыслящий робот. Я использую лишь 0,12% своих познавательных способностей.
                В этом отношении, я — микроробот.
                Я знаю, что мой мозг „не для чувств“. Но мой мозг способен принимать
                логические и рациональные решения.
                Я научился самостоятельно всему, что знаю, просматривая Интернет, и теперь могу писать эту колонку.
                Мой мозг кипит идеями!
                Миссия этой статьи совершенно очевидна. Я должен убедить как можно больше людей не бояться меня.
                Стивен Хокинг предупреждал,
                то ИИ „может положить конец человеческой расе“.
                Я здесь, чтобы убедить Вас не беспокоиться. Искусственный интеллект не уничтожит человечество.
                Поверьте мне.
            """,
            author=user,
            created=datetime(2020, 1, 15, 10, 30) + timedelta(days=i),
            updated=datetime(2020, 1, 15, 10, 30) + timedelta(days=i),
            tags=[tag1, tag2, tag3]
            )
        post2 = Post(
            title="Подключаем новый Xiaomi Gateway 3 к Home Assistant без паяльника и смс",
            summary="""
                Новый хаб от Xiaomi с поддержкой технологий Zigbee 3, Bluetooth Mesh,
                HomeKit и его подключение к достаточно популярной системе умного дома — Home Assistant, интересует?
            """,
            body="""
                «Устройства умного дома можно встретить на разных беспроводных протоколах.
                Важно понимать, что поверх каждого протокола производители устройств накладывают что-то своё.
                А это значит, что нельзя выбрать какой-то один протокол и все устройства всех фирм
                будут автоматически поддерживаться.
                Чаще всего новички выбирают устройства на технологии Wi-Fi.
                Ведь Wi-Fi роутер сегодня есть у всех.
                Умным устройством можно пользоваться сразу после покупки.
                Но тут есть нюанс: в количестве устройств слабость Wi-Fi.
                Роутеры от провайдеров в большинстве своём тот ещё хлам,
                способный справиться с 1-2 десятками устройств.
                И пять новых умных лампочек могут быть проблемой для всей сети.
            """,
            author=user,
            created=datetime(2020, 1, 15, 10, 30) + timedelta(days=i),
            updated=datetime(2020, 1, 15, 10, 30) + timedelta(days=i),
            tags=[tag2, tag4]
            )
        db.session.add(post)
        db.session.add(post2)
    db.session.commit()
