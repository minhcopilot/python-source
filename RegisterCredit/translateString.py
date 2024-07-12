import sys
import os
import pandas as pd
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QMessageBox

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def process_excel_data(code_file_path):
    # Read the main Excel file
    main_file_path = resource_path('danhsach.xlsx')
    df = pd.read_excel(main_file_path)
    
    # Read the code Excel file
    df_code = pd.read_excel(code_file_path)
    
    # Process each row in the main dataframe
    result_parts = []
    for _, row in df.iterrows():
        ma_hp = str(row['Mã HP'])
        ten_lhp = row['Tên LHP']
        
        # Check if the LHP name exists in the code file
        if ten_lhp in df_code['Tên LHP'].values:
            # Extract the last two digits from LHP name
            match = re.search(r'\d{2}$', ten_lhp)
            if match:
                last_two_digits = match.group()
                
                # Create the new code format without decimal part
                new_code = f"124{ma_hp.split('.')[0]}{last_two_digits}"  # Remove decimal part
                result_parts.append(new_code)
    
    # Join the parts with '&mldk='
    result_string = '&mldk='.join(result_parts)
    
    # Create the course registration JavaScript string
    registration_js = f"""
var count = 0;
var last = "";
async function doc() {{
    return await new Promise(resolve => {{
        count++;
        document.title = "[" + count + "]";
        $.post('http://daotao.ute.udn.vn/dkmhcmtbk.asp', "mldk={result_string}", function(data) {{
            document.html.innerHTML = data;
            var body = data;
            var a = body.match(/Xin mời đăng nhập(.*?)ký môn học/)[1];
            if (a == null) {{
                alert("ok");
            }} else {{
                setTimeout(resolve, 300);
            }}
        }});
    }});
}}
async function main() {{
    for (i = 0; i < 100000000000; i++) {{
        await doc();
    }}
}}
main();
    """
    
    # Get login information from the code file
    login_info = df_code.iloc[0]  # Assuming the first row contains login info
    ma_sv = str(login_info['tk']).split('.')[0]
    password = login_info['mk']
     # Handle the password field to keep the original format
    password = login_info['mk']
    if isinstance(password, pd.Timestamp):
        password = password.strftime('%m/%d/%Y')
    else:
        password = str(password)
    # Create the login JavaScript string
    login_js = f"""
var count = 0;
async function doc() {{
    return await new Promise(resolve => {{
        count++;
        document.title = "[" + count + "]";
        $.post('http://daotao.ute.udn.vn/svlogin.asp', {{
            maSV: '{ma_sv}',
            pw: '{password}',
        }}, function(data) {{
            document.html.innerHTML = data;
            setTimeout(resolve, 100);
        }});
    }});
}}
async function main() {{
    for (i = 0; i < 100000000000; i++) {{
        await doc();
    }}
}}
main();
    """
    
    return registration_js, login_js

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Excel Processing Application'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 640
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QVBoxLayout()
        
        self.btn = QPushButton('Chọn file code', self)
        self.btn.clicked.connect(self.chooseFile)
        layout.addWidget(self.btn)
        
        self.registration_text = QTextEdit(self)
        layout.addWidget(self.registration_text)
        
        self.login_text = QTextEdit(self)
        layout.addWidget(self.login_text)
        
        self.setLayout(layout)
        
        self.show()
    
    def chooseFile(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file Excel", "", "Excel Files (*.xlsx)", options=options)
        if file_path:
            try:
                registration_result, login_result = process_excel_data(file_path)
                self.registration_text.setPlainText(registration_result)
                self.login_text.setPlainText(login_result)
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi xử lý file: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())