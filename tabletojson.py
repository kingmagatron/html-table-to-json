import json
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def html_to_json(content, indent=None):
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")
    
    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = thead.find_all("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower()
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            for index in headers:
                items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        data.append(items)
    return json.dumps(data, indent=indent)

def nested_table_to_json(content, indent=None):
  soup = BeautifulSoup(str(content), "html.parser")
  rows = soup.find_all('tr')
  headers = {}
  thead = soup.find("thead")
  if thead:
    thead = thead.find_all("th")
    for i in range(len(thead)):
      headers[i] = thead[i].text.strip().lower()
  data = []
  for row in rows:
    cells = row.find_all('td')
    if thead:
      items = {}
      for index in headers:
        if headers[index] != "" and headers[index] != "-":
          if cells[index].table:
            items[headers[index]] = html_to_json(cells[index].table)
            ttd = cells[index].table.find_all('td')
            for tds in ttd:
              cells.remove(tds)
            ttr = cells[index].table.find_all('tr')
            for trs in ttr:
              rows.remove(trs)
          else:
            items[headers[index]] = cells[index].text
    else:
      items = []
      for index in cells:
        items.append(index.text.strip())
    data.append(items)
  return json.dumps(data, indent=indent)

if __name__ == "__main__":
    content = "<table> <thead> <th>ID</th> <th>Vendor</th> <th>Product</th> </thead> <tr> <td>1</td> <td>Intel</td> <td>Processor</td> </tr> <tr> <td>2</td> <td>AMD</td> <td>GPU</td> </tr> <tr> <td>3</td> <td>Gigabyte</td> <td>Mainboard</td> </tr></table>"
    content_no_thead = "<table> <tr> <td>1</td> <td>Intel</td> <td>Processor</td> </tr> <tr> <td>2</td> <td>AMD</td> <td>GPU</td> </tr> <tr> <td>3</td> <td>Gigabyte</td> <td>Mainboard</td> </tr></table>"
    
    print(html_to_json(content))
    # returns list of objects as header is present
    # [{"id": "1", "vendor": "Intel", "product": "Processor"}, {"id": "2", "vendor": "AMD", "product": "GPU"}, {"id": "3", "vendor": "Gigabyte", "product": "Mainboard"}]
    
    print(html_to_json(content_no_thead, indent=4))
    # autodetects if thead is there, returns list of list
    # [["1", "Intel", "Processor"], ["2", "AMD", "GPU"], ["3", "Gigabyte", "Mainboard"]]
    
    nested = '''<table> <thead> <th>ID</th> <th>Vendor</th> <th>Product</th> </thead> <tr> <td>1</td> <td><table>
    <tr><td>nested table</td></tr>
    <tr><td>nested table</td></tr>
    </table></td> <td>Processor</td> </tr> <tr> <td>2</td> <td>AMD</td> <td>GPU</td> </tr> <tr> <td>3</td> <td>Gigabyte</td> <td>Mainboard</td> </tr></table>
    '''
    print(nested_table_to_json(nested))
    # [{"id": "1", "vendor": "[[\"nested table\"], [\"nested table\"]]", "product": "Processor"}, {"id": "2", "vendor": "AMD", "product": "GPU"}, {"id": "3", "vendor": "Gigabyte", "product": "Mainboard"}]
    
    nested_no_thead = '''<table>
    <tr>
    <td>First cell in first table. The cell to the right has the second table in it.</td>
    <td>
        <table>
        <tr><td>nested table</td></tr>
        <tr><td>nested table</td></tr>
        </table>
    </td>
    </tr>
    </table>
    ''' 
    print(nested_table_to_json(nested_no_thead))
    # [["First cell in first table. The cell to the right has the second table in it.", "nested table\nnested table", "nested table", "nested table"], ["nested table"], ["nested table"]]
