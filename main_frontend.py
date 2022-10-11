from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QSpacerItem, QSizePolicy
from backend import app_database

__version__ = "0.1"

class car_rental_app(app_database):
    def start_up(self, car_rental_mainwindow):
        car_rental_mainwindow.setFixedSize(961, 709)
        self.main_widget = QtWidgets.QWidget(car_rental_mainwindow)
        car_rental_mainwindow.setWindowTitle("Car Rentals")
        self.main_program_frame = QtWidgets.QFrame(self.main_widget)
        self.main_program_frame.setGeometry(QtCore.QRect(0, 0, 961, 71))
        self.main_program_frame.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.main_program_title = QtWidgets.QLabel(self.main_program_frame)
        self.main_program_title.setGeometry(QtCore.QRect(30, 10, 271, 51))
        self.main_program_title.setStyleSheet("font: 25 18pt \"Segoe UI\";")
        self.load_screen1()
        self.load_screen2()
        self.load_screen3()

    def load_screen1(self):
        self.main_login_frame = QtWidgets.QFrame(self.main_widget)
        self.main_login_frame.setEnabled(True)
        self.main_login_frame.setGeometry(QtCore.QRect(0, 70, 961, 641))

        self.main_page_admin_login = QtWidgets.QPushButton(self.main_login_frame)
        self.main_page_admin_login.setGeometry(QtCore.QRect(20, 590, 75, 23))

        self.main_page_login_label = QtWidgets.QLabel(self.main_login_frame)
        self.main_page_login_label.setGeometry(QtCore.QRect(20, 20, 231, 31))
        self.main_page_login_label.setStyleSheet("font: 25 15pt \"Segoe UI\";")
        self.requested_car_rentals_frame = QtWidgets.QFrame(self.main_login_frame)
        self.requested_car_rentals_frame.setGeometry(QtCore.QRect(390, 10, 561, 621))

        self.requested_car_rentals_refresh_btn = QtWidgets.QPushButton(self.requested_car_rentals_frame)
        self.requested_car_rentals_refresh_btn.setObjectName(u"requested_car_rentals_refresh_btn")
        self.requested_car_rentals_refresh_btn.setGeometry(QtCore.QRect(450, 10, 91, 23))
        self.requested_car_rentals_refresh_btn.setText("Delete All")
        self.requested_car_rentals_refresh_btn.clicked.connect(self.delete_all_requests)

        self.title_label_requeste_car_rentals = QtWidgets.QLabel(self.requested_car_rentals_frame)
        self.title_label_requeste_car_rentals.setGeometry(QtCore.QRect(10, 0, 211, 41))
        self.title_label_requeste_car_rentals.setStyleSheet("font: 25 15pt \"Segoe UI\";")

        self.requested_cars_scroll = QtWidgets.QScrollArea(self.requested_car_rentals_frame)
        self.requested_cars_scroll.setGeometry(QtCore.QRect(0, 50, 551, 561))
        self.requested_cars_scroll.setMinimumSize(QtCore.QSize(500, 530))
        self.requested_cars_scroll.setMaximumSize(QtCore.QSize(600, 600))
        self.requested_cars_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.requested_cars_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.requested_cars_scroll.setWidgetResizable(True)
        self.requested_cars_scroll_content = QtWidgets.QWidget()
        self.requested_cars_scroll_content.setGeometry(QtCore.QRect(0, 0, 538, 588))
        self.verticalLayout_screen1 = QtWidgets.QVBoxLayout(self.requested_cars_scroll_content)
        self.verticalSpacer_screen1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.load_rentals_from_database_screen1()
        self.verticalLayout_screen1.addItem(self.verticalSpacer_screen1)
        self.create_normal_user_screen1()
        self.login_form_normal_screen1()
        self.get_admin_data_all()
        self.admin_login_screen1()
        self.main_page_admin_login.clicked.connect(self.user_login_form_admin.show)
        self.user_login_form_admin.hide()

        self.load_text_rental_screen1()
        QtCore.QMetaObject.connectSlotsByName(car_rental_mainwindow)
    
    def delete_all_requests(self):
        self.conn.execute("DELETE FROM CAR_RENTAL_DATA")
        self.reload_rentals_from_database_screen1()

    def user_login_operation_screen1(self):
        email = self.login_username_email.text()
        password = self.login_username_password.text()
        response = self.get_user_data(email, password)
        response_list = []
        for i in response:
            response_list.append(i)
        if response == "Failed to Get User Data":
            self.error_user_login_label.setText('User not found')
        elif response_list != []:
            self.error_user_login_label.setText("Logged in")
            self.main_login_frame.hide()
            # So new added cars must become visible when logging in again
            self.reload_cars_from_database_screen3()
            self.main_book_rental_frame.show()
            self.current_user = response_list[0][0]
        else:
            self.error_label.setText("Log-in Failed")

    def admin_login_operation_screen1(self):
        email = self.admin_input_email.text()
        password = self.admin_input_password.text()
        response = self.get_admin_data(email, password)
        if response == []:
            self.error_label.setText('User not found')
        elif response != []:
            self.error_label.setText("Logged in")
            self.main_login_frame.hide()
            self.admin_page_main_frame.show()
        else:
            self.error_label.setText("Log-in Failed")

    def create_user_in_database_operation_screen1(self):
        self.create_username_label.setText("User Name")
        try:
            total = self.get_user_data_all()
            list_id = []
            for ID in total:
                list_id.append(int(ID[0]))
            user_id = list_id[-1] + 1
        except Exception:
            user_id = 1
        user_name = self.input_create_username.text()
        email = self.input_create_username_email.text()
        password = self.input_create_username_password.text()
        if user_name:
            if email:
                if password:
                    self.error_label.setText("")
                    self.add_new_user(id=user_id, user_name=user_name, user_pass=password, user_email=email)
                    self.error_user_login_label.setText(f'User created {user_name}')

    def switch_user_creation_form_to_admin_screen1(self):
        self.create_username_label.setText("Admin User")
        self.create_username_add_user_button.setEnabled(True)
        try:
            self.create_username_add_user_button.clicked.disconnect()
        except Exception:
            pass
        self.create_username_add_user_button.clicked.connect(self.create_admin_in_database_operation_screen1)

    def switch_user_creation_form_to_user_screen1(self):
        self.create_username_label.setText("User Name")
        self.create_username_add_user_button.setEnabled(True)
        try:
            self.create_username_add_user_button.clicked.disconnect()
        except Exception:
            pass
        self.create_username_add_user_button.clicked.connect(self.create_user_in_database_operation_screen1)

    def create_admin_in_database_operation_screen1(self):
        try:
            total = self.get_admin_data_all()
            list_id = []
            for ID in total:
                list_id.append(int(ID[0]))
            user_id = list_id[-1] + 1
        except Exception:
            user_id = 1
        user_name = self.input_create_username.text()
        email = self.input_create_username_email.text()
        password = self.input_create_username_password.text()
        if user_name:
            if email:
                if password:
                    self.error_user_login_label.setText('')
                    self.add_new_admin(id=user_id, user_name=user_name, user_pass=password, user_email=email)
                    self.error_label.setText(f"Created Admin User {user_name}")

    def load_rentals_from_database_screen1(self):
        try:
            rental_requests = self.get_all_rentals()
            #(rental_requests)
            for rental in rental_requests:
                rented_car_name = rental[1]
                rented_by_who = rental[3]
                rented_car_image = self.get_car_image(rented_car_name, save_name=None)
                self.request_rentals_cards_screen1(rented_by_who, rented_car_name, rented_car_image)
        except Exception:
            pass
    
    def reload_rentals_from_database_screen1(self):
        self.verticalLayout_screen1.removeItem(self.verticalSpacer_screen1)
        for i in reversed(range(self.verticalLayout_screen1.count())):
            widgetToRemove = self.verticalLayout_screen1.itemAt(i).widget()
            self.verticalLayout_screen1.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        self.load_rentals_from_database_screen1()
        self.verticalLayout_screen1.addItem(self.verticalSpacer_screen1)

    def request_rentals_cards_screen1(self, rented_by_who, rented_car_name, rented_car_image):
        self.reqested_rentals_data_frame = QtWidgets.QFrame(self.requested_cars_scroll_content)
        self.reqested_rentals_data_frame.setMinimumSize(QtCore.QSize(520, 90))
        self.reqested_rentals_data_frame.setMaximumSize(QtCore.QSize(520, 90))

        self.car_bit_map_frame = QtWidgets.QFrame(self.reqested_rentals_data_frame)
        self.car_bit_map_frame.setGeometry(QtCore.QRect(0, 0, 131, 90))
        self.car_bit_map_frame.setMinimumSize(QtCore.QSize(131, 90))
        self.car_bit_map_frame.setMaximumSize(QtCore.QSize(131, 90))

        self.car_image_2 = QtWidgets.QLabel(self.car_bit_map_frame)
        self.car_image_2.setGeometry(QtCore.QRect(0, 2, 131, 91))
        try:
            self.car_image_2.setPixmap(self.load_bytes_image(rented_car_image).scaledToWidth(140))
        except Exception:
            self.car_image_2.setText("No image")
        self.car_data_container_screen1 = QtWidgets.QFrame(self.reqested_rentals_data_frame)
        self.car_data_container_screen1.setGeometry(QtCore.QRect(130, 0, 360, 90))
        self.car_data_container_screen1.setMinimumSize(QtCore.QSize(360, 90))
        self.car_data_container_screen1.setMaximumSize(QtCore.QSize(360, 90))
        self.car_data_container_screen1.setStyleSheet("background-color: rgb(255, 200, 138);")

        self.rent_request_car_title = QtWidgets.QLabel(self.car_data_container_screen1)
        self.rent_request_car_title.setGeometry(QtCore.QRect(20, 20, 200, 21))
        self.rent_request_car_title.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.rent_request_car_title.setText(f" User {rented_by_who} request for {rented_car_name}")
        self.rent_request_meta_data = QtWidgets.QLabel(self.car_data_container_screen1)
        self.rent_request_meta_data.setGeometry(QtCore.QRect(20, 40, 300, 41))
        self.rent_request_meta_data.setText(f"Booking of this car will be processed shortly")
        self.verticalLayout_screen1.addWidget(self.reqested_rentals_data_frame)
        self.requested_cars_scroll.setWidget(self.requested_cars_scroll_content)

    def create_normal_user_screen1(self):
        self.create_user_frame = QtWidgets.QFrame(self.main_login_frame)
        self.create_user_frame.setEnabled(True)
        self.create_user_frame.setGeometry(QtCore.QRect(20, 240, 261, 131))

        self.create_username_add_user_button = QtWidgets.QPushButton(self.create_user_frame)
        self.create_username_add_user_button.setGeometry(QtCore.QRect(110, 100, 141, 23))
        self.create_username_add_user_button.setObjectName("create_username_add_user_button")
        self.create_username_add_user_button.setEnabled(False)

        self.input_create_username_email = QtWidgets.QLineEdit(self.create_user_frame)
        self.input_create_username_email.setGeometry(QtCore.QRect(110, 70, 141, 20))

        self.input_create_username_password = QtWidgets.QLineEdit(self.create_user_frame)
        self.input_create_username_password.setGeometry(QtCore.QRect(110, 40, 141, 20))
        self.input_create_username_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.input_create_username = QtWidgets.QLineEdit(self.create_user_frame)
        self.input_create_username.setGeometry(QtCore.QRect(110, 10, 141, 21))

        self.create_username_label = QtWidgets.QLabel(self.create_user_frame)
        self.create_username_label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.create_username_label.setStyleSheet("font: 25 12pt \"Segoe UI\";")

        self.create_username_password = QtWidgets.QLabel(self.create_user_frame)
        self.create_username_password.setGeometry(QtCore.QRect(10, 40, 81, 21))
        self.create_username_password.setStyleSheet("font: 25 12pt \"Segoe UI\";")

        self.create_username_email = QtWidgets.QLabel(self.create_user_frame)
        self.create_username_email.setGeometry(QtCore.QRect(10, 70, 81, 21))
        self.create_username_email.setStyleSheet("font: 25 12pt \"Segoe UI\";")

    def login_form_normal_screen1(self):
        self.user_login_form_normal = QtWidgets.QFrame(self.main_login_frame)
        self.user_login_form_normal.setGeometry(QtCore.QRect(20, 80, 261, 141))

        self.error_user_login_label = QtWidgets.QLabel(self.user_login_form_normal)
        self.error_user_login_label.setGeometry(QtCore.QRect(10, 110, 241, 20))
        self.error_user_login_label.setStyleSheet("color: rgb(255, 0, 0);")

        self.login_button_normal = QtWidgets.QPushButton(self.user_login_form_normal)
        self.login_button_normal.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.login_button_normal.clicked.connect(self.user_login_operation_screen1)

        self.user_button_createuser = QtWidgets.QPushButton(self.user_login_form_normal)
        self.user_button_createuser.setGeometry(QtCore.QRect(100, 80, 151, 23))
        self.user_button_createuser.clicked.connect(self.switch_user_creation_form_to_user_screen1)

        self.user_password_label = QtWidgets.QLabel(self.user_login_form_normal)
        self.user_password_label.setGeometry(QtCore.QRect(10, 40, 91, 31))
        self.user_password_label.setStyleSheet("font: 25 12pt \"Segoe UI\";")

        self.user_email_label = QtWidgets.QLabel(self.user_login_form_normal)
        self.user_email_label.setGeometry(QtCore.QRect(10, 10, 61, 31))
        self.user_email_label.setStyleSheet("font: 25 12pt \"Segoe UI\";")

        self.login_username_password = QtWidgets.QLineEdit(self.user_login_form_normal)
        self.login_username_password.setGeometry(QtCore.QRect(100, 50, 151, 21))
        self.login_username_password.setMaxLength(100)
        self.login_username_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_username_email = QtWidgets.QLineEdit(self.user_login_form_normal)
        self.login_username_email.setGeometry(QtCore.QRect(100, 20, 151, 21))

    def admin_login_screen1(self):
        self.user_login_form_admin = QtWidgets.QFrame(self.main_login_frame)
        self.user_login_form_admin.setGeometry(QtCore.QRect(20, 390, 261, 141))

        self.error_label = QtWidgets.QLabel(self.user_login_form_admin)
        self.error_label.setGeometry(QtCore.QRect(10, 110, 241, 20))
        self.error_label.setStyleSheet("color: rgb(255, 0, 0);")

        self.login_button_admin = QtWidgets.QPushButton(self.user_login_form_admin)
        self.login_button_admin.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.login_button_admin.clicked.connect(self.admin_login_operation_screen1)

        self.create_user_button_admin = QtWidgets.QPushButton(self.user_login_form_admin)
        self.create_user_button_admin.setGeometry(QtCore.QRect(100, 80, 151, 23))
        self.create_user_button_admin.clicked.connect(self.switch_user_creation_form_to_admin_screen1)

        self.admin_password = QtWidgets.QLabel(self.user_login_form_admin)
        self.admin_password.setGeometry(QtCore.QRect(10, 40, 81, 31))
        self.admin_password.setStyleSheet("font: 25 13pt \"Segoe UI\";")

        self.admin_email = QtWidgets.QLabel(self.user_login_form_admin)
        self.admin_email.setGeometry(QtCore.QRect(10, 10, 61, 31))
        self.admin_email.setStyleSheet("font: 25 13pt \"Segoe UI\";")

        self.admin_input_password = QtWidgets.QLineEdit(self.user_login_form_admin)
        self.admin_input_password.setGeometry(QtCore.QRect(100, 50, 151, 21))
        self.admin_input_password.setMaxLength(100)
        self.admin_input_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.admin_input_email = QtWidgets.QLineEdit(self.user_login_form_admin)
        self.admin_input_email.setGeometry(QtCore.QRect(100, 20, 151, 21))
        car_rental_mainwindow.setCentralWidget(self.main_widget)

    def load_text_rental_screen1(self):
        self.main_program_title.setText("CAR RENTAL SERVICE")
        self.login_button_normal.setText("Login")
        self.user_button_createuser.setText("Create User")
        self.user_password_label.setText("Password:")
        self.user_email_label.setText("Email:")
        self.create_username_add_user_button.setText("Create User")
        self.create_username_label.setText("User Name")
        self.create_username_password.setText("Password")
        self.create_username_email.setText("Email")
        self.main_page_admin_login.setText("Admin Login")
        self.main_page_login_label.setText("Please Log in to continue")
        self.title_label_requeste_car_rentals.setText("Requested Car Rentals")
        self.login_button_admin.setText("Login")
        self.create_user_button_admin.setText("Create User")
        self.admin_password.setText("Password:")
        self.admin_email.setText("Email:")


    def load_screen2(self):
        self.admin_page_main_frame = QtWidgets.QFrame(self.main_widget)
        self.admin_page_main_frame.setGeometry(QtCore.QRect(0, 69, 961, 641))
        self.welcome_admin_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.welcome_admin_label.setGeometry(QtCore.QRect(20, 10, 341, 51))
        self.welcome_admin_label.setStyleSheet("font: 25 20pt \"Segoe UI\";")
        self.admin_car_rental_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_rental_label.setGeometry(QtCore.QRect(30, 240, 81, 21))
        self.admin_car_color_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_color_label.setGeometry(QtCore.QRect(30, 150, 71, 21))
        self.admin_car_company_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_company_label.setGeometry(QtCore.QRect(30, 90, 71, 21))
        self.admin_car_number_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_number_label.setGeometry(QtCore.QRect(30, 180, 71, 21))
        self.admin_car_model_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_model_label.setGeometry(QtCore.QRect(30, 120, 71, 21))
        self.admin_car_year_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_year_label.setGeometry(QtCore.QRect(30, 210, 71, 21))
        self.admin_car_company_add = QtWidgets.QLineEdit(self.admin_page_main_frame)
        self.admin_car_company_add.setGeometry(QtCore.QRect(120, 90, 161, 20))
        self.admin_car_color_add = QtWidgets.QLineEdit(self.admin_page_main_frame)
        self.admin_car_color_add.setGeometry(QtCore.QRect(120, 150, 161, 20))
        self.admin_car_rental_price_select = QtWidgets.QSpinBox(self.admin_page_main_frame)
        self.admin_car_rental_price_select.setGeometry(QtCore.QRect(120, 240, 161, 22))
        self.admin_car_rental_price_select.setMaximum(100000)
        self.admin_car_rental_price_select.setSingleStep(50)
        self.admin_car_year_select = QtWidgets.QDateEdit(self.admin_page_main_frame)
        self.admin_car_year_select.setGeometry(QtCore.QRect(120, 210, 161, 22))
        self.admin_car_number_add = QtWidgets.QLineEdit(self.admin_page_main_frame)
        self.admin_car_number_add.setGeometry(QtCore.QRect(120, 180, 161, 20))
        self.admin_car_number_add.setPlaceholderText("")
        self.admin_car_make_add = QtWidgets.QLineEdit(self.admin_page_main_frame)
        self.admin_car_make_add.setGeometry(QtCore.QRect(120, 120, 161, 20))
        self.admin_select_car_image = QtWidgets.QPushButton(self.admin_page_main_frame)
        self.admin_select_car_image.setGeometry(QtCore.QRect(120, 270, 81, 23))
        self.admin_select_car_image.clicked.connect(self.select_image_file_screen2)
        self.admin_car_description = QtWidgets.QTextBrowser(self.admin_page_main_frame)
        self.admin_car_description.setGeometry(QtCore.QRect(120, 300, 161, 51))
        self.admin_car_description.setReadOnly(False)
        self.admin_car_description_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_description_label.setGeometry(QtCore.QRect(30, 300, 71, 21))
        self.admin_add_image_button = QtWidgets.QPushButton(self.admin_page_main_frame)
        self.admin_add_image_button.setGeometry(QtCore.QRect(210, 270, 75, 23))
        self.admin_add_image_button.clicked.connect(self.show_image_preview_screen2)
        self.admin_car_image_label = QtWidgets.QLabel(self.admin_page_main_frame)
        self.admin_car_image_label.setGeometry(QtCore.QRect(30, 270, 71, 21))
        self.add_car_new = QtWidgets.QPushButton(self.admin_page_main_frame)
        self.add_car_new.setGeometry(QtCore.QRect(120, 390, 161, 23))
        self.add_car_new.clicked.connect(self.add_new_car_operation_screen2)
        self.admin_car_scroll = QtWidgets.QScrollArea(self.admin_page_main_frame)
        self.admin_car_scroll.setGeometry(QtCore.QRect(320, 80, 631, 551))
        self.admin_car_scroll.setMinimumSize(QtCore.QSize(621, 511))
        self.admin_car_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.admin_car_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.admin_car_scroll.setWidgetResizable(True)
        self.admin_car_scroll_contents = QtWidgets.QWidget()
        self.admin_car_scroll_contents.setGeometry(QtCore.QRect(0, 0, 612, 549))
        self.verticalLayout_screen2 = QtWidgets.QVBoxLayout(self.admin_car_scroll_contents)
        self.admin_car_scroll.setWidget(self.admin_car_scroll_contents)
        self.preview_image_bitmap = QtWidgets.QLabel(self.admin_page_main_frame)
        self.preview_image_bitmap.setGeometry(QtCore.QRect(20, 430, 281, 191))
        self.preview_image_bitmap.setObjectName("preview_image_bitmap")
        car_rental_mainwindow.setCentralWidget(self.main_widget)
        self.log_out_button_admin = QtWidgets.QPushButton(self.admin_page_main_frame)
        self.log_out_button_admin.setGeometry(QtCore.QRect(870, 30, 75, 23))
        self.log_out_button_admin.setText("Log Out")
        self.log_out_button_admin.clicked.connect(self.logout_admin_screen2)
        self.load_cars_from_database_screen2()
        self.verticalSpacer_screen2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_screen2.addItem(self.verticalSpacer_screen2)
        self.load_text_rental_screen2()
        self.admin_page_main_frame.hide()
        QtCore.QMetaObject.connectSlotsByName(car_rental_mainwindow)
    
    def logout_admin_screen2(self):
        # Disconnecting the buttons
        try:
            self.admin_add_image_button.clicked.disconnect()
            self.add_car_new.clicked.disconnect()
        except Exception:
            pass
        # Empty form fields
        try:
            self.fileName = None
            self.admin_car_company_add.clear()
            self.admin_car_make_add.clear()
            self.admin_car_color_add.clear()
            self.admin_car_number_add.clear()
            self.admin_car_rental_price_select.clear()
            self.admin_car_description.clear()
        except Exception:
            pass
        # Do other stuff
        self.user_login_form_admin.hide()
        self.load_text_rental_screen2()
        self.reload_rentals_from_database_screen1()
        self.admin_page_main_frame.hide()
        self.main_login_frame.show()
        self.error_label.setText("Logged out")
        self.error_user_login_label.setText("")

    def select_image_file_screen2(self):
        self.fileName = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "","Image Files (*.jpg)")[0]

    def load_bytes_image(self, image_bytes):
        qp = QPixmap()
        qp.loadFromData(image_bytes)
        return qp

    def show_image_preview_screen2(self):
        try:
            car_image = QPixmap(self.fileName).scaledToHeight(190)
            self.preview_image_bitmap.setPixmap(car_image)
        except Exception:
            print("Error No Image loaded")

    def load_cars_from_database_screen2(self):
        cars = self.get_all_cars()
        if cars != []:
            for car in cars:
                car_id = car[0]
                car_name = (car[1] + " " + car[2])
                car_color = car[3]
                car_year = car[4]
                car_rent = car[5]
                car_plate = car[6]
                car_image = car[8]
                self.reload_admin_scroll_data_screen2(car_id, car_name, car_color, car_year, car_plate, car_rent, car_image)

    def reload_admin_scroll_data_screen2(self, car_id, car_name, car_color, car_year, car_number_plate, car_rent, car_image):
        self.car_admin_frame = QtWidgets.QFrame(self.admin_car_scroll_contents)
        self.car_admin_frame.setMinimumSize(QtCore.QSize(581, 90))
        self.car_admin_frame.setMaximumSize(QtCore.QSize(581, 90))
        self.car_admin_frame.setObjectName(f"{car_name}")

        self.car_bit_map = QtWidgets.QFrame(self.car_admin_frame)
        self.car_bit_map.setGeometry(QtCore.QRect(0, 0, 131, 90))
        self.car_bit_map.setMinimumSize(QtCore.QSize(131, 90))
        self.car_bit_map.setMaximumSize(QtCore.QSize(131, 90))

        self.car_bit_map_label = QtWidgets.QLabel(self.car_bit_map)
        self.car_bit_map_label.setGeometry(QtCore.QRect(0, 2, 131, 91))
        try:
            self.car_bit_map_label.setPixmap(self.load_bytes_image(car_image).scaledToWidth(140))
        except Exception:
            self.car_bit_map_label.setText("No image")
        self.car_data_container = QtWidgets.QFrame(self.car_admin_frame)
        self.car_data_container.setGeometry(QtCore.QRect(130, 0, 360, 90))
        self.car_data_container.setMinimumSize(QtCore.QSize(360, 90))
        self.car_data_container.setMaximumSize(QtCore.QSize(360, 90))
        self.car_data_container.setStyleSheet("background-color: rgb(255, 200, 138);")

        self.car_name = QtWidgets.QLabel(self.car_data_container)
        self.car_name.setGeometry(QtCore.QRect(20, 20, 200, 21))
        self.car_name.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.car_name.setText(f"{str(car_name).upper()} {str(car_year).split('.')[0]} {car_color}")
        
        self.car_meta_data = QtWidgets.QLabel(self.car_data_container)
        self.car_meta_data.setGeometry(QtCore.QRect(20, 40, 300, 41))
        self.car_meta_data.setText(f"CAR NUMBER:{car_number_plate} RENT:{car_rent}")
        self.car_delete_button = QtWidgets.QPushButton(self.car_admin_frame)
        self.car_delete_button.setGeometry(QtCore.QRect(500, 10, 75, 71))
        self.car_delete_button.setText("Delete")
        self.car_delete_button.clicked.connect(lambda: self.car_delete_operation_screen2(car_id))
        self.verticalLayout_screen2.addWidget(self.car_admin_frame)

    def car_delete_operation_screen2(self, arguments):
        print(arguments)
        self.verticalLayout_screen2.removeItem(self.verticalSpacer_screen2)
        self.delete_car(car_id=arguments)
        for i in reversed(range(self.verticalLayout_screen2.count())):
            widgetToRemove = self.verticalLayout_screen2.itemAt(i).widget()
            self.verticalLayout_screen2.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        self.load_cars_from_database_screen2()
        self.verticalLayout_screen2.addItem(self.verticalSpacer_screen2)

    def reload_cars_from_database_screen2(self):
        self.verticalLayout_screen2.removeItem(self.verticalSpacer_screen2)
        for i in reversed(range(self.verticalLayout_screen2.count())):
            widgetToRemove = self.verticalLayout_screen2.itemAt(i).widget()
            self.verticalLayout_screen2.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        self.load_cars_from_database_screen2()
        self.verticalLayout_screen2.addItem(self.verticalSpacer_screen2)

    def add_new_car_operation_screen2(self):
        try:
            try:
                total = self.get_all_cars()
                list_auto = []
                for cars in total:
                    list_auto.append(int(cars[0]))
                car_id = list_auto[-1] + 1
            except Exception:
                car_id = 1
            car_company = self.admin_car_company_add.text()
            car_make = self.admin_car_make_add.text()
            car_color = self.admin_car_color_add.text()
            car_year = self.admin_car_year_select.text()
            car_number_plate = self.admin_car_number_add.text()
            car_rental_price = (self.admin_car_rental_price_select.text().split("/")[0][1:])
            car_description = self.admin_car_description.toPlainText()
            if car_company != "":
                if car_make != "":
                    if car_number_plate !="":
                        if car_color !="":
                            if car_rental_price != "0":
                                if self.fileName is not None:
                                    output = self.add_new_car(car_id,
                                                                  car_company,
                                                                  car_make,
                                                                  car_color,
                                                                  car_year,
                                                                  car_rental_price,
                                                                  car_number_plate,
                                                                  car_description,
                                                                  self.fileName)
                                    print(output)
                                    self.reload_cars_from_database_screen2()
        except Exception:
            print("Form not filled right")

    def load_text_rental_screen2(self):
        self.main_program_title.setText("CAR RENTAL SERVICE")
        self.welcome_admin_label.setText("Welcome to Admin Area")
        self.admin_car_rental_label.setText("Car Rental Price")
        self.admin_car_color_label.setText("Car Color")
        self.admin_car_company_label.setText("Car Company")
        self.admin_car_number_label.setText("Car Number")
        self.admin_car_model_label.setText("Car Model")
        self.admin_car_year_label.setText("Car Year")
        self.preview_image_bitmap.setText("Preview image bitmap")
        self.admin_car_rental_price_select.setSuffix("/Week")
        self.admin_car_rental_price_select.setPrefix("$")
        self.admin_car_year_select.setDisplayFormat("yyyy")
        self.admin_select_car_image.setText("Select Image")
        self.admin_car_description_label.setText("Description")
        self.admin_add_image_button.setText("Show Image")
        self.admin_car_image_label.setText("Car Image")
        self.add_car_new.setText("Add Record")

        #_______________________________________________________________________

    def load_screen3(self):
        self.main_book_rental_frame = QtWidgets.QFrame(self.main_widget)
        self.main_book_rental_frame.setGeometry(QtCore.QRect(0, 69, 961, 641))
        self.car_show_frame = QtWidgets.QFrame(self.main_book_rental_frame)
        self.car_show_frame.setGeometry(QtCore.QRect(640, 10, 321, 621))
        self.description_text_box = QtWidgets.QTextBrowser(self.car_show_frame)
        self.description_text_box.setGeometry(QtCore.QRect(10, 270, 301, 231))
        self.car_rental_price = QtWidgets.QLabel(self.car_show_frame)
        self.car_rental_price.setGeometry(QtCore.QRect(10, 510, 301, 41))
        self.car_rental_price.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.alert_rental_request_label = QtWidgets.QLabel(self.car_show_frame)
        self.alert_rental_request_label.setGeometry(QtCore.QRect(20, 550, 131, 16))
        self.alert_rental_request_label.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.alert_rental_request_label.setObjectName("alert_rental_request_label")
        self.add_to_rental_request_button = QtWidgets.QPushButton(self.car_show_frame)
        self.add_to_rental_request_button.setGeometry(QtCore.QRect(170, 580, 131, 23))
        self.logout_from_account = QtWidgets.QPushButton(self.car_show_frame)
        self.logout_from_account.setGeometry(QtCore.QRect(20, 580, 131, 23))
        self.logout_from_account.clicked.connect(self.logout_book_rentals_screen3)
        self.label = QtWidgets.QLabel(self.car_show_frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 301, 261))
        self.cardata_filter_frame = QtWidgets.QFrame(self.main_book_rental_frame)
        self.cardata_filter_frame.setGeometry(QtCore.QRect(10, 10, 631, 621))
        self.apply_filter = QtWidgets.QPushButton(self.cardata_filter_frame)
        self.apply_filter.setGeometry(QtCore.QRect(450, 70, 61, 23))
        self.apply_filter.clicked.connect(self.load_with_filter_screen3)
        self.price_filter = QtWidgets.QSpinBox(self.cardata_filter_frame)
        self.price_filter.setGeometry(QtCore.QRect(310, 70, 121, 22))
        self.price_filter.setMaximum(10000)
        self.price_filter.setSingleStep(50)
        self.filter_label_5 = QtWidgets.QLabel(self.cardata_filter_frame)
        self.filter_label_5.setGeometry(QtCore.QRect(320, 40, 91, 16))
        self.filter_label_4 = QtWidgets.QLabel(self.cardata_filter_frame)
        self.filter_label_4.setGeometry(QtCore.QRect(230, 40, 71, 16))
        self.car_color_filter = QtWidgets.QComboBox(self.cardata_filter_frame)
        self.car_color_filter.setGeometry(QtCore.QRect(150, 70, 61, 22))
        self.car_color_filter.addItem("")
        self.filter_label_3 = QtWidgets.QLabel(self.cardata_filter_frame)
        self.filter_label_3.setGeometry(QtCore.QRect(150, 40, 41, 16))
        self.car_year_filter = QtWidgets.QComboBox(self.cardata_filter_frame)
        self.car_year_filter.setGeometry(QtCore.QRect(70, 70, 61, 22))
        self.car_year_filter.addItem("")
        self.filter_label_2 = QtWidgets.QLabel(self.cardata_filter_frame)
        self.filter_label_2.setGeometry(QtCore.QRect(70, 40, 41, 16))
        self.filter_label = QtWidgets.QLabel(self.cardata_filter_frame)
        self.filter_label.setGeometry(QtCore.QRect(10, 70, 41, 16))
        self.search_name_label = QtWidgets.QLabel(self.cardata_filter_frame)
        self.search_name_label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.search_by_name = QtWidgets.QLineEdit(self.cardata_filter_frame)
        self.search_by_name.setGeometry(QtCore.QRect(120, 10, 311, 21))
        self.scrollArea = QtWidgets.QScrollArea(self.cardata_filter_frame)
        self.scrollArea.setGeometry(QtCore.QRect(0, 110, 621, 511))
        self.scrollArea.setMinimumSize(QtCore.QSize(621, 511))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 604, 588))
        self.verticalLayout_screen3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.car_license_plate = QtWidgets.QLineEdit(self.cardata_filter_frame)
        self.car_license_plate.setGeometry(QtCore.QRect(230, 70, 61, 21))
        self.reload_list = QtWidgets.QPushButton(self.cardata_filter_frame)
        self.reload_list.setGeometry(QtCore.QRect(520, 70, 61, 23))
        self.reload_list.clicked.connect(self.reload_cars_from_database_screen3)
        car_rental_mainwindow.setCentralWidget(self.main_widget)
        self.verticalSpacer_screen3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.load_cars_from_database_screen3()
        self.populate_drop_downs_screen3()
        self.verticalLayout_screen3.addItem(self.verticalSpacer_screen3)
        self.load_text_for_rental_screen3()
        QtCore.QMetaObject.connectSlotsByName(car_rental_mainwindow)
        self.main_book_rental_frame.hide()

    def load_cars_from_database_screen3(self):
        cars = self.get_all_cars()
        if cars != []:
            for car in cars:
                car_name = (car[1] + " " + car[2])
                car_color = car[3]
                car_year = car[4]
                car_rent = car[5]
                car_plate = car[6]
                car_image = car[8]
                self.rental_card_frames_screen3(car_name, car_color, car_year, car_plate, car_rent, car_image)

    def load_with_filter_screen3(self):
        search = self.search_by_name.text()
        year = self.car_year_filter.currentText()
        car_color = self.car_color_filter.currentText()
        license = self.car_license_plate.text()
        price = self.price_filter.value()
        if price == 0:
            price = ""
        cars_filtered = self.car_filter(car_make=search,car_color=car_color, car_year=year,car_number_plate=license,car_rental=price)
        cars = cars_filtered
        self.verticalLayout_screen3.removeItem(self.verticalSpacer_screen3)
        for i in reversed(range(self.verticalLayout_screen3.count())):
            widgetToRemove = self.verticalLayout_screen3.itemAt(i).widget()
            self.verticalLayout_screen3.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        if cars != []:
            for car in cars:
                car_name = (car[1] + " " + car[2])
                car_color = car[3]
                car_year = car[4]
                car_rent = car[5]
                car_plate = car[6]
                car_image = car[8]
                self.rental_card_frames_screen3(car_name, car_color, car_year, car_plate, car_rent, car_image)
        self.verticalLayout_screen3.addItem(self.verticalSpacer_screen3)

    def reload_cars_from_database_screen3(self):
        self.verticalLayout_screen3.removeItem(self.verticalSpacer_screen3)
        for i in reversed(range(self.verticalLayout_screen3.count())):
            widgetToRemove = self.verticalLayout_screen3.itemAt(i).widget()
            self.verticalLayout_screen3.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        self.load_cars_from_database_screen3()
        self.verticalLayout_screen3.addItem(self.verticalSpacer_screen3)

    def rental_card_frames_screen3(self, car_name, car_color, car_year, car_number_plate, car_rent, car_image):
        self.car_search_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.car_search_frame.setMinimumSize(QtCore.QSize(581, 90))
        self.car_search_frame.setMaximumSize(QtCore.QSize(581, 90))
        self.car_search_frame.setObjectName(f"{car_name}")

        self.car_bit_map_frame = QtWidgets.QFrame(self.car_search_frame)
        self.car_bit_map_frame.setGeometry(QtCore.QRect(0, 0, 131, 90))
        self.car_bit_map_frame.setMinimumSize(QtCore.QSize(131, 90))
        self.car_bit_map_frame.setMaximumSize(QtCore.QSize(131, 90))

        self.car_bit_map = QtWidgets.QLabel(self.car_bit_map_frame)
        self.car_bit_map.setGeometry(QtCore.QRect(0, 2, 131, 91))
        try:
            self.car_bit_map.setPixmap(self.load_bytes_image(car_image).scaledToWidth(130))
        except Exception:
            self.car_bit_map.setText("No image")
        self.car_data_container = QtWidgets.QFrame(self.car_search_frame)
        self.car_data_container.setGeometry(QtCore.QRect(130, 0, 360, 90))
        self.car_data_container.setMinimumSize(QtCore.QSize(360, 90))
        self.car_data_container.setMaximumSize(QtCore.QSize(360, 90))
        self.car_data_container.setStyleSheet("background-color: rgb(255, 200, 138);")
        self.car_name = QtWidgets.QLabel(self.car_data_container)
        self.car_name.setGeometry(QtCore.QRect(20, 20, 200, 21))
        self.car_name.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.car_name.setText(f"{str(car_name).upper()} {str(car_year).split('.')[0]} {car_color}")
        self.car_meta_data = QtWidgets.QLabel(self.car_data_container)
        self.car_meta_data.setGeometry(QtCore.QRect(20, 40, 300, 41))
        self.car_meta_data.setText(f"CAR NUMBER:{car_number_plate} RENT:{car_rent}")
        self.car_scroll_rent_button = QtWidgets.QPushButton(self.car_search_frame)
        self.car_scroll_rent_button.setGeometry(QtCore.QRect(500, 10, 75, 71))
        self.car_scroll_rent_button.clicked.connect(lambda: self.show_details_for_car_screen3(car_name))
        self.car_scroll_rent_button.setText("Show")
        self.verticalLayout_screen3.addWidget(self.car_search_frame)

    def show_details_for_car_screen3(self, car_name):
        try:
            self.add_to_rental_request_button.clicked.disconnect()
        except Exception:
            pass
        print(car_name)
        car_make = str(car_name).split(" ")[1]
        detail = self.get_specific_car(car_make=car_make)
        car_name = detail[2]
        car_rent = detail[5]
        car_description = detail[7]
        car_image = detail[8]
        try:
            self.label.setPixmap(self.load_bytes_image(car_image).scaledToWidth(300))
            self.car_rental_price.setText( f"Price: ${str(car_rent)} / Per Week")
        except Exception:
            self.label.setText("No image")
        try:
            rental_id = self.rental_auto_number_screen3()
            if rental_id <= 1:
                rental_id = 2
        except Exception:
            rental_id = 1
        self.description_text_box.setText(car_description)
        self.add_to_rental_request_button.clicked.connect(lambda: self.add_new_rental_request_screen3(rental_id, car_name))

    def add_new_rental_request_screen3(self, rental_id, car_name):
        print(f"{rental_id}, {car_name}")
        self.add_request_rental(rental_id, car_name, self.current_user)
        self.alert_rental_request_label.setText("Rental Request Added")

    def rental_auto_number_screen3(self):
        total = self.get_all_rentals()
        list_auto = []
        for rentals in total:
            print(rentals)
            list_auto.append(int(rentals[0]))
        return list_auto[-1] + 1

    def populate_drop_downs_screen3(self):
        cars = self.get_all_cars()
        list_of_color = []
        list_years = []
        for car in cars:
            list_of_color.append(car[3])
            list_years.append(car[4])
        unique_color = list(dict.fromkeys(list_of_color))
        unique_year = list(dict.fromkeys(list_years))
        for color in unique_color:
            self.car_color_filter.addItem(str(color).upper())
        for year in unique_year:
            self.car_year_filter.addItem(str(year).split(".")[0])

    def load_text_for_rental_screen3(self):
        self.main_program_title.setText("CAR RENTAL SERVICE")
        self.add_to_rental_request_button.setText("Make Rental Request")
        self.logout_from_account.setText("Log out")
        self.label.setText(" Car Picture ")
        self.apply_filter.setText("Apply")
        self.price_filter.setSuffix("/Per Week")
        self.price_filter.setPrefix("$")
        self.filter_label_5.setText("Car Rental Price")
        self.filter_label_4.setText("License Plate")
        self.filter_label_3.setText("Color")
        self.filter_label_2.setText("Year")
        self.filter_label.setText("Filters")
        self.search_name_label.setText("Search by car name")
        self.reload_list.setText("Cancel")
    
    def logout_book_rentals_screen3(self):
        try:
            self.add_to_rental_request_button.clicked.disconnect()
        except Exception:
            pass


        self.car_rental_price.setText(" ")
        self.description_text_box.setText(" ")
        self.alert_rental_request_label.setText("")
        self.user_login_form_admin.hide()
        self.load_text_for_rental_screen3()
        self.main_book_rental_frame.hide()
        self.main_login_frame.show()
        self.reload_rentals_from_database_screen1()
        self.error_user_login_label.setText("Logged Out")
        self.error_label.setText("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    car_rental_mainwindow = QtWidgets.QMainWindow()
    ui = car_rental_app()
    ui.start_up(car_rental_mainwindow)
    car_rental_mainwindow.show()
    sys.exit(app.exec_())
