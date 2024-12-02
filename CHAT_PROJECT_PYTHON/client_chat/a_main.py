import sys
import os
import random
import client

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLabel, QMainWindow, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

#--------------------------------------------------------------------------------------------------------------

# rounded corner layout
# def create_stylesheet():
#     return """
#     QMainWindow {
#         background-color: #2b2b2b; /* Dark theme */
#         border-radius: 15px;
#     }
#     QPushButton#navButton {
#         background-color: #444444;
#         color: white;
#         font-size: 14px;
#         border: none;
#         padding: 10px 15px;
#         border-radius: 10px;
#     }
#     QPushButton#navButton:hover {
#         background-color: #555555;
#     }
#     QLabel {
#         color: white;
#         font-size: 14px;
#     }
#     QTextEdit#middleArea {
#         background: #3e3e3e;
#         color: white;
#         font-size: 16px;
#         font-weight: bold;
#         border-radius: 15px;
#         padding: 10px;
#     }
#     QWidget#centralWidget {
#         background: #2e2e2e;
#         border-radius: 15px;
#     }
#     """

def create_stylesheet():
    return """
    QMainWindow {
        background-color: #000000; /* Complete black */
        border: none;
    }
    QPushButton#navButton {
        background-color: #1a1a1a; /* Slightly lighter black for contrast */
        color: white;
        font-size: 14px;
        border: 1px solid #333333; /* Subtle border for buttons */
        padding: 10px 15px;
    }
    QPushButton#navButton:hover {
        background-color: #333333; /* Highlight effect */
    }
    QLabel {
        color: white;
        font-size: 14px;
    }
    QTextEdit#middleArea {
        background: #111111; /* Dark text area */
        color: white;
        font-size: 16px;
        font-weight: bold;
        border: 1px solid #444444; /* Border for text area */
        padding: 10px;
    }
    QWidget#centralWidget {
        background: #000000; /* Consistent black for central widget */
    }
    QTextEdit#textInput {
        background: #111111; /* Black theme for input box */
        color: white;
        font-size: 14px;
        border: 1px solid #444444; /* Subtle border */
        padding: 5px;
    }
    """

def apply_dark_palette(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(43, 43, 43))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(43, 43, 43))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(43, 43, 43))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(50, 50, 50))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)

#--------------------------------------------------------------------------------------------------------------

# Function to highlight the clicked button
current_button = None  # To keep track of the currently highlighted button

def highlight_button(button):
    global current_button
    
    # Reset style of the previously active button
    if current_button:
        current_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;    /* Default dark color */
                color: white;
                font-size: 14px;
                border: 1px solid #333333;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
    
    # Set the active button's style
    button.setStyleSheet("""
        QPushButton {
            background-color: #2E004F;    /* Highlighted color */
            color: white;
            font-size: 14px;
            border: 1px solid #003377;
            padding: 10px;
        }
    """)
    
    # Update the current_button to the newly clicked button
    current_button = button

#--------------------------------------------------------------------------------------------------------------

