# Kirish

## 1. Tortoise ORM nima?

Tortoise ORM — Python dasturlash tili uchun engil va asinxron obyektlar-yo‘naltirilgan ma'lumotlar bazasi boshqaruv
tizimi. U asinxron tarzda asyncio bilan ishlaydi va SQL yozmasdan turib, obyektlar orqali ma'lumotlar bazasi bilan
muloqot qilishga imkon beradi. Tortoise ORM PostgreSQL, MySQL, va SQLite kabi ma'lumotlar bazalarini
qo‘llab-quvvatlaydi.

Ushbu tutorialda biz aynan **PostgreSQL** bilan Tortoise ORM'ni qanday ishlatishni o'rganamiz.

## 2. Tortoise ORM afzalliklari

- **Asinxronlik:** Tortoise asyncio asosida ishlaydi, bu katta so'rovlar bilan samarali ishlash imkonini beradi.
- **PostgreSQL'ni qo'llab-quvvatlash:** PostgreSQL ma'lumotlar bazasi bilan kuchli integratsiya.
- **Oddiy va minimal tuzilma:** Python obyektlari orqali ma'lumotlarni boshqarish.

# Tortoise ORM o'rnatilishi (PostgreSQL uchun)

## 1. O‘rnatish va sozlash

PostgreSQL bilan ishlash uchun bizga Tortoise ORM va `asyncpg` kutubxonasi kerak bo‘ladi.

### 1-qadam: Virtual environment yaratish

Birinchi qadam — har doim virtual environment yaratish tavsiya etiladi. Bu loyihangizdagi kutubxonalarni boshqalaridan
ajratib turadi.

Terminalda yoki buyruq satrida quyidagilarni yozing:

```bash
python3 -m venv venv
```

Endi virtual environmentni faollashtiramiz:

- **Linux yoki macOS uchun:**

```bash
source venv/bin/activate
```

- **Windows uchun:**

```bash
venv\Scripts\activate
```

### 2-qadam: Tortoise ORM va asyncpg o‘rnatish

PostgreSQL bilan ishlash uchun Tortoise ORM va `asyncpg` kutubxonasini o‘rnatamiz:

```bash
pip install tortoise-orm asyncpg
```

Bu buyruq orqali ikkala kutubxona ham o‘rnatiladi: Tortoise ORM va PostgreSQL bilan ishlash uchun kerakli `asyncpg`.

### 3-qadam: PostgreSQL serverini sozlash

Sizda PostgreSQL serveringiz o'rnatilgan bo'lishi va baza yaratib qo'yilgan bo'lishi kerak.
Baza yaratish uchun quyidagi buyruqlarni ishlatamiz:

```bash
sudo -u postgres psql
CREATE DATABASE tortoise_db;
CREATE USER tortoise_user WITH PASSWORD 'password';
ALTER ROLE tortoise_user SET client_encoding TO 'utf8';
ALTER ROLE tortoise_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE tortoise_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tortoise_db TO tortoise_user;
```

Bu buyruqlar orqali biz `tortoise_db` nomli baza yaratamiz va unga kirish uchun `tortoise_user` foydalanuvchisini
yaratamiz.

### 4-qadam: Loyiha tarkibi va asosiy fayllarni yaratish

Loyihamizning tarkibini tashkil qilamiz:

```css
│
├── main.py
├── models.py
└── settings.py

```

Bu modelda `id`, `username`, `email`, va `is_active` kabi maydonlar mavjud.

### 5-qadam: Tortoise ORM ulanishini sozlash

Endi `settings.py` faylida PostgreSQL bilan ulanishni sozlaymiz:

```python
DATABASE = "tortoise_db"
HOST = "localhost"
PASSWORD = "password"
PORT = "5432"
DBUSER = "tortoise_user"

ORM_CREDENTIALS = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": DATABASE,
                "host": HOST,
                "password": PASSWORD,
                "port": PORT,
                "user": DBUSER,
            },
        }
    },
    "apps": {
        "models": {
            "models": ["domain.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Asia/Tashkent"
}

```

Bu yerda biz ulanish uchun `ORM_CREDENTIALS` konfiguratsiyasidan foydalanamiz, unda PostgreSQL ma'lumotlar bazasi
ulanish
parametrlari ko'rsatilgan.

`models.py` fayli:

Bu faylda model yaratamiz. Masalan, oddiy `User` modelini yaratamiz:

```python
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100)
    bio = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "users"  # table_name

```

# Ma'lumotlar bazasini migrate qilish va ulanish

## Aerich yordamida ma'lumotlar bazasini migratsiya qilish

Tortoise ORM bilan ishlashda **Aerich** — migratsiyalarni boshqarish uchun qulay vosita hisoblanadi. Bu vosita Tortoise
ORM uchun maxsus ishlab chiqilgan va sizning modellar o'zgarganda avtomatik ravishda migratsiyalar yaratib, ularni
ma'lumotlar bazasiga qo‘llash imkonini beradi.

### Aerich o'rnatish

Aerich'ni o'rnatish uchun quyidagi buyruqni terminalda bajaring:

```bash
pip install aerich
```

### Aerich'ni dastlabki sozlash

Aerich bilan ishlashni boshlashdan oldin, dastlabki konfiguratsiyani o‘rnatish kerak. Buning uchun quyidagi buyruqni
ishlatamiz:

```bash
aerich init -t settings.ORM_CREDENTIALS
```

Agar quyidagi natijani ko'rsangiz muammo yo'q:

```
Success create migrate location ./migrations
Success write config to pyproject.toml
```

Agar bu natija chiqsa:

```
Usage: aerich init [OPTIONS]
Try 'aerich init -h' for help.

Error: No such option: -c
```

siz `settings.ORM_CREDENTIALS` ni noto'g'ri ko'rsatyapsiz. Balki `ORM_CREDENTIALS` sizning loyihangizda boshqa manzilda
joylashgandir

### Aerich uchun config fayli `pyproject.toml`

Yuqoridagi buyruq pyproject.toml faylini yaratadi va unda Tortoise ORM konfiguratsiyasini o'rnatish uchun kerakli yo'
lni (
settings.ORM_CREDENTIALS) ko'rsatadi.

```
[tool.aerich]
tortoise_orm = "settings.ORM_CREDENTIALS"
location = "./migrations" # migration fayllar uchun, 
src_folder = "./."
```

Bu konfiguratsiya Tortoise ORM va Aerich migratsiya joylashuvlarini boshqarish uchun ishlatiladi.

- `tortoise_orm` - database konfiguratsiyasi
- `location` - migration fayllar uchun folder

### Dastlabki migratsiyani yaratish

Endi dastlabki migratsiyalarni yaratish uchun, quyidagi buyruqni ishlating:

```bash
aerich init-db -c orm_config.toml
```

Bu buyruq mavjud modellarga asoslangan holda dastlabki migratsiyalarni yaratadi va migrations folderiga saqlaydi.

**Eslatma:** *faqat birinchi marta migrationlarni yaratish
uchun* `init-db` *buyrug'i ishlatiladi. Bu buyruq natijasida migrationlar yaratilib ma'lumotlar bazasida jadvallar
yaratiladi. Agar bu buyruq ishlatilganidan keyin modellarda biror o'zgarish amalga oshirilmasa boshqa buyruqlarni ishga
tushurish kerak emas.*


  