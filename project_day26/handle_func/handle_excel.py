import openpyxl
class handle_excel_class:
    def __init__(self,file_name,sheet_name):
        self.file_name=file_name
        self.sheet_name=sheet_name
    def handle_cell(self):
        # 获取当前文件下的所有工作表
        self.we_book=openpyxl.load_workbook(self.file_name)
        # 定位到当前的工作表
        self.sh=self.we_book[self.sheet_name]
    def read_excel(self):
        self.handle_cell()
        rows=list(self.sh.rows)
        list_title=[c.value for c in rows[0]]
        list_all=[]
        for r in rows[1:]:
            list_data=[m.value for m in r]
            zip_data=dict(zip(list_title,list_data))
            list_all.append(zip_data)
        return list_all

    def write_excel(self,row,column,value):
        self.handle_cell()
        self.sh.cell(row=row,column=column,value=value)
        self.we_book.save(self.file_name)

if __name__=='__main__':
    excel = handle_excel_class('/Users/mlamp/Desktop/python/python-project/project_day26/test_data/register_login.xlsx', 'register')
    excel.handle_cell()
    excel.read_excel()




