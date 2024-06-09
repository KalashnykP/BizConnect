"""
product.py

Definition of the Product model and functions to interact with product records in
the database
"""

class Product:
    """ An object representation of a product. Each product must have a title, author
    first name, author last name, publication year after 1900, and account_id
    of the patron that the book is checked out to (can be null).
    """

    def __init__(self, product_name, seller_name, style, price, qty):
        self._product_name = product_name
        self._seller_name = seller_name
        self._style = style
        self._price = price
        self._qty = qty


class ProductDB:
    """ Manages CRUD functions for Books in the database
    """

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor
    

    
    def select_all_products(self):
        """ Gets a list of all books in database

            Returns:
                list of dictionaries representing products: all products in the products
                table
        """

        select_all_query = """
            SELECT * from products;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()


    def select_product_by_id(self, product_id):
        """ Returns a list with the product corresponding the provided product_id

            Args:
                product_id: The product_id of the product to be selected

            Returns:
                list of a dictionary representing a product: the product record
                corresponding to the given product_id. Will be an empty list
                if no product with the provided product_id exists
        """

        select_product_by_id = """
                SELECT * from products WHERE product_id = %s;
        """
        self._cursor.execute(select_product_by_id, (product_id,))
        return self._cursor.fetchall()


    def select_all_products_by_name(self, name):
        """ Returns a list of all products with a title similar to the provided search
        term.

        Args:
            title (string): The title or keyword to search for in the title of
            a product

        Returns:
            list of dictionaries representing products: the product records
            matching the given title. Will be an empty list
            if no product matching the given title exists
        """

        select_products_by_name = """
            SELECT * from products WHERE product_name LIKE %s;
        """
        self._cursor.execute(select_products_by_name, (f"%{name}%",))
        return self._cursor.fetchall()


    def insert_product(self, product):
        """ Adds a new product to the products table.

        Args:
            product: The product object to be added

        Returns:
            product_id: the product_id of the newly added product record
        """

        insert_query = """
            INSERT INTO products (product_name, seller_name, style, price, qty)
            VALUES (%s, %s, %s, %s, %s);
        """

        self._cursor.execute(insert_query, (product._product_name, product._seller_name, product._style, product._price, product._qty))
        self._cursor.execute("SELECT LAST_INSERT_ID() product_id")
        product_id = self._cursor.fetchone()
        self._db_conn.commit()

        return product_id


    def update_product(self, product_id, new_product):
        """ Sets the title, author_fname, author_lname, publication_year, and 
        checked_out_to of a given product. 

        Args:
            product_id: The product_id of the product record to be updated
            product: A product object containing the updated attributes of the product
        """

        update_query = """
            UPDATE products
            SET product_name=%s, 
            seller_name=%s, 
            style=%s,
            price=%s,
            qty=%s
            WHERE product_id=%s;
        """
        self._cursor.execute(update_query, (new_product._product_name, new_product._seller_name, new_product._style, new_product._price, new_product._qty, product_id))
        self._db_conn.commit()


    def delete_product_by_id(self, product_id):
        """ Deletes the product record corresponding to the given product_id

        Args:
            product_id: The product_id of the product record to be deleted
        """
        delete_query = """
            DELETE from products
            WHERE product_id=%s;
        """
        self._cursor.execute(delete_query, (product_id,))
        self._db_conn.commit()
    

    # def select_available_products(self):
    #     """ Returns a list of all products available for checkout in database as 
    #     dictionaries. Available products must not be currently checked out to 
    #     anyone.

    #     Returns:
    #         list of dictionaries representing products: A list of all products that 
    #         are not currently checked out to someone.
    #     """

    #     select_available_books = """
    #             SELECT * from books WHERE checked_out_to is NULL;
    #     """
    #     self._cursor.execute(select_available_books)
    #     return self._cursor.fetchall()

    
    # def select_all_books_by_patron(self, patron_id):
    #     """ Returns a list of all books that a given patron has currently 
    #     checked out

    #     Args:
    #         patron_id: The account id of a patron

    #     Returns:
    #         list of dictionaries representing books: A list of all books that 
    #         are checked out to the given patron
    #     """

    #     select_all_books_by_patron = """
    #             SELECT * from books WHERE checked_out_to = %s;
    #     """
    #     self._cursor.execute(select_all_books_by_patron, (patron_id,))
    #     return self._cursor.fetchall()