def setup_ui(main_window, sender):
    main_window.setWindowTitle("ήλιος user : "+"<"+sender+">")#sun, meaning of it
    main_window.setGeometry(100, 100, 800, 600)
    main_window.setStyleSheet(create_stylesheet())
    main_window.setFixedSize(800, 600)
    
    # Central widget and layout
    central_widget = QWidget(main_window)
    central_widget.setObjectName("centralWidget")
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)

    # Top Bar
    top_bar = QHBoxLayout()
    top_bar.setContentsMargins(10, 10, 10, 10)
    top_bar.setSpacing(10)
    
    # Generate buttons dynamically for top bar
    user_list = client.user_list()
    for username in user_list:
        if username == sender:
            continue
        btn = QPushButton(username)
        btn.setObjectName("navButton")
        # Use the button's text dynamically in the lambda
        btn.clicked.connect(lambda checked, button=btn: highlight_button(button))
        btn.clicked.connect(lambda checked, display_new_content='', button=btn, sender=sender: 
            open_file(display_new_content, button.text(), sender, middle_area))
        btn.clicked.connect(lambda checked, button=btn : current_reciever(sender, text_input, button.text()))
        top_bar.addWidget(btn)
    
    # Middle Designer Area (Chat Window)
    global middle_area  # Make middle_area accessible
    middle_area = QTextEdit()
    middle_area.setReadOnly(True)  # Make it read-only
    middle_area.setObjectName("middleArea")
    middle_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Enable vertical scroll bar

    # Bottom Bar (Text Input Area + Submit Button)
    bottom_bar = QHBoxLayout()
    bottom_bar.setContentsMargins(10, 10, 10, 10)
    bottom_bar.setSpacing(10)

    # Text Area for Typing Input
    text_input = QTextEdit()
    text_input.setObjectName("textInput")
    text_input.setPlaceholderText("Type your message here...")
    text_input.setFixedHeight(40)
    
    # Submit Button
    submit_btn = QPushButton("Submit")
    submit_btn.setObjectName("navButton")
    submit_btn.clicked.connect(lambda checked, sender=sender : current_reciever(sender, text_input))
    
    # Add to bottom bar
    bottom_bar.addWidget(text_input)
    bottom_bar.addWidget(submit_btn)

    # Add components to main layout
    main_layout.addLayout(top_bar)
    main_layout.addWidget(middle_area)
    main_layout.addLayout(bottom_bar)

    main_window.setCentralWidget(central_widget)

#--------------------------------------------------------------------------------------------------------------

global_rec = ''
def current_reciever(sender, text_input=None, reciever=None):
    global global_rec
    if reciever is None:
        submit_message(text_input, global_rec, sender)
    if reciever is not None:
        global_rec = reciever
    # print("Current receiver is:", global_rec)
    return global_rec

#--------------------------------------------------------------------------------------------------------------

def open_file(display_new_content, reciever, sender, middle_area):
    # print("\n open_file function working here rec and send = ",reciever," and ",sender,"\n")
    if display_new_content != '':
        content = display_new_content
    else:
        content = client.file_data(reciever, sender, '')
    if content:
        formatted_content = format_chat(content, reciever, sender)
        middle_area.setHtml(formatted_content)
        middle_area.verticalScrollBar().setValue(middle_area.verticalScrollBar().maximum())# Auto-scroll to bottom
    else:
        middle_area.setHtml("<i>No content found.</i>")

#--------------------------------------------------------------------------------------------------------------

# Function to process the input when submit button is clicked
def submit_message(text_input, reciever, sender):
    # print(" \n submit_message function working here rec and send = ",reciever," and ",sender,"\n")
    message = text_input.toPlainText()
    display_new_content = client.file_data(reciever, sender, message)
    open_file(display_new_content, reciever, sender, middle_area)
    # Auto-scroll to bottom    
    middle_area.verticalScrollBar().setValue(middle_area.verticalScrollBar().maximum())
    # Clear the text input area after submission
    text_input.clear()

#--------------------------------------------------------------------------------------------------------------

# Format content as chat
def format_chat(content, reciever, sender):
    # print("\n format_chat function working here rec and send = ",reciever," and ",sender,"\n")
    formatted_content = ""
    
    start1 = len(reciever+'@$#: ')
    start2 = len(sender+'@$#: ')
    for line in content.splitlines():
        # other
        if line.startswith(reciever+'@$#: '):
            # Received message (left-aligned)
            formatted_content += f'<p style="text-align: left; color: lightblue;">{line[start1:]}</p>'
        # you
        elif line.startswith(sender+'@$#: '):
            # Sent message (right-aligned)
            formatted_content += f'<p style="text-align: right; color: lightgreen;">{line[start2:]}</p>'
        else:
            # Sent message (right-aligned)
            formatted_content += f'<p style="text-align: right; color: lightgreen;">{line[0:]}</p>'
    return formatted_content

#--------------------------------------------------------------------------------------------------------------

def main(sender):
    
    # print(" mian frame called in main file ")
    
    app = QApplication(sys.argv)
    apply_dark_palette(app)

    main_window = QMainWindow()
    setup_ui(main_window, sender)

    main_window.show()
    sys.exit(app.exec_())
    
main(client.get_god_user())  # Retrieve the value      