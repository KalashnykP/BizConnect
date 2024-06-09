"""
Collection of functions to help establish the database
"""
import mysql.connector


# Connect to MySQL and the cyberbrary database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


# Setup for the Database
# Will erase the database if it exists
def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    # cursor.execute(
    #     f""" 
    #     CREATE TABLE patrons
    #     (
    #         account_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
    #         first_name VARCHAR(50),
    #         last_name VARCHAR(50),
    #         account_type ENUM('STUDENT', 'PROFESSOR', 'STAFF'),
    #         CONSTRAINT pk_patrons PRIMARY KEY (account_id)
    #     );
    #     """
    # )
    cursor.execute(
        f""" 
        CREATE TABLE products
        (
            product_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            product_name VARCHAR(50),
            seller_name VARCHAR(50),
            style VARCHAR(50),
            price VARCHAR(50),
            qty VARCHAR(50),
            CONSTRAINT pk_products PRIMARY KEY (product_id)
        );
        """
    )
    # cursor.execute(
    #     f""" 
    #     CREATE TABLE courses
    #     (
    #         course_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
    #         course_title VARCHAR(50),
    #         reference_book SMALLINT UNSIGNED,
    #         CONSTRAINT fk_reference_book FOREIGN KEY (reference_book)
    #         REFERENCES books (book_id),
    #         CONSTRAINT pk_courses PRIMARY KEY (course_id)
    #     );
    #     """
    # )
    # cursor.execute(
    #     f""" 
    #     CREATE TABLE course_patrons
    #     (
    #         account_id SMALLINT UNSIGNED,
    #         course_id SMALLINT UNSIGNED,
    #         CONSTRAINT fk_account_ID FOREIGN KEY (account_id)
    #         REFERENCES patrons (account_id),
    #         CONSTRAINT fk_course_ID FOREIGN KEY (course_id)
    #         REFERENCES courses (course_id),
    #         CONSTRAINT pk_course_members PRIMARY KEY (account_id, course_id)
    #     );
    #     """
    # )
    cursor.close()
    conn.close()
