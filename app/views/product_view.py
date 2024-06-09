"""
product_view.py

Collection of functions performing CRUD operations on product records for a
given route
"""

from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.product_api import Product, ProductDB
# from api.patron_api import PatronDB
from models.library import Library

product_list_blueprint = Blueprint('product_list_blueprint', __name__)

@product_list_blueprint.route('/', methods=["GET", "POST"])
def index():
    """No GET or POST requests are made from the index route, so this function
    simply renders index.html 
    """
    # database = BookDB(g.mysql_db, g.mysql_cursor)

    # # We know that if a POST is made from index (/), then that was the user
    # # selecting the 'Checkout Books' button
    # if request.method == "POST":
    #     book_ids = request.form.getlist("book_item")

    #     for book_id in book_ids:
    #         database.delete_book_by_id(book_id) 

    # return render_template('index.html', book_list=database.select_all_books())
    return render_template('index.html')


@product_list_blueprint.route('/product-entry')
def product_entry():
   """Renders the product-entry.html page
   """

   return render_template('product-entry.html')


@product_list_blueprint.route('/add-product', methods=["POST"])
def add_product():
    """Add a new product to the databse

    Returns:
        render_template: redirects user to the index route
    """

    product_name = request.form.get("product_name")
    seller_name = request.form.get("seller_name")
    style = request.form.get("style")
    price = request.form.get("price")
    qty = request.form.get("qty")
    
    new_product = Product(product_name, seller_name, style, price, qty)
    database = ProductDB(g.mysql_db, g.mysql_cursor)

    database.insert_product(new_product)

    return redirect('/')


@product_list_blueprint.route('/product-update', methods=["GET", "POST"])
def edit_products():
    product_database = ProductDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        product_id = request.form.get("product_id")
        new_product_name = request.form.get("product_name")
        new_seller_name = request.form.get("seller_name")
        new_price = request.form.get("price")
        new_style = request.form.get("style")
        new_qty = request.form.get("qty")
        product_database.update_product(product_id, Product(new_product_name,
            new_seller_name, new_style, new_price, new_qty))
        return redirect('/')

    product_database = ProductDB(g.mysql_db, g.mysql_cursor)
    return render_template('/product-update.html',
        products=product_database.select_all_products())


# @book_list_blueprint.route('/book-checkout-selection')
# def book_checkout_selection():
#     """Renders checkout-book.html page with a list of all books available for
#     checkout
#     """

#     database = BookDB(g.mysql_db, g.mysql_cursor)

#     return render_template('checkout-book.html', book_list=database.select_available_books())


# @book_list_blueprint.route('/checkout-book', methods=["POST"])
# def checkout_book():
#     """Updates a book record to be checked-out to a patron.

#     Returns:
#         render_template: If successful, renders a checkout-success.html page,
#         if failed, renders a checkout-failure.html page
#     """

#     database = BookDB(g.mysql_db, g.mysql_cursor)
#     my_library = Library(g.mysql_db, g.mysql_cursor)

#     # We know that if a POST is made from this route, then that was the user
#     # selecting the 'Checkout Books' button
#     if request.method == "POST":
#         book_ids = request.form.getlist("book_item")
#         patron_id = request.form.get("id")
#         book_list = []
    
#         for book_id in book_ids:
#             new_book = my_library.checkout_book(patron_id, book_id)

#             if new_book[0] == False:
#                 return render_template('checkout-failure.html', book_list=book_list, 
#                 error_message=new_book[1])

#             book_list.append(new_book[1])
        
#         return render_template('checkout-success.html', book_list=book_list)


@product_list_blueprint.route('/product-list', methods=["GET"])
def patron_list():
    database = ProductDB(g.mysql_db, g.mysql_cursor)

    return render_template('product-list.html', product_table=database.select_all_products())


@product_list_blueprint.route('/product-remove', methods=['GET', 'POST'])
def product_delete():
    database = ProductDB(g.mysql_db, g.mysql_cursor)

    if request.method == 'POST':
        product_id_to_delete = request.form.get("product_id_to_delete")
        database.delete_product_by_id(product_id_to_delete)
        return redirect('/')

    return render_template('/product-remove.html', products=database.select_all_products()
    )

@product_list_blueprint.route('/product-search', methods=["GET"])
def product_search():
    database = ProductDB(g.mysql_db, g.mysql_cursor)

    query = request.form.get("query")

    return render_template('/product-search.html', product_table=database.select_products_by_name(query))

# @book_list_blueprint.route('/book-return', methods=['POST'])
# def book_return():
#    """Renders the book-return.html page
#    """
#    database = BookDB(g.mysql_db, g.mysql_cursor)
#    patron_id = request.form.get("account_id")

#    return render_template('book-return.html', patrons_books=database.select_all_books_by_patron(patron_id))


# @book_list_blueprint.route('/enter-patron-id')
# def enter_patron_id():
#    """Gets user's patron id and sends it to the /book-return form
#    """

#    database = PatronDB(g.mysql_db, g.mysql_cursor)

#    return render_template('enter-patron-id.html', patron_list=database.select_all_patrons())


# @book_list_blueprint.route('/return-book-to-library', methods=['POST'])
# def return_book_to_library():
#    """Updates book to be available for checkout again
#    """
#    my_library = Library(g.mysql_db, g.mysql_cursor)
#    book_id = request.form.get("book_id")

#    my_library.return_book(book_id)

#    return redirect('/')
