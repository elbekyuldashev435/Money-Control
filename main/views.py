from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Cash, Currency, Income, Outcome
from users.models import User
from .forms import CashForm, CardForm, CardEditForm, CurrencyForm, IncomeForm, OutcomeForm
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import qrcode
import io
import base64
from django.db.models import Q


def get_home(request):
    if not request.user.is_authenticated:
        return redirect('user-login')
    else:
        try:
            cash = Cash.objects.get(user_id=request.user.pk)
        except:
            cash = None
        try:
            card = Card.objects.get(user_id=request.user.pk)
        except:
            card = None
        try:
            currency = Currency.objects.get(user_id=request.user.pk)
        except:
            currency = None
        try:
            incomes = Income.objects.filter(receiver_id=request.user.pk)
        except:
            incomes = None
        try:
            outcomes = Outcome.objects.filter(sender_id=request.user.pk)
        except:
            outcomes = None

        context = {
            'all_money': 0,
            'all_incomes': 0,
            'all_outcomes': 0,

            'income_salary_cash': 0,
            'income_salary_card': 0,
            'income_salary_currency': 0,

            'income_gift_cash': 0,
            'income_gift_card': 0,
            'income_gift_currency': 0,

            'outcome_kamunal_cash': 0,
            'outcome_kamunal_card': 0,
            'outcome_kamunal_currency': 0,

            'outcome_shaxsiy_cash': 0,
            'outcome_shaxsiy_card': 0,
            'outcome_shaxsiy_currency': 0,

            'outcome_transport_cash': 0,
            'outcome_transport_card': 0,
            'outcome_transport_currency': 0,

            'outcome_uyali_aloqa_cash': 0,
            'outcome_uyali_aloqa_card': 0,
            'outcome_uyali_aloqa_currency': 0,

            'outcome_internet_cash': 0,
            'outcome_internet_card': 0,
            'outcome_internet_currency': 0,

            "outcome_ruzgor_cash": 0,
            "outcome_ruzgor_card": 0,
            "outcome_ruzgor_currency": 0,
        }

        if cash is not None:
            context['all_money'] += cash.amount
        if card is not None:
            context['all_money'] += card.amount
        if currency is not None:
            context['all_money'] += currency.amount * (12.5 * 1000)

        if incomes is not None:
            for income in incomes:

                context['all_incomes'] += income.amount * (12.5 * 100) if income.payment_type == 'currency' else income.amount
                if income.income_type == 'salary':  # salary
                    if income.payment_type == 'cash':
                        context['income_salary_cash'] += income.amount
                    if income.payment_type == 'card':
                        context['income_salary_card'] += income.amount
                    if income.payment_type == 'currency':
                        context['income_salary_currency'] += income.amount

                if income.income_type == 'gift':    # gift
                    if income.payment_type == 'cash':
                        context['income_gift_cash'] += income.amount
                    if income.payment_type == 'card':
                        context['income_gift_card'] += income.amount
                    if income.payment_type == 'currency':
                        context['income_gift_currency'] += income.amount
        if outcomes is not None:
            for outcome in outcomes:
                context['all_outcomes'] += outcome.amount * (12.5 * 100) if outcome.payment_type == 'currency' else outcome.amount

                if outcome.outcome_type == 'komunal':    # kamunal
                    if outcome.payment_type == 'cash':
                        context['outcome_kamunal_cash'] += outcome.amount
                    if outcome.payment_type == 'card':
                        context['outcome_kamunal_card'] += outcome.amount
                    if outcome.payment_type == 'currency':
                        context['outcome_kamunal_currency'] += outcome.amount

                if outcome.outcome_type == 'shaxsiy':    # shaxsiy
                    if outcome.payment_type == 'cash':
                        context['outcome_shaxsiy_cash'] += outcome.amount
                    if outcome.payment_type == 'card':
                        context['outcome_shaxsiy_card'] += outcome.amount
                    if outcome.payment_type == 'currency':
                        context['outcome_shaxsiy_currency'] += outcome.amount

                if outcome.outcome_type == 'transport':    # transport
                    if outcome.payment_type == 'cash':
                        context['outcome_transport_cash'] += outcome.amount
                    if outcome.payment_type == 'card':
                        context['outcome_transport_card'] += outcome.amount
                    if outcome.payment_type == 'currency':
                        context['outcome_transport_currency'] += outcome.amount

                if outcome.outcome_type == 'uyali aloqa':    # uyali aloqa
                    if outcome.payment_type == 'cash':
                        context['outcome_uyali_aloqa_cash'] += outcome.amount
                    if outcome.payment_type == 'card':
                        context['outcome_uyali_aloqa_card'] += outcome.amount
                    if outcome.payment_type == 'currency':
                        context['outcome_uyali_aloqa_currency'] += outcome.amount

                if outcome.outcome_type == 'internet':    # internet
                    if outcome.payment_type == 'cash':
                        context['outcome_internet_cash'] += outcome.amount
                    if outcome.payment_type == 'card':
                        context['outcome_internet_card'] += outcome.amount
                    if outcome.payment_type == 'currency':
                        context['outcome_internet_currency'] += outcome.amount

                if outcome.outcome_type == "ro'zg'or":    # ro'zg'or
                    if outcome.payment_type == 'cash':
                        context["outcome_ruzgor_cash"] += outcome.amount
                    if outcome.payment_type == 'card':
                        context["outcome_ruzgor_card"] += outcome.amount
                    if outcome.payment_type == 'currency':
                        context["outcome_ruzgor_currency"] += outcome.amount

        return render(request, 'main/home.html', context=context)


