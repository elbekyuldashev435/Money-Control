
def get_home(request):
Bu funksiya home.html ga hisoblardagi pullar miqdori va kirim chiqmlarning umumiy miqdor summasini ko'rsatib berish uchun ishlaydi. Va valyuta hamyoni bo'lsa uning miqdor summasini so'mga o'g'irib ko'rsatadi.

def get_wallet(request):
Bu funksiya wallet.html ga Naqt pul, Karta va Valyuta hamyonlaridagi umumiy summa miqdorini ko'rsatish bilan birga uni tahrirlash imkoniniham beradi.

def get_settings(request):
Bu funksiya settings.html ga user ma'lumotlari va uning barcha hamyonlar ro'yxatini beradi.

def cash_create(request): | def card_create(request): | def currency_create(request):
Bu funksiyalar asosan hamyonlar yaratish uchun ishlaydi.

def cash_edit(request, pk): | def card_edit(request, pk): | def currency_edit(request, pk):
Bu funksiyalar o'sha yaratilgan hamyonlarni tahrirlash uchun ishlaydi.

def get_income_outcome_list(request):
Bu funksiya kirim va chiqimlarni vaqti bilan filtirlab barcha kirim va chiqimlarni kategoriya va to'lov turlari bilan ko'rsatish uchun ishlaydi.

def generate_qr_code(data): | def get_income_detail(request, pk):
Bu ikki funksiya birgarikda ishlaydi. Asosan kirim bo'lgandagi har bir ma'lumot ustiga bosilganda undan [chek] hosil qilish uchun ishlab beradi.

def create_income(request): | def create_outcome(request):
Bu funksiyalar kirim va chiqim kiritish uchun ishlaydi. 
