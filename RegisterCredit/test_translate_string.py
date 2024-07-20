import sys
import pandas as pd
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QFont

def check_time_conflict(df):
    conflicts = []
    for day in df['THứ'].unique():
        day_courses = df[df['THứ'] == day].sort_values('Từ tiết')
        for i, row in day_courses.iterrows():
            # Skip courses with invalid time slots (end time 0)
            if row['Đến tiết'] == 0:
                continue
            
            overlapping_courses = day_courses[
                (day_courses['Từ tiết'] < row['Đến tiết']) & 
                (day_courses['Đến tiết'] > row['Từ tiết']) &
                (day_courses['Đến tiết'] != 0) &  # Exclude courses with end time 0
                (day_courses.index > i)  # Only check conflicts with courses that come later in the list
            ]
            
            for _, other_row in overlapping_courses.iterrows():
                conflicts.append((row['Tên LHP'].strip(), other_row['Tên LHP'].strip(), int(day), 
                                  f"Từ tiết {int(row['Từ tiết'])} đến tiết {int(row['Đến tiết'])}",
                                  f"Từ tiết {int(other_row['Từ tiết'])} đến tiết {int(other_row['Đến tiết'])}"))
    
    return conflicts

def process_excel_data(file_path, code_file_path):
    # Read the main Excel file
    df = pd.read_excel(file_path)
    
    # Read the code Excel file
    df_code = pd.read_excel(code_file_path)
    
    # Strip whitespace from 'Tên LHP' in both dataframes
    df['Tên LHP'] = df['Tên LHP'].str.strip()
    df_code['Tên LHP'] = df_code['Tên LHP'].str.strip()

    # Find LHP names in df_code that are not in df
    missing_lhp = list(set(df_code['Tên LHP']) - set(df['Tên LHP']))

    # Process each row in the main dataframe
    result_parts = []
    existing_lhp = []
    full_lhp = []
    total_credits = 0
    for _, row in df.iterrows():
        ma_hp = str(row['Mã HP'])
        ten_lhp = row['Tên LHP'].strip()
        sldk = row['SLDK']
        da_dk = row['Đã ĐK']
        so_tc = row['Số TC']
        # Check if the LHP name exists in the code file
        if ten_lhp in df_code['Tên LHP'].values:
            existing_lhp.append(ten_lhp)
            total_credits += so_tc
            # Check if the class is full
            if da_dk >= sldk:
                full_lhp.append(f"{ten_lhp} SLDK: {str(sldk).split('.')[0]}, Đã ĐK: {str(da_dk).split('.')[0]}")
            
            # Extract the last two digits from LHP name
            match = re.search(r'\d{2}$', ten_lhp)
            if match:
                last_two_digits = match.group()
                
                # Create the new code format without decimal part
                new_code = f"124{ma_hp.split('.')[0]}{last_two_digits}"  # Remove decimal part
                result_parts.append(new_code)
    
    # Filter the main dataframe to only include existing LHP
    df_filtered = df[df['Tên LHP'].isin(df_code['Tên LHP'])].copy()
    
    # Convert 'THứ', 'Từ tiết', 'Đến tiết' to numeric, replacing NaN with 0
    df_filtered['THứ'] = pd.to_numeric(df_filtered['THứ'], errors='coerce').fillna(0).astype(int)
    df_filtered['Từ tiết'] = pd.to_numeric(df_filtered['Từ tiết'], errors='coerce').fillna(0).astype(int)
    df_filtered['Đến tiết'] = pd.to_numeric(df_filtered['Đến tiết'], errors='coerce').fillna(0).astype(int)
    
    # Check for time conflicts
    conflicts = check_time_conflict(df_filtered)
   
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
        password = str(password).split('.')[0]
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
    
    return registration_js, login_js, len(existing_lhp), existing_lhp, full_lhp, conflicts, total_credits, missing_lhp

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Excel Processing Application'
        self.left = 100
        self.top = 50
        self.width = 800
        self.height = 1000  # Increased height to accommodate new text box
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QVBoxLayout()
        
        self.btn = QPushButton('Chọn file code', self)
        self.btn.clicked.connect(self.chooseFile)
        layout.addWidget(self.btn)
        
        large_font = QFont()
        large_font.setPointSize(14)  # You can adjust this value to make it larger or smaller
        large_font.setBold(True)
        
        self.lhp_count_label = QLabel('SỐ LƯỢNG LHP: ', self)
        self.lhp_count_label.setFont(large_font)
        layout.addWidget(self.lhp_count_label)
        
        self.total_credits_label = QLabel('TỔNG SỐ TÍN CHỈ: ', self)
        self.total_credits_label.setFont(large_font)
        layout.addWidget(self.total_credits_label)
        
        # self.lhp_list_text = QTextEdit(self)
        # self.lhp_list_text.setReadOnly(True)
        # layout.addWidget(self.lhp_list_text)
        
         # Tạo layout ngang cho "Các LHP đã đầy" và "Các LHP trong file code không có trong file chính"
        horizontal_layout = QHBoxLayout()
        
        # Phần "Các LHP đã đầy"
        full_lhp_layout = QVBoxLayout()
        self.full_lhp_label = QLabel('CÁC LHP ĐÃ FULL:', self)
        full_lhp_layout.addWidget(self.full_lhp_label)
        self.full_lhp_text = QTextEdit(self)
        self.full_lhp_text.setReadOnly(True)
        full_lhp_layout.addWidget(self.full_lhp_text)
        horizontal_layout.addLayout(full_lhp_layout)
        
        # Phần "Các LHP trong file code không có trong file chính"
        missing_lhp_layout = QVBoxLayout()
        self.missing_lhp_label = QLabel('Các LHP CHƯA ĐÚNG TÊN LHP:', self)
        missing_lhp_layout.addWidget(self.missing_lhp_label)
        self.missing_lhp_text = QTextEdit(self)
        self.missing_lhp_text.setReadOnly(True)
        missing_lhp_layout.addWidget(self.missing_lhp_text)
        horizontal_layout.addLayout(missing_lhp_layout)
        
        layout.addLayout(horizontal_layout)
        
        self.conflicts_label = QLabel('Các LHP bị trùng lịch:', self)
        layout.addWidget(self.conflicts_label)
        
        self.conflicts_text = QTextEdit(self)
        self.conflicts_text.setReadOnly(True)
        layout.addWidget(self.conflicts_text)
        
        # self.missing_lhp_label = QLabel('Các LHP trong file code không có trong file chính:', self)
        # layout.addWidget(self.missing_lhp_label)
        
        # self.missing_lhp_text = QTextEdit(self)
        # self.missing_lhp_text.setReadOnly(True)
        # layout.addWidget(self.missing_lhp_text)
        
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
                main_file_path = "D:\DaiHoc\HK223_2023_2024\ChuyenDeNNLT\python_course_223\RegisterCredit\danhsach.xlsx"
                registration_result, login_result, lhp_count, existing_lhp, full_lhp, conflicts, total_credits, missing_lhp = process_excel_data(main_file_path, file_path)
                self.registration_text.setPlainText(registration_result)
                self.login_text.setPlainText(login_result)
                self.lhp_count_label.setText(f'SỐ LƯỢNG LHP: {str(lhp_count).split(".")[0]}')
                self.total_credits_label.setText(f'Tổng số tín chỉ: {str(total_credits).split(".")[0]}')
                # self.lhp_list_text.setPlainText('\n'.join(existing_lhp))
                self.full_lhp_text.setPlainText('\n'.join(full_lhp))
                self.conflicts_text.setPlainText('\n'.join([f"{c[0]} và {c[1]} trùng lịch vào Thứ {c[2]}, {c[3]} và {c[4]}" for c in conflicts]))
                self.missing_lhp_text.setPlainText('\n'.join(missing_lhp))
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi xử lý file: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())