def get_wallet(request):
    if request.method == 'GET':
        context = {
            'cash': 0,
            'cash_pk': 0,
            'card': 0,
            'card_pk': 0,
            'currency': 0,
            'currency_pk': 0
        }

        try:
            cash = Cash.objects.get(user_id=request.user.pk)
        except:
            cash = None
        try:
            card = Card.objects.get(user_id=request.user.pk)
        except:
            card = None
        try:
            currency = Currency.objects.get(user_id=request.user.pk)
        except:
            currency = None

        if cash is not None:
            context['cash'] = cash.amount
            context['cash_pk'] = cash.pk
        if card is not None:
            context['card'] = card.amount
            context['card_pk'] = card.pk
        if currency is not None:
            context['currency'] = currency.amount
            context['currency_pk'] = currency.pk

        return render(request, 'main/wallet.html', context=context)
    else:
        raise ValueError("Bunday so'rov mavjud emas!")


def get_settings(request):
    if request.method == 'GET':

        user = User.objects.get(username=request.user.username)
        try:
            cash = Cash.objects.get(user_id=request.user.pk)
        except:
            cash = None
        try:
            card = Card.objects.get(user_id=request.user.pk)
        except:
            card = None
        try:
            currency = Currency.objects.get(user_id=request.user.pk)
        except:
            currency = None

        context = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,

            'cash': "Naqt pul bo'yicha hamyon mavjud emas",
            'card': "Karta bo'yicha hamyon mavjud emas",
            'currency': "Valyuta bo'yicha hamyon mavjud emas"
        }
        if cash is not None:
            context['cash'] = cash
        if card is not None:
            context['card'] = card
        if currency is not None:
            print(currency)
            context['currency'] = currency

        return render(request, 'main/settings.html', context=context)


def cash_create(request):
    cashes = Cash.objects.filter(user_id=request.user.pk)
    if len(cashes) < 2:
        if request.method == 'POST':
            cash_form = CashForm(request.POST)
            if cash_form.is_valid():
                form = cash_form.save(commit=False)
                form.user_id = request.user
                form.save()
                messages.success(request, 'Naqt pul hamyoni muvafaqqiyatli yaratildi.')
                return redirect('get-settings')
            else:
                messages.error(request, 'Naqt pul hamyon kiritilishi bilan Xatolik!!!')
        else:
            cash_form = CashForm()

        return render(request, 'main/create_cash.html', {'cash_form': cash_form})
    else:
        messages.error(request, "1dan ortiq hisob qo'sha olmaysiz!!!")
        return redirect('get-settings')


