# 200 store
<div align="center">
  <img src="https://user-images.githubusercontent.com/74485621/109629698-72b1fa00-7b87-11eb-9fd2-6e89988293c4.png"><br>
</div>

-----------------
## What is it?
**200 store**  is a project to clone the core functions of the web-based online commerce platform ['BAEMIN STORE'](https://store.baemin.com)

## Project Structure
```
├── order
├── product
├── store200
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── user
├── .gitignore
├── manage.py
├── requirements.txt
└── utils.py
```
* `order`: Include API function code related to the orders
	* `CartView`, `OrderListView` : The functions to show list of the cart and order. Implementing the C.R.U.D using the ORM in Django
* `product` : Include API feature code related to the products
    * `ProductListView` : The function to show the product list. `order_by` and `timezone.timedelta`
    * `ProductDetailView`, `ProductLikeView` : The function to show the detail list of product and like. `chaining` in the Django.
    * `MainView` : The function to show the main of the website. `Function`, `Constant`, `order_by`, `timezone.timedelta`.
    * `ReivewView` : The function to show the review of the user.  
* `user` : Include API function code related to user    
    * `SignInView`, `SignUpView` : The function about join and login. `bcrypt`, `jwt` and `regular expression` 
    * `MyPageMainView` : The function to show the my page of the user.`annotate`
* `utils.py` : The module about permission. `decorator`

## ERD 
URL : https://aquerytool.com:443/aquerymain/index/?rurl=f0cadad2-6e0e-4fb8-acd2-693c65e993cf&

Password : 818ycs

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/sayxyoung/17-1st-200store-backend

## Endpoint
<div align="center">
  <img src="https://user-images.githubusercontent.com/74485621/115168101-c905d880-a0f4-11eb-8880-aa4bd5e47516.png"><br>
</div>

## Reference
👉🏻 [VIDEO](https://www.youtube.com/watch?v=OLsMR11oai8https://www.youtube.com/watch?v=OLsMR11oai8)

👉🏻 [PROJECT TECHNICAL DOCUMENTATION](https://www.notion.so/Project-technical-documentation-fecc5c24866d4536affc56df6b82c483) 