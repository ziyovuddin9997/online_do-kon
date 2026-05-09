from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from app_main.models import Product, User, Cart, Transaction


def products(request):
    products = Product.objects.all()

    return render(request, "products.html", { "products": products })


def signin(request):
    if request.user.is_authenticated:
        return redirect("products")

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        user = User.objects.filter(phone_number=phone_number).first()

        if user:
            password_is_correct = user.check_password(raw_password=password)

            if password_is_correct:
                login(request=request, user=user)
                return redirect("products")

        messages.error(request, "Tel. raqam yoki Parol xato!")
        return redirect("signin")

    return render(request, "login.html")


def signout(request):
    logout(request=request)
    return redirect("products")


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not first_name or not last_name or not phone_number or not password1 or not password2:
            messages.error(request, "Barcha sohalar to'ldirilishi shart")
            return redirect("signup")

        if password1 == password2:
            if len(password2) >= 8:
                user_exists = User.objects.filter(phone_number=phone_number).exists()

                if not user_exists:
                    new_user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                    )
                    new_user.set_password(raw_password=password2)
                    new_user.save()
                    return redirect("signin")

                else:
                    messages.error(request, "Bunday tel. raqamga ega foydalanuvchi tizimda mavjud")
            else:
                messages.error(request, "Parol 8 ta yoki undan ko'p belgidan iborat bo'lishi shart")
        else:
            messages.error(request, "Parollar bir-biriga mos emas")

        return redirect("signup")

        # Ro'yxatdan o'tkazish

    return render(request, "registration.html")


def product_detail(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        quantity = request.POST.get("quantity")  # 2 yoki 3

        try:
            cart_object = Cart.objects.get(user=request.user, product=product)
        except:
            cart_object = None

        if cart_object is None:
            Cart.objects.create(
                user=request.user,
                product=product,
                count=quantity,
            )
            messages.success(request, "Maxsulot savatchaga muvaffaqiyatli qo'shildi")
        else:
            cart_object.count += int(quantity)
            cart_object.save()
            messages.success(request, "Savatchadagi maxsulot soni o'zgartirildi")

    context = {
        "product": product
    }
    return render(request, "product_detail.html", context)


def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "Avval tizimga kirish talab etiladi")
        return redirect("signin")

    return render(request, "profile.html")


def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Avval tizimga kirish talab etiladi")
        return redirect("signin")

    # cart_objects = Cart.objects.filter(user=request.user)
    cart_objects = request.user.cart_set.all()

    context = {
        "cart_objects": cart_objects,
    }

    return render(request, "cart.html", context)


def transactions(request):
    return render(request, "transactions.html")


def delete_cart_product(request, id):
    request.user.cart_set.all().filter(id=id).delete()
    return redirect("cart")


def buy(request):
    cart_objects = request.user.cart_set.all()

    for cart_object in cart_objects:
        Transaction.objects.create(
            user=request.user,
            amount=cart_object.product.price * cart_object.count,
            product_name=f"{cart_object.product.name} x{cart_object.count} ta"
        )

    cart_objects.delete()
    return redirect("transactions")

