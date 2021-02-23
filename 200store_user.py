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

CSV_PATH = "./csv/200store_product_product.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            category_id = row[8]
            Product.objects.create(
                    name = row[0],
                    price = Decimal(row[1]),
                    stock = row[2],
                    sale  = Decimal(row[3]),
                    image_url = row[4],
                    total_sales = row[5],
                    create_at = row[6],
                    update_at = row[7],
                    category_id = category_id,
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


CSV_PATH = "./csv/200store_user_user.csv"
with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        grade_id = row[12]
        print(row[12])
        #grade_id = Grade.objects.get(id = grade_id)
        print(grade_id)
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


