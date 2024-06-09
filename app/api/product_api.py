"""
product_api.py

Routes for the API and logic for managing Books.
"""

from flask import g, request, jsonify, Blueprint

from models.product import Product, ProductDB
from models.library import Library

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
product_api_blueprint = Blueprint("product_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a product to the end of the url
#   so we can retrieve a specific product or the entire list of products as a JSON object
@product_api_blueprint.route('/api/v1/products/', defaults={'product_id':None}, methods=["GET"])
@product_api_blueprint.route('/api/v1/products/<int:product_id>/', methods=["GET"])
def get_products(product_id):
    """
    get_products can take urls in a variety of forms:
        * /api/v1/products/ - get all products
        * /api/v1/products/1 - get the products with id 1 (or any other valid id)
        * /api/v1/products/?search="eggs" - find all products with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the productDB object with the mysql connection and cursor objects
    productdb = ProductDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the product is not supplied then we are either returning all
    #   products or any products that match the search query string.
    if product_id is None:
        # Logic to find all or multiple products

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = productdb.select_all_products()
        else:
            # All products matching the query string "search"
            result = productdb.select_all_products_by_name(args['search'])
    
    else:
        # Logic to request a specific products
        # We get a specific products based on the provided product ID
        result = productdb.select_product_by_id(product_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the products found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "products": result}), 200


@product_api_blueprint.route('/api/v1/products/', methods=["POST"])
def add_product():
    """Add a new product to the products table

    Returns: 
        json: A status message including the product_id of the newly added product
        HTML status code: 200 if successful
    """

    productdb = ProductDB(g.mysql_db, g.mysql_cursor)
        
    product = Product(request.json['product_name'], request.json['seller_name'], 
    request.json['style'], request.json['price'],
    request.json['qty'])      

    new_book_id = productdb.insert_product(product)['product_id']
    
    return jsonify({"status": "success", "product_id": new_product_id}), 200


@product_api_blueprint.route('/api/v1/products/<int:product_id>/', methods=["PUT"])
def update_product(product_id):
    """Update the attributes of a product

    Args:
        product_id: the product_id of the product record to be updated

    Returns: 
        json: A status message including the product_id of the newly added product
        HTML status code: 200 if successful
    """

    productdb = ProductDB(g.mysql_db, g.mysql_cursor)

    product = Product(request.json['product_name'], request.json['seller_name'], 
    request.json['style'], request.json['price'], 
    request.json['qty'])

    productdb.update_product(product_id, product)
    
    return jsonify({"status": "success", "product_id": product_id}), 200


@product_api_blueprint.route('/api/v1/products/<int:product_id>/', methods=["DELETE"])
def delete_product(product_id):
    """Delete a product from the database

    Args:
        product_id: the product_id of the product record to be deleted

    Returns: 
        json: A status message including the product_id of the newly added product
        HTML status code: 200 if successful
    """

    productdb = ProductDB(g.mysql_db, g.mysql_cursor)
    productdb.delete_product_by_id(product_id)
        
    return jsonify({"status": "success", "product_id": product_id}), 200


# @book_api_blueprint.route('/api/v1/books/<int:patron_id>/<int:book_id>/', methods=["POST"])
# def checkout_book(patron_id, book_id):
#     """Assigns a book to a patron, signifying the book has been checked out

#     Args:
#         patron_id: the account_id of the patron checking out the book
#         book_id: the book_id of the book to be checked out

#     Returns: 
#         json: A status message including the book_id of the newly added book
#         HTML status code: 200 if successful, 409 if book could not be checked out
#     """
    
#     bookdb = BookDB(g.mysql_db, g.mysql_cursor)
#     my_library = Library(g.mysql_db, g.mysql_cursor)
        
#     book = my_library.checkout_book(patron_id, book_id) 

#     if book[0] == False:
#         # Conflict: the book could not be checked out
#         return jsonify({"status": "failure", "patron_id": patron_id, 
#         "book_id": book_id}), 409 
#     else:
#         return jsonify({"status": "success", "patron_id": patron_id, 
#         "book_id": book_id}), 200


#     @book_api_blueprint.route('/api/v1/books/return-book/<int:book_id>/', methods=["POST"])
#     def return_book(self, book_id):
#         """Updates a book to be no longer checked out.

#         Args:
#             book_id: The book_id of the book to be returned.
        
#         Returns:
#             json: A status message including the book_id of the returned book
#             HTML status code: 200 if successful
#         """

#         # database = BookDB(self._db_conn, self._cursor)
#         # selected_book = database.select_book_by_id(book_id)

#         # # if not selected_book:
#         # #     return [False, "Selected book not in database"]

#         # new_book = Book(selected_book[0]["title"], selected_book[0]["author_fname"], 
#         # selected_book[0]["author_lname"], selected_book[0]["publication_year"], None)

#         #bookdb = BookDB(g.mysql_db, g.mysql_cursor)
#         my_library = Library(g.mysql_db, g.mysql_cursor)
            
#         my_library.return_book(book_id) 

#         return jsonify({"status": "success", "book_id": book_id}), 200