def card_create(request):
    cards = Card.objects.filter(user_id=request.user.pk)
    if len(cards) < 2:
        if request.method == 'POST':
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                form = card_form.save(commit=False)
                form.user_id = request.user
                form.save()
                messages.success(request, "Karta muvafaqqiyatli qo'shildi.")
                return redirect('get-settings')
            else:
                messages.error(request, "Karta qo'shilishi bilan Xatolik!!!")
        else:
            card_form = CardForm()

        return render(request, 'main/create_card.html', {'card_form': card_form})
    else:
        messages.error(request, "1dan ortiq hisob qo'sha olmaysiz!!!")
        return redirect('get-settings')


def currency_create(request):
    currencies = Currency.objects.filter(user_id=request.user.pk)
    if len(currencies) < 2:
        if request.method == 'POST':
            currency_form = CurrencyForm(request.POST)
            if currency_form.is_valid():
                form = currency_form.save(commit=False)
                form.user_id = request.user
                form.save()
                messages.success(request, 'Valyuta hamyoni muvafaqqiyatli yaratildi.')
                return redirect('get-settings')
            else:
                messages.error(request, 'Valyuta hamyoni yaratilishi bilan Xatolik!!!')
        else:
            currency_form = CurrencyForm()

        return render(request, 'main/create_currency.html', {'currency_form': currency_form})
    else:
        messages.error(request, "1dan ortiq hisob qo'sha olmaysiz!!!")
        return redirect('get-settings')


def cash_edit(request, pk):
    cash = Cash.objects.get(pk=pk)
    if request.method == 'POST':
        cash_from = CashForm(request.POST, instance=cash)
        if cash_from.is_valid():
            cash_from.save()
            messages.success(request, "Naqt pul hamyoni muvafaqqiyatli o'zgartirildi")
            return redirect('get-settings')
        else:
            messages.error(request, "Naqt pul hamyoni o'zgartirilishi bilan Xatolik!!!")
    else:
        cash_form = CashForm(instance=cash)
    return render(request, 'main/edit_cash.html', {'cash_form': cash_form, 'cash': cash})


def card_edit(request, pk):
    card = Card.objects.get(pk=pk)
    if request.method == 'POST':
        card_form = CardEditForm(request.POST, instance=card)
        if card_form.is_valid():
            card_form.save()
            messages.success(request, "Karta malumotlari muvafaqqiyatli o'zgartirildi")
            return redirect('get-settings')
        else:
            messages.error(request, "Karta malumotlari o'zgartirilishi bilan Xatolik!!!")
    else:
        card_form = CardEditForm(instance=card)
    return render(request, 'main/edit_card.html', {'card_form': card_form, 'card': card})


def currency_edit(request, pk):
    currency = get_object_or_404(Currency, pk=pk, user_id=request.user.pk)
    if request.method == 'POST':
        currency_form = CurrencyForm(request.POST, instance=currency)
        if currency_form.is_valid():
            currency_form.save()
            messages.success(request, "Valyuta malumotlari muvafaqqiyatli o'zgartirildi")
            return redirect('get-settings')
        else:
            messages.error(request, "Valyuta malumotlari o'zgartirilishi bilan Xatolik!!!")
    else:
        currency_form = CurrencyForm(instance=currency)
    return render(request, 'main/edit_currency.html', {'currency_form': currency_form, 'currency': currency})


