from flask import Flask, request
from flask import Response
import pandas as pd
import sqlite3
import markdown
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

@app.route('/home')
def home():
    conn = sqlite3.connect('data/chinook.db')
    albums = pd.read_sql_query("SELECT * FROM albums", conn)
    return(albums.head().to_json())

@app.route('/country')
def list_country():
    conn = sqlite3.connect('data/chinook.db')
    country = pd.read_sql_query("SELECT * FROM customers", conn)
    json_country = pd.DataFrame(country['Country'].unique()).to_json()

    resp = Response(response=json_country,
                    status=200,
                    mimetype="application/json")

    return(resp)

@app.route('/invoice/total/freq/<country>')
def freq_invoices(country):
    conn = sqlite3.connect('data/chinook.db')
    invoice_customer = pd.read_sql_query("SELECT invoices.InvoiceId, customers.Country, customers.City \
                   FROM invoices \
                   LEFT JOIN customers ON customers.CustomerID = invoices.CustomerID",
                 conn)
    
    invoice_customer['InvoiceId'] = invoice_customer['InvoiceId'].astype('object')
    invoice_customer[['Country', 'City']] = invoice_customer[['Country', 'City']].astype('category', errors='raise')
    invoice_customer = invoice_customer.groupby(by=['Country', 'City']).count().rename(columns={'InvoiceId': 'TotalInvoice'}).reset_index(level=[0,1])

    cond = invoice_customer['Country'] == str(country)
    json_data = invoice_customer[cond].dropna().to_json()

    resp = Response(response=json_data,
                    status=200,
                    mimetype="application/json")
    return(resp)

@app.route('/invoice/total/<year>')
def total_invoices(year):
    year = int(year)
    if year%1!=0:
        return("Should be integer")
    
    if (year < 2009) or (year > 2014):
        return("Should be integer and from 2009 - 2013")

    conn = sqlite3.connect('data/chinook.db')
    total_invoice = pd.read_sql_query("SELECT InvoiceDate, InvoiceId, Invoices.CustomerId, Country, City, Total \
                   FROM invoices \
                   LEFT JOIN customers ON customers.CustomerID = invoices.CustomerID",
                 conn)
    total_invoice['InvoiceDate'] = pd.to_datetime(total_invoice['InvoiceDate'])
    total_invoice = total_invoice.groupby(by=['InvoiceDate','Country', 'City'])['Total'].agg(Total='sum').reset_index()
    total_invoice['year'] = total_invoice['InvoiceDate'].dt.year

    cond = total_invoice['year'] == year
    json_data = total_invoice[cond].to_json()

    resp = Response(response=json_data,
                    status=200,
                    mimetype="application/json")
    return(resp)

@app.route('/customer')
def customer():
    conn = sqlite3.connect('data/chinook.db')
    json_data = pd.read_sql_query("SELECT * FROM customers", conn).to_json()

    resp = Response(response=json_data,
                    status=200,
                    mimetype="application/json")
    return(resp)

@app.route('/customer/topbuy/<customerid>')
def customer_topbuy(customerid):
    print(customerid)
    conn = sqlite3.connect('data/chinook.db')
    data = pd.read_sql_query("SELECT artists.ArtistId, \
                   artists.Name as ArtistName, albums.AlbumId, albums.Title as albumTitle, \
                   customers.CustomerId, \
                   COUNT(customers.CustomerId) AS TotalInvoice  \
                   FROM invoice_items \
                   LEFT JOIN invoices on invoices.InvoiceId = invoice_items.InvoiceId \
                   LEFT JOIN customers on customers.CustomerId = invoices.CustomerId \
                   LEFT JOIN tracks on tracks.TrackId = invoice_items.TrackId \
                   LEFT JOIN albums on albums.AlbumId = tracks.AlbumId \
                   LEFT JOIN artists on artists.ArtistId = albums.ArtistId \
                   WHERE customers.CustomerId = ? \
                   GROUP BY artists.ArtistId \
                   ORDER BY TotalInvoice DESC",
                 conn, params=(customerid,))

    json_data = data.to_json()

    resp = Response(response=json_data,
                    status=200,
                    mimetype="application/json")
    return(resp)

@app.route('/docs')
def docs():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    formatter = HtmlFormatter(style="emacs",full=True,cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template_string
    return md_template

@app.route('/')
def index():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    formatter = HtmlFormatter(style="emacs",full=True,cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template_string
    return md_template

if __name__ == '__main__':
    app.run(debug=True, port=5000)