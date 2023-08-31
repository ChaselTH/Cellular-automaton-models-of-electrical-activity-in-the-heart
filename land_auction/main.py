from bs4 import BeautifulSoup
import openpyxl

# 读取保存的HTML源码文件
with open('土拍大数据中心.html', 'r', encoding='utf-8') as file:
    html_source = file.read()

# 解析HTML源码
soup = BeautifulSoup(html_source, 'html.parser')

# 创建一个Excel工作簿
workbook = openpyxl.Workbook()
sheet = workbook.active

# 清空工作表中的所有内容（如果之前有内容）
sheet.delete_rows(idx=1, amount=sheet.max_row)

# 找到所有包含表格数据的行（<tr>标签）
table_rows = soup.find_all('tr')

for row in table_rows:
    # 找到每一行的列数据（<td>标签）
    columns = row.find_all('td')

    row_data = []
    for column in columns:
        div_cell = column.find('div', class_='cell')
        if div_cell is not None:
            cell_value = div_cell.get_text(strip=True)
            row_data.append(cell_value)
        else:
            row_data.append("")  # 如果没有找到数据，将空字符串添加到行数据

    # 将提取的行数据写入Excel
    sheet.append(row_data)

# 保存Excel文件
workbook.save('table_data.xlsx')