def get_income_outcome_list(request):
    context = {
        'all_salary': 0.0,
        'salary_cash': [],
        'salary_card': [],
        'salary_currency': [],

        'all_gift': 0.0,
        'gift_cash': [],
        'gift_card': [],
        'gift_currency': [],

        'all_kamunal': 0.0,
        'kamunal_cash': [],
        'kamunal_card': [],
        'kamunal_currency': [],

        'all_shaxsiy': 0.0,
        'shaxsiy_cash': [],
        'shaxsiy_card': [],
        'shaxsiy_currency': [],

        'all_transport': 0.0,
        'transport_cash': [],
        'transport_card': [],
        'transport_currency': [],

        'all_uyali_aloqa': 0.0,
        'uyali_aloqa_cash': [],
        'uyali_aloqa_card': [],
        'uyali_aloqa_currency': [],

        'all_internet': 0.0,
        'internet_cash': [],
        'internet_card': [],
        'internet_currency': [],

        'all_ruzgor': 0.0,
        "ruzgor_cash": [],
        "ruzgor_card": [],
        "ruzgor_currency": [],
    }

    try:
        incomes = Income.objects.filter(receiver_id=request.user.pk).order_by('-created_at')
    except Income.DoesNotExist:
        incomes = None
    try:
        outcomes = Outcome.objects.filter(sender_id=request.user.pk).order_by('-created_at')
    except Outcome.DoesNotExist:
        outcomes = None

    start_date_income = request.GET.get('start_date_income')
    end_date_income = request.GET.get('end_date_income')
    start_date_outcome = request.GET.get('start_date_outcome')
    end_date_outcome = request.GET.get('end_date_outcome')
    if (start_date_income and end_date_income) or (start_date_outcome and end_date_outcome):
        try:
            if start_date_income and end_date_income:
                start_date_income = datetime.strptime(start_date_income, '%Y-%m-%d')
                end_date_income = datetime.strptime(end_date_income, '%Y-%m-%d')
                incomes = incomes.filter(created_at__range=[start_date_income, end_date_income])
            if start_date_outcome and end_date_outcome:
                start_date_outcome = datetime.strptime(start_date_outcome, '%Y-%m-%d')
                end_date_outcome = datetime.strptime(end_date_outcome, '%Y-%m-%d')
                outcomes = outcomes.filter(created_at__range=[start_date_outcome, end_date_outcome])
        except ValueError:
            pass

    income_page = request.GET.get('income_page', 1)
    income_paginator = Paginator(incomes, 15)
    try:
        incomes = income_paginator.page(income_page)
    except PageNotAnInteger:
        incomes = income_paginator.page(1)
    except EmptyPage:
        incomes = income_paginator.page(income_paginator.num_pages)

    outcome_page = request.GET.get('outcome_page', 1)
    outcome_paginator = Paginator(outcomes, 8)
    try:
        outcomes = outcome_paginator.page(outcome_page)
    except PageNotAnInteger:
        outcomes = outcome_paginator.page(1)
    except EmptyPage:
        outcomes = outcome_paginator.page(outcome_paginator.num_pages)

    if incomes is not None:
        for income in incomes:
            if income.income_type == 'salary':
                context['all_salary'] += income.amount * (12.5 * 1000) if income.payment_type == 'currency' else income.amount
                income.income_type = 'Maosh'
                if income.payment_type == 'cash':
                    income.payment_type = 'Naqt pul'
                    context['salary_cash'].append(income)
                elif income.payment_type == 'card':
                    income.payment_type = 'Karta'
                    context['salary_card'].append(income)
                elif income.payment_type == 'currency':
                    income.payment_type = 'Valyuta'
                    context['salary_currency'].append(income)

            if income.income_type == 'gift':    # Sovg'a
                context['all_gift'] += income.amount * (12.5 * 1000) if income.payment_type == 'currency' else income.amount
                income.income_type = "Sovg'a"
                if income.payment_type == 'cash':
                    income.payment_type = 'Naqt pul'
                    context['gift_cash'].append(income)
                elif income.payment_type == 'card':
                    income.payment_type = 'Karta'
                    context['gift_card'].append(income)
                elif income.payment_type == 'currency':
                    income.payment_type = 'Valyuta'
                    context['gift_currency'].append(income)

    if outcomes is not None:
        for outcome in outcomes:
            if outcome.outcome_type == 'komunal':   # Kamunal
                context['all_kamunal'] += outcome.amount * (12.5 * 1000) if outcome.payment_type == 'currency' else outcome.amount
                outcome.outcome_type = 'Kamunal'
                if outcome.payment_type == 'cash':
                    context['kamunal_cash'].append(outcome)
                elif outcome.payment_type == 'card':
                    context['kamunal_card'].append(outcome)
                elif outcome.payment_type == 'currency':
                    context['kamunal_currency'].append(outcome)

            if outcome.outcome_type == 'shaxsiy':   # Shaxsiy
                context['all_shaxsiy'] += outcome.amount * (12.5 * 1000) if outcome.payment_type == 'currency' else outcome.amount
                outcome.outcome_type = 'Shaxsiy'
                if outcome.payment_type == 'cash':
                    context['shaxsiy_cash'].append(outcome)
                elif outcome.payment_type == 'card':
                    context['shaxsiy_card'].append(outcome)
                elif outcome.payment_type == 'currency':
                    context['shaxsiy_currency'].append(outcome)

            if outcome.outcome_type == 'transport':   # Transport
                context['all_transport'] += outcome.amount * (12.5 * 1000) if outcome.payment_type == 'currency' else outcome.amount
                outcome.outcome_type = 'Transport'
                if outcome.payment_type == 'cash':
                    context['transport_cash'].append(outcome)
                elif outcome.payment_type == 'card':
                    context['transport_card'].append(outcome)
                elif outcome.payment_type == 'currency':
                    context['transport_currency'].append(outcome)

            if outcome.outcome_type == 'uyali aloqa':   # Uyali Aloqa
                context['all_uyali_aloqa'] += outcome.amount * (12.5 * 1000) if outcome.payment_type == 'currency' else outcome.amount
                outcome.outcome_type = 'Uyali Aloqa'
                if outcome.payment_type == 'cash':
                    context['uyali_aloqa_cash'].append(outcome)
                elif outcome.payment_type == 'card':
                    context['uyali_aloqa_card'].append(outcome)
                elif outcome.payment_type == 'currency':
                    context['uyali_aloqa_currency'].append(outcome)

            if outcome.outcome_type == 'internet':   # Internet
                context['all_internet'] += outcome.amount * (12.5 * 1000) if outcome.payment_type == 'currency' else outcome.amount
                outcome.outcome_type = 'Internet'
                if outcome.payment_type == 'cash':
                    context['internet_cash'].append(outcome)
                elif outcome.payment_type == 'card':
                    context['internet_card'].append(outcome)
                elif outcome.payment_type == 'currency':
                    context['internet_currency'].append(outcome)

            if outcome.outcome_type == "ro'zg'or":   # Ro'zg'or
                context['all_ruzgor'] += outcome.amount * (12.5 * 1000) if outcome.payment_type == 'currency' else outcome.amount
                outcome.outcome_type = "Ro'zg'or"
                if outcome.payment_type == 'cash':
                    context['ruzgor_cash'].append(outcome)
                elif outcome.payment_type == 'card':
                    context['ruzgor_card'].append(outcome)
                elif outcome.payment_type == 'currency':
                    context['ruzgor_currency'].append(outcome)

    context['incomes'] = incomes
    context['outcomes'] = outcomes

    return render(request, 'main/income_outcome.html', context=context)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


