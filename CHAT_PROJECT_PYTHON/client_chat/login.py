import sys
import time
import client

#--------------------------------------------------------------------------------------------------------------

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt

#--------------------------------------------------------------------------------------------------------------

status = ''

#--------------------------------------------------------------------------------------------------------------

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login Window')
        
        # Set window size and make it bigger
        self.setFixedSize(400, 300)  # Set a larger fixed size for the window
        
        # Apply rounded corners
        self.setStyleSheet("""
            QWidget {
                background-color: #1f1f1f;
                color: white;
                border-radius: 15px;
                padding: 20px;
            }
            QPushButton {
                background-color: #444444;
                border: 1px solid #444444;
                border-radius: 10px;
                padding: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QLineEdit {
                background-color: #444444;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
                color: white;
            }
            QLabel {
                font-size: 28px;  /* Increased size for Hello */
                font-weight: bold;
                color: #f0f0f0;
            }
        """)

        # Set up main layout
        main_layout = QVBoxLayout()

        # Top layout (buttons area)
        top_layout = QHBoxLayout()

        # Button 1
        self.button1 = QPushButton(' LOGIN ', self)
        self.button1.setStyleSheet("background-color: #444444;")
        self.button1.clicked.connect(self.on_button1_click)
        top_layout.addWidget(self.button1)

        # Button 2
        self.button2 = QPushButton(' SIGNUP ', self)
        self.button2.setStyleSheet("background-color: #444444;")
        self.button2.clicked.connect(self.on_button2_click)
        top_layout.addWidget(self.button2)

        main_layout.addLayout(top_layout)

        # Middle area (hello message and text fields)
        self.middle_area = QVBoxLayout()
        self.label = QLabel("  Hello  ", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.middle_area.addWidget(self.label)

        # Text fields (initially hidden)
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        self.username_field.setVisible(False)  # Hide initially
        self.middle_area.addWidget(self.username_field)

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setVisible(False)  # Hide initially
        self.middle_area.addWidget(self.password_field)

        main_layout.addLayout(self.middle_area)

        # Bottom layout (submit button)
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setStyleSheet("background-color: #555555;")
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setVisible(False)  # Hide initially
        main_layout.addWidget(self.submit_button)

        # Set main layout
        self.setLayout(main_layout)

    def on_button1_click(self):
        global status
        status = 'login'
        # print(status)
        # Highlight the clicked button and reset the other
        self.button1.setStyleSheet("background-color: #2E004F;")
        self.button2.setStyleSheet("background-color: #444444;")
        self.label.setText(" LOGIN ")
        self.username_field.setVisible(True)  # Show username field
        self.password_field.setVisible(True)  # Show password field
        self.submit_button.setVisible(True)  # Show submit button
        self.username_field.clear()
        self.password_field.clear()

    def on_button2_click(self):
        global status
        status = 'signup'
        # print(status)
        # Highlight the clicked button and reset the other
        self.button2.setStyleSheet("background-color: #2E004F;")
        self.button1.setStyleSheet("background-color: #444444;")
        self.label.setText(" SIGNUP ")
        self.username_field.setVisible(True)  # Show username field
        self.password_field.setVisible(True)  # Show password field
        self.submit_button.setVisible(True)  # Show submit button
        self.username_field.clear()
        self.password_field.clear()

    def on_submit(self):
        username = self.username_field.text()
        password = self.password_field.text()
        self.username_field.clear()
        self.password_field.clear()

        # print(username, password)
        result = client.credentials(username, password, status)
        if result == True:
            # print(f"Submitted: Username: {username}, Password: {password}")
            self.close()  # Close window when correct credentials are entered
        else:
            # print("Invalid credentials!")
            QMessageBox.critical(None, "Error", "Invalid Credentials!")
            
#--------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
    # time.sleep(1)  # Pauses execution for 1 second
    
#--------------------------------------------------------------------------------------------------------------
