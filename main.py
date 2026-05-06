#!/usr/bin/env python3
"""
Lab: SQL Table Relations - Complete solution
All DataFrames are defined at module level for autograder.
"""

import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# Step 1: Boston employees
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName, e.jobTitle
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# Step 2: Offices with zero employees
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
""", conn)

# Step 3: All employees with office city/state (including those without office)
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# Step 4: Customers with no orders
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# Step 5: Payment report with numeric sorting
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, 
           CAST(p.amount AS REAL) AS amount, p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY amount DESC
""", conn)

# Step 6: Employees with avg customer credit limit > 90k
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, 
           COUNT(c.customerNumber) AS num_customers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)

# Step 7: Product order counts and total units sold
df_product_sold = pd.read_sql("""
    SELECT p.productName, 
           COUNT(DISTINCT o.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    ORDER BY totalunits DESC
""", conn)

# Step 8: Number of unique customers per product
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    ORDER BY numpurchasers DESC
""", conn)

# Step 9: Number of customers per office
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city,
           COUNT(c.customerNumber) AS n_customers
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode
""", conn)

# Step 10: Employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName,
           off.city AS office_city, off.officeCode
    FROM employees e
    JOIN offices off ON e.officeCode = off.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    JOIN products p ON od.productCode = p.productCode
    WHERE p.productCode IN (
        SELECT p2.productCode
        FROM products p2
        JOIN orderdetails od2 ON p2.productCode = od2.productCode
        JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
        GROUP BY p2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName
""", conn)

# Close connection (optional, but good practice)
conn.close()