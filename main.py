#!/usr/bin/env python3
"""
Lab: SQL Table Relations - Complete solution
This script runs all SQL queries from the lab assessment on the CRM database.
"""

import sqlite3
import pandas as pd

def main():
    # Connect to the database
    conn = sqlite3.connect('data.sqlite')
    
    # Step 1: Boston employees
    df_boston = pd.read_sql("""
        SELECT e.firstName, e.lastName, e.jobTitle
        FROM employees e
        JOIN offices o ON e.officeCode = o.officeCode
        WHERE o.city = 'Boston'
    """, conn)
    print("Step 1 - Boston employees:", df_boston.shape)
    
    # Step 2: Offices with zero employees
    df_zero_emp = pd.read_sql("""
        SELECT o.officeCode, o.city
        FROM offices o
        LEFT JOIN employees e ON o.officeCode = e.officeCode
        WHERE e.employeeNumber IS NULL
    """, conn)
    print("Step 2 - Offices with zero employees:", df_zero_emp.shape)
    
    # Step 3: All employees with office city/state (including those without office)
    df_employee = pd.read_sql("""
        SELECT e.firstName, e.lastName, o.city, o.state
        FROM employees e
        LEFT JOIN offices o ON e.officeCode = o.officeCode
        ORDER BY e.firstName, e.lastName
    """, conn)
    print("Step 3 - All employees:", df_employee.shape)
    
    # Step 4: Customers with no orders
    df_contacts = pd.read_sql("""
        SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
        FROM customers c
        LEFT JOIN orders o ON c.customerNumber = o.customerNumber
        WHERE o.orderNumber IS NULL
        ORDER BY c.contactLastName
    """, conn)
    print("Step 4 - Customers with no orders:", df_contacts.shape)
    
    # Step 5: Payment report with numeric sorting
    df_payment = pd.read_sql("""
        SELECT c.contactFirstName, c.contactLastName, 
               CAST(p.amount AS REAL) AS amount, p.paymentDate
        FROM customers c
        JOIN payments p ON c.customerNumber = p.customerNumber
        ORDER BY amount DESC
    """, conn)
    print("Step 5 - Payments:", df_payment.shape)
    
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
    print("Step 6 - High credit limit employees:", df_credit.shape)
    
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
    print("Step 7 - Product sales:", df_product_sold.shape)
    
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
    print("Step 8 - Distinct customers per product:", df_total_customers.shape)
    
    # Step 9: Number of customers per office
    df_customers = pd.read_sql("""
        SELECT o.officeCode, o.city,
               COUNT(c.customerNumber) AS n_customers
        FROM offices o
        LEFT JOIN employees e ON o.officeCode = e.officeCode
        LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        GROUP BY o.officeCode
    """, conn)
    print("Step 9 - Customers per office:", df_customers.shape)
    
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
    print("Step 10 - Employees selling low-reach products:", df_under_20.shape)
    
    # Close connection
    conn.close()
    
    # Optional: Save all dataframes to Excel or CSV for inspection
    # Uncomment the lines below if needed:
    # with pd.ExcelWriter('lab_results.xlsx') as writer:
    #     df_boston.to_excel(writer, sheet_name='BostonEmployees', index=False)
    #     df_zero_emp.to_excel(writer, sheet_name='ZeroEmployeesOffices', index=False)
    #     df_employee.to_excel(writer, sheet_name='AllEmployees', index=False)
    #     df_contacts.to_excel(writer, sheet_name='CustomersNoOrders', index=False)
    #     df_payment.to_excel(writer, sheet_name='Payments', index=False)
    #     df_credit.to_excel(writer, sheet_name='HighCreditEmployees', index=False)
    #     df_product_sold.to_excel(writer, sheet_name='ProductSales', index=False)
    #     df_total_customers.to_excel(writer, sheet_name='ProductCustomers', index=False)
    #     df_customers.to_excel(writer, sheet_name='CustomersPerOffice', index=False)
    #     df_under_20.to_excel(writer, sheet_name='Under20ProductEmployees', index=False)
    # print("All results saved to lab_results.xlsx")

if __name__ == "__main__":
    main()