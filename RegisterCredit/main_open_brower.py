import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from operagxdriver import start_opera_driver

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SeleniumWorker(QThread):
    finished = pyqtSignal(bool)
    error = pyqtSignal(str, bool)

    def __init__(self, username, password, script1, script2, browser_type, incognito=False, opera_path=None):
        super().__init__()
        self.username = username
        self.password = password
        self.script1 = script1
        self.script2 = script2
        self.browser_type = browser_type
        self.incognito = incognito
        self.opera_path = opera_path

    def run(self):
        try:
            self.run_selenium_script()
            self.finished.emit(not self.incognito)
        except Exception as e:
            self.error.emit(str(e), not self.incognito)

    def run_selenium_script(self):
        def init_driver(url):
            if self.browser_type == "chrome":
                options = webdriver.ChromeOptions()
                if self.incognito:
                    options.add_argument("--incognito")
                driver = webdriver.Chrome(resource_path("drivers/chromedriver.exe"), options=options)
            elif self.browser_type == "edge":
                options = EdgeOptions()
                options.use_chromium = True
                if self.incognito:
                    options.add_argument("inprivate")
                driver = Edge(executable_path=resource_path("drivers/msedgedriver.exe"), options=options)
            elif self.browser_type == "firefox":
                options = FirefoxOptions()
                if self.incognito:
                    options.add_argument("-private")
                driver = webdriver.Firefox(executable_path=resource_path("drivers/geckodriver.exe"), options=options)
            else:  # Opera GX
                if not self.opera_path:
                    raise ValueError("Opera browser path not specified")
                arguments = (
                    "--no-sandbox",
                    "--test-type",
                    "--no-default-browser-check",
                    "--no-first-run",
                    "--start-maximized",
                )
                if self.incognito:
                    arguments += ("--incognito",)
                driver = start_opera_driver(
                    opera_browser_exe=self.opera_path,
                    opera_driver_exe=resource_path("drivers/operadriver.exe"),
                    arguments=arguments
                )

            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(('tag name', 'body')))
            return driver

        def execute_script_in_tab(driver, script):
            driver.execute_script(script)

        url = 'http://daotao.ute.udn.vn/'
        driver = init_driver(url)
        
        execute_script_in_tab(driver, self.script1)
        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        
        execute_script_in_tab(driver, self.script2)
        
        import time
        time.sleep(3600)
        
        driver.quit()

class SeleniumGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Selenium Script Runner')
        self.setGeometry(100, 100, 1000, 800)

        main_layout = QVBoxLayout()

        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Excel File')
        self.load_button.clicked.connect(self.load_excel)
        button_layout.addWidget(self.load_button)

        self.run_chrome_button = QPushButton('Run Chrome')
        self.run_chrome_button.clicked.connect(lambda: self.run_script("chrome", False))
        button_layout.addWidget(self.run_chrome_button)

        self.run_chrome_incognito_button = QPushButton('Run Chrome Incognito')
        self.run_chrome_incognito_button.clicked.connect(lambda: self.run_script("chrome", True))
        button_layout.addWidget(self.run_chrome_incognito_button)

        self.run_edge_button = QPushButton('Run Edge')
        self.run_edge_button.clicked.connect(lambda: self.run_script("edge", False))
        button_layout.addWidget(self.run_edge_button)

        self.run_edge_incognito_button = QPushButton('Run Edge Incognito')
        self.run_edge_incognito_button.clicked.connect(lambda: self.run_script("edge", True))
        button_layout.addWidget(self.run_edge_incognito_button)

        self.run_firefox_button = QPushButton('Run Firefox')
        self.run_firefox_button.clicked.connect(lambda: self.run_script("firefox", False))
        button_layout.addWidget(self.run_firefox_button)

        self.run_firefox_private_button = QPushButton('Run Firefox Private')
        self.run_firefox_private_button.clicked.connect(lambda: self.run_script("firefox", True))
        button_layout.addWidget(self.run_firefox_private_button)

        self.run_opera_button = QPushButton('Run Opera')
        self.run_opera_button.clicked.connect(lambda: self.run_script("opera", False))
        button_layout.addWidget(self.run_opera_button)

        self.run_opera_incognito_button = QPushButton('Run Opera Incognito')
        self.run_opera_incognito_button.clicked.connect(lambda: self.run_script("opera", True))
        button_layout.addWidget(self.run_opera_incognito_button)

        main_layout.addLayout(button_layout)

        # Add Opera path input
        opera_layout = QHBoxLayout()
        self.opera_path_label = QLabel("Opera Path:")
        self.opera_path_input = QLineEdit()
        self.opera_path_button = QPushButton("Browse")
        self.opera_path_button.clicked.connect(self.browse_opera_path)
        opera_layout.addWidget(self.opera_path_label)
        opera_layout.addWidget(self.opera_path_input)
        opera_layout.addWidget(self.opera_path_button)
        main_layout.addLayout(opera_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.df = None
        self.worker = None

    def load_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Excel File', '', 'Excel Files (*.xlsx *.xls)')
        if file_name:
            self.df = pd.read_excel(file_name)
            self.display_table()

    def display_table(self):
        self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

        self.table.resizeColumnsToContents()

    def browse_opera_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Opera Executable', '', 'Executable Files (*.exe)')
        if file_name:
            self.opera_path_input.setText(file_name)

    def run_script(self, browser_type, incognito=False):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'No row selected')
            return

        row = selected_rows[0].row()
        username = self.df.iloc[row]['username']
        password = self.df.iloc[row]['password']
        script1 = self.df.iloc[row]['script1']
        script2 = self.df.iloc[row]['script2']

        opera_path = self.opera_path_input.text() if browser_type == "opera" else None
        
        if browser_type == "opera" and not opera_path:
            QMessageBox.warning(self, 'Warning', 'Please specify Opera browser path')
            return

        self.worker = SeleniumWorker(username, password, script1, script2, browser_type, incognito, opera_path)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.error.connect(self.on_worker_error)
        self.worker.start()

    def on_worker_finished(self, is_normal):
        QMessageBox.information(self, 'Success', 'Script execution completed.')

    def on_worker_error(self, error_message, is_normal):
        QMessageBox.critical(self, 'Error', f'An error occurred: {error_message}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SeleniumGUI()
    window.show()
    sys.exit(app.exec_())