import requests
from bs4 import BeautifulSoup
import json
from .models import DayStats
from decimal import Decimal
from django.db.models import Sum,Avg
import datetime


# Step 1: Fetch the HTML content from the URL

class Extract():
    
    def __init__(self):
        self.url = "https://dev-test-d3u.pages.dev/coffee"
        self.page = 1
        self.extracted_rows = []
        
    def HTML_TO_Python(self):
        
        url = self.url+"?page="+str(self.page) + "&per_page=20" # Replace with the URL of the HTML page
        response = requests.get(url)
        html_content = response.text

        # Step 2: Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Step 3: Find the table in the HTML
        table = soup.find("table")  # Finds the first table; use `soup.find_all("table")` for multiple tables

        # Step 4: Extract table headers (if available)
        headers = []
        if table:
            header_row = table.find("thead")  # Look for headers in <thead> or first <tr>
            if header_row:
                headers = [header.get_text(strip=True) for header in header_row.find_all("th")]

        # Step 5: Extract table rows and data
        table_data = []
        if table:
            data_rows = table.find("tbody")
            rows = data_rows.find_all("tr")  # Find all rows in the table
            for row in rows:
                cells = row.find_all(["td"])  # Extract both <td> and <th> elements
                if cells:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        # Use headers if available, otherwise use column indices
                        key = headers[i]
                        row_data[key] = cell.get_text(strip=True)
                    table_data.append(row_data)

        # Step 6: Convert the table data to JSON
        # json_data = json.dumps(table_data, indent=4)

        # Step 7: Print or save the JSON data
        # print(json_data)

        # print(table_data)
        
        return table_data
    
    def run(self):

        data = self.HTML_TO_Python()

        while len(data):

            self.extracted_rows += data
            self.page += 1
            data = self.HTML_TO_Python()
        
        self.clean_data()
        # self.to_JSON()
        
    
    def clean_data(self):

        cleaned_data = []

        for row in self.extracted_rows:
            temp = {}
            for key,value in row.items():
                value = value.strip("USD$")
                value = value.strip()
                temp[key]=value
            
            cleaned_data.append(temp)
        
        self.extracted_rows = cleaned_data
    
    # def to_JSON(self):

    #     self.extracted_rows = json.dumps(self.extracted_rows, indent=4)



class Store():

    def __init__(self,extract):
        self.data = extract.extracted_rows
        self.fields = ["date", "cups_sold" ,"cup_price"  ,"total_sale" ,"customer_count","discount" ,"profit"]
         
    def list_to_objects(self):

        l=[]

        for row in self.data:
            temp = {}
            i=0
            for key,val in row.items():
                convert = Convert(self.fields[i],val)
                temp[self.fields[i]] = convert.val
                i+=1

            l.append(DayStats(**temp))

        return l
    
    def create_or_update(self):

        objects = self.list_to_objects()

        DayStats.objects.bulk_create(objects,
            update_conflicts=True,
            unique_fields=['date'],
            update_fields=self.fields[1:])
        return
    
    def run(self):

        self.create_or_update()

        print("DONE !!")


    

class Convert():

    def __init__(self,field,val):
        self.field = field
        self.val = val

        self.run()
    
    def run(self):
        
        if self.field in ['cups_sold','customer_count','discount']:
            self.val = int(self.val)
        elif self.field in ['date']:
            self.val = datetime.datetime.strptime(self.val, "%d-%m-%Y").strftime("%Y-%m-%d")
        else:
            self.val = Decimal(self.val)

        
        

class QueryManager(object):

    agg_fun = {}

    def agg(q):
        for field in DayStats._meta.get_fields():
            field = field.name
            key = f"{field}_total"
            if field not in ['cup_price','date','id']: 
                val = Sum(f"{field}")
                QueryManager.agg_fun[key]=val
            elif field in ['cup_price']:
                val = Avg(f"{field}")
                QueryManager.agg_fun[key]=val

        # print(QueryManager.agg_fun)
        q = q.aggregate(**QueryManager.agg_fun)
        print("b")
        return q
    
    @staticmethod
    def run(year):

        print("a")
        
        queries_by_month = {} 

        for i in range (1,13):

            start = f"{year}-{i}-1"
            end = f"{year}-{i+1}-1"
            if i==12:
                end = f"{year+1}-1-1"
            q = DayStats.objects.filter(date__gte=start,date__lt=end)
            queries_by_month[i] = QueryManager.agg(q)

        return queries_by_month
    

