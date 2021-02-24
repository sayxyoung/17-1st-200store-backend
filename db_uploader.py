import os
import django
import csv
import sys

from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store200.settings")
django.setup()

from product.models import *
from user.models import *
from order.models import *

# 카테고리업로드
CSV_PATH = "./csv/200store_user_grade.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Grade.objects.create(name = row[0])

CSV_PATH = "./csv/200store_user_coupon.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Coupon.objects.create(name = row[0], price = row[1])

CSV_PATH = "./csv/200store_product_category.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Category.objects.create(name = row[0])

CSV_PATH = "./csv/200store_user_user.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            User.objects.create(
                    account  = row[0],
                    password = row[1],
                    name     = row[2],
                    email    = row[3],
                    cell_phone = row[4],
                    home_phone = row[5],
                    home_address = row[6],
                    phone_spam = row[7],
                    email_spam = row[8],
                    total_price = row[14],
                    grade_id = row[9],
                    )

CSV_PATH = "./csv/200store_product_product.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            # category_id = row[8]
            Product.objects.create(
                    name = row[0],
                    price = Decimal(row[1]),
                    stock = row[2],
                    sale  = Decimal(row[3]),
                    image_url = row[4],
                    total_sales = row[5],
                    create_at = row[6],
                    update_at = row[7],
                    category_id = row[8],
                    )

CSV_PATH = "./csv/200store_product_productImage.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            ProductImage.objects.create(
                    product_id = row[0],
                    image_url = row[1]
                    )

CSV_PATH = "./csv/200store_user_address.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Address.objects.create(
                    user_id = row[0],
                    name = row[1],
                    to_person = row[2],
                    to_address = row[3],
                    home_phone = row[4],
                    cell_phone = row[5],
                    is_default = row[6],
                    )

CSV_PATH = "./csv/200store_user_userCoupon.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            UserCoupon.objects.create(
                    user_id = row[0],
                    coupon_id = row[1],
                    validity = row[2],
                    create_at = row[3],
                    )

CSV_PATH = "./csv/200store_user_point.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Point.objects.create(
                    user_id = row[0],
                    content = row[1],
                    value   = row[2],
                    validity = row[3],
                    remaining_point = row[4],
                    create_at = row[5],
                    )

CSV_PATH = "./csv/200store_user_recentlyView.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            RecentlyView.objects.create(
                    user_id = row[0],
                    product_id = row[1],
                    create_at = row[2],
                    )

CSV_PATH = "./csv/200store_product_productLike.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            ProductLike.objects.create(
                    product_id = row[0],
                    user_id = row[1],
                    )

CSV_PATH = "./csv/200store_product_productOption.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            ProductOption.objects.create(
                    product_id = row[0],
                    name = row[1],
                    stock = row[2],
                    )

CSV_PATH = "./csv/200store_product_answerStatus.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            AnswerStatus.objects.create(
                    name = row[0],
                    )

CSV_PATH = "./csv/200store_product_productInquiry.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            ProductInquiry.objects.create(
                    product_id = row[0],
                    user_id = row[1],
                    title = row[2],
                    content = row[3],
                    answer_title = row[4],
                    answer_content = row[5],
                    answer_status_id = row[6],
                    create_at = row[7],
                    )


CSV_PATH = "./csv/200store_order_orderStatus.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            OrderStatus.objects.create(
                    name = row[0],
                    )

CSV_PATH = "./csv/200store_order_cartStatus.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            CartStatus.objects.create(
                    name = row[0],
                    )

CSV_PATH = "./csv/200store_order_order.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Order.objects.create(
                    user_id = row[0],
                    status_id = row[1],
                    address_id = row[2],
                    create_at = row[3],
                    total_price = Decimal(row[4]),
                    is_confirmed = row[5],
                    serial_number = row[6],
                    )

CSV_PATH = "./csv/200store_product_review.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Review.objects.create(
                    product_id = row[0],
                    user_id = row[1],
                    title = row[2],
                    content = row[3],
                    star_rating = int(row[4]),
                    image_url = row[5],
                    )

CSV_PATH = "./csv/200store_product_matching_review.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            MatchingReview.objects.create(
            review_id = row[0],
            order_id = row[1],
            product_id = row[2],
            )

CSV_PATH = "./csv/200store_order_cart.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Cart.objects.create(
                    order_id = row[0],
                    product_id = row[1],
                    option = row[2],
                    quantity = row[3],
                    total_price = Decimal(row[4]),
                    status_id = row[5],
                    )