def get_income_detail(request, pk):
    if request.method == 'GET':
        try:
            income = Income.objects.get(receiver_id=request.user.pk, pk=pk)
        except:
            income = None

        if income is not None:
            qr_code_data = f"Kirim turi: {income.income_type}, To'lov turi: {income.payment_type}, Summa: {income.amount}, Vaqti: {income.created_at}"
            qr_code_image = generate_qr_code(qr_code_data)
            context = {
                'income': income,
                'qr_code_image': qr_code_image
            }

            return render(request, 'main/income_detail.html', context=context)


def create_income(request):
    if request.method == 'POST':
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            form = income_form.save(commit=False)
            form.receiver_id = request.user
            form.save()
            messages.success(request, 'Kirim malumotlari muvafaqqiyatli yaratildi.')
            return redirect('income-outcome')
        else:
            messages.error(request, 'Kirim malumotlari kiritilishi bilan Xatolik!!!')
    else:
        income_form = IncomeForm()
    return render(request, 'main/create_income.html', {'form': income_form})


def create_outcome(request):
    if request.method == 'POST':
        outcome_form = OutcomeForm(request.POST)
        if outcome_form.is_valid():
            form = outcome_form.save(commit=False)
            form.sender_id = request.user
            form.save()
            messages.success(request, 'Chiqim malumotlari muvafaqqiyatli yaratildi.')
            return redirect('income-outcome')
        else:
            messages.error(request, 'Chiqim malumotlari kiritilishi bilan Xatolik!!!')
    else:
        outcome_form = OutcomeForm()
    return render(request, 'main/create_outcome.html', {'form': outcome_form})