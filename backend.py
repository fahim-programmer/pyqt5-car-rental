import os
import sqlite3

""" 
Tables of the database 
USER_ACCOUNTS; ID, USER_NAME, USER_EMAIL, USER_PASS
ADMIN_ACCOUNTS; ID, USER_NAME, USER_EMAIL, USER_PASS
CAR_DATA; ID, CAR_COMPANY, CAR_MAKE, CAR_COLOR, CAR_YEAR, CAR_RENTAL, CAR_NUMBER_PLATE, CAR_IMAGE_BYTES, CAR_DESCRIPTION
CAR_RENTAL_DATA; ID, CAR_MAKE, CAR_ID, RENTAL_REQUEST_BY 
"""

class app_database():
    def __init__(self) -> None:
        self.create_connection("car_rental_database.db")
        print("Successfully connected with database")

    def refresh_connection(self):
        self.close_connection()
        self.create_connection("car_rental_database.db")

    def create_connection(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(f"{self.get_path()}{db_file}")
        except sqlite3.Error as e:
            print(e)

    def execute_command(self, query, format_tuple):
        sql_cursor = self.conn.execute(query, (format_tuple))
        return sql_cursor

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def put_data_to_table(self, table_name, table_headers, values):
        self.conn.execute(f"INSERT INTO {table_name} {table_headers} VALUES {values};")
        self.conn.commit()

    def make_table(self, table_name, fields):
        self.conn.execute(f'''CREATE TABLE {table_name}({fields});''')
        print("Table created successfully")

    def del_table(self, table_name):
        self.conn.execute(f'''DROP TABLE {table_name};''')
        print("Table deleted successfully")

    def add_column(self, table_name, new_column_name, column_definition):
        self.conn.execute(f"ALTER TABLE {table_name} ADD {new_column_name} {column_definition};")
        print(f"{new_column_name} created successfully in table {table_name}")
        self.conn.commit()

    def delete_column(self, table_name, del_column_name):
        self.conn.execute(f"ALTER TABLE {table_name} DROP COLUMN {del_column_name};")
        print(f"{del_column_name} deleted successfully in table {table_name}")
        self.conn.commit()

    # _____________________________________________________________________________________________
    # APP SPECIFIC COMMANDS PAGE MAIN LOGIN
    # USER_ACCOUNTS Functions
    def get_user_data(self, user_email, user_password):
        try:
            specific_user = self.conn.execute(
                f'''SELECT USER_NAME, USER_PASS FROM USER_ACCOUNTS WHERE USER_EMAIL="{user_email}" AND USER_PASS="{user_password}"''')
            self.conn.commit()
            return specific_user
        except Exception:
            return "Failed to Get User Data"

    # Not Tested
    def get_user_data_all(self):
        try:
            users = self.conn.execute(f'''SELECT * FROM USER_ACCOUNTS''')
            list_user = []
            for user in users:
                # print(user)
                list_user.append(user)
            self.conn.commit()
            return list_user
        except Exception:
            return "Failed to Get User Data"

    # Not Tested
    def add_new_user(self, id, user_name, user_email, user_pass):
        try:
            self.execute_command("INSERT INTO USER_ACCOUNTS (ID, USER_NAME, USER_EMAIL, USER_PASS) VALUES (?,?,"
                                 "?,?);", (id, user_name, user_email, user_pass))
            self.conn.commit()
            return "Added New User"
        except Exception:
            return "New User wasn't added"

    # ADMIN_ACCOUNTS Functions
    def get_admin_data(self, user_email, user_password):
        try:
            specific_user = self.conn.execute("SELECT USER_EMAIL, USER_PASS FROM ADMIN_ACCOUNTS WHERE USER_EMAIL=? AND "
                                              "USER_PASS=?", (user_email, user_password))
            admin_account_data = []
            for data in specific_user:
                admin_account_data.append(data)
            self.conn.commit()
            return admin_account_data
        except Exception:
            return "Failed to get admin data"

    def get_admin_data_all(self):
        try:
            users = self.conn.execute('''SELECT * FROM ADMIN_ACCOUNTS''')
            list_admin = []
            for user in users:
                list_admin.append(user)
            self.conn.commit()
            return list_admin
        except Exception:
            return "Failed to get data of Admins"

    def add_new_admin(self, id, user_name, user_email, user_pass):
        try:
            self.execute_command(
                f"INSERT INTO ADMIN_ACCOUNTS (ID, USER_NAME, USER_EMAIL, USER_PASS)  VALUES (?,?,?,?);",
                (id, user_name, user_email, user_pass))
            self.conn.commit()
            return "New Admin Added"
        except Exception:
            return "Failed to add admin"

    # Not Tested
    def del_user(self, user_email):
        try:
            self.conn.execute(f"DELETE FROM USER_ACCOUNTS WHERE USER_EMAIL='{user_email}';")
            self.conn.commit()
            return f"Deleted User {user_email}"
        except Exception:
            return "Failed to delete user"

    # Not Tested
    def del_admin(self, admin_email):
        try:
            self.conn.execute(f"DELETE FROM ADMIN_ACCOUNTS WHERE USER_EMAIL='{admin_email}';")
            self.conn.commit()
            return f"Admin account {admin_email} deleted"
        except Exception:
            return "Failed to delete admin"

    # WORKING WITH RENTALS
    def get_all_rentals(self):
        try:
            all_rentals = self.conn.execute('''SELECT * FROM CAR_RENTAL_DATA''')
            list_of_rentals = []
            for rental in all_rentals:
                list_of_rentals.append(rental)
            self.conn.commit()
            if list_of_rentals != []:
                return list_of_rentals
        except Exception:
            return "No Requested Rentals"

    # Tested
    def verify_user_data(self, user_name):
        try:
            specific_user = self.conn.execute(
                f'''SELECT USER_NAME FROM USER_ACCOUNTS WHERE USER_NAME="{(str(user_name).lower())}"''')
            status = "User Not found"
            for value in specific_user:
                status = value[0]
            self.conn.commit()
            return status
        except Exception:
            return "User Not found"

    # Tested
    def verify_car_data(self, car_name):
        try:
            car_id = self.conn.execute(f'''SELECT * FROM CAR_DATA WHERE CAR_MAKE='{str(car_name).lower()}';''')
            status_id = "Car Not found"
            status_car = "Car ID Not found"
            for name in car_id:
                #print(name[:-1])
                status_id = name[:-1][2]
                status_car = name[:-1][0]
            self.conn.commit()
            return status_id, status_car
        except Exception:
            return "Car Not found"

    # Finalized
    def add_request_rental(self, id, car_name, user_who_requested):
        car_name_verified, car_id_verified = self.verify_car_data(car_name.lower())
        print(car_id_verified)
        user_name_verified = self.verify_user_data(user_who_requested)
        try:
            if user_name_verified != "User Not found":
                if car_name_verified != "Car Not found":
                    self.conn.execute(
                        f"INSERT INTO CAR_RENTAL_DATA (ID, CAR_MAKE, CAR_ID, RENTAL_REQUEST_BY)  "
                        f"VALUES ('{id}','{car_name_verified}','{car_id_verified}','{user_name_verified}');")
                    self.conn.commit()
                    return f"Rental Request Added {car_name_verified}"
        except Exception:
            return "Rental request not successful"

    # Finalized
    def delete_request_rental(self, id, user_who_requested):
        if id and user_who_requested is not None:
            try:
                self.conn.execute(
                    f"DELETE FROM CAR_RENTAL_DATA WHERE ID='{id}' AND RENTAL_REQUEST_BY='{user_who_requested}';")
                self.conn.commit()
            except Exception:
                return "Rental Request Doesn't Exists"
            return "Deleted Rental Request"
        else:
            return "Failed to Delete Rental Request"
        # verification function will return the right car ID

    def check_already_in_rental(self, id, rented_car):
        rented_filter = self.conn.execute(f"SELECT * FROM CAR_RENTAL_DATA "
                                          f"WHERE ID LIKE '{id}%' AND CAR_ID LIKE '{rented_car}%';")
        rented_result = []
        for cars in rented_filter:
            rented_result.append(cars)
        self.conn.commit()
        return rented_result

    # WORKING WITH CARS
    # Tested
    def add_new_car(self, id, car_company, car_make, car_color, car_year, car_rental, car_number_plate, car_description,
                    car_bitmap):
        try:
            with open(car_bitmap, "rb") as file:
                car_image_bytes = file.read()
            query = """INSERT INTO CAR_DATA (ID, CAR_COMPANY, CAR_MAKE, CAR_COLOR, CAR_YEAR, CAR_RENTAL, CAR_NUMBER_PLATE, CAR_DESCRIPTION, CAR_IMAGE_BYTES) 
            VALUES (?,?,?,?,?,?,?,?,?) """
            self.conn.execute(query, (
                id, car_company.lower(), car_make.lower(), car_color.lower(), car_year, car_rental,
                car_number_plate, car_description, car_image_bytes))
            self.conn.commit()
            return f"New car {car_make} added"
        except Exception:
            return "Failed in adding a car"

    # Tested
    def delete_car(self, car_id=None, car_name=None):
        if car_id or car_name is not None:
            try:
                self.conn.execute(f"DELETE FROM CAR_DATA WHERE ID='{car_id}' OR CAR_MAKE='{car_name}';")
                self.conn.execute(f"DELETE FROM CAR_RENTAL_DATA WHERE ID='{car_id}' OR CAR_MAKE='{car_name}';")
                self.conn.commit()
                return "Deleted"
            except Exception:
                return "Car doesn't Exists"
        else:
            print("Provide car_id or car_name")

    # Tested
    def get_all_cars(self):
        users = self.conn.execute('''SELECT * FROM CAR_DATA''')
        list_cars = []
        for user in users:
            list_cars.append(user)
        self.conn.commit()
        return list_cars

    # Tested
    def get_all_cars_without_image(self):
        users = self.conn.execute('''SELECT * FROM CAR_DATA''')
        list_cars = []
        for user in users:
            list_cars.append(user[:-1])
        self.conn.commit()
        return list_cars

    # Tested
    def get_specific_car(self, car_make="", car_color="", car_year="", car_rent=""):
        try:
            query = """
            SELECT * FROM CAR_DATA 
            WHERE CAR_MAKE=?   
            OR CAR_COLOR=? 
            OR CAR_YEAR=? 
            OR CAR_RENTAL=?;"""
            cars = self.conn.execute(query, (car_make.lower(), car_color.lower(), car_year, car_rent))
            specific_car = []
            for car in cars:
                specific_car.append(car)
            self.conn.commit()
            return specific_car[0]
        except Exception:
            return "No car found"

    # Tested
    def car_filter(self, car_company="", car_make="", car_color="", car_rental="", car_year="", car_number_plate=""):
        try:
            filtered = self.conn.execute(f"SELECT * FROM CAR_DATA "
                                         f"WHERE CAR_COMPANY LIKE '%{car_company}%' "
                                         f"AND CAR_MAKE LIKE '%{car_make}%' "
                                         f"AND CAR_COLOR LIKE '{car_color}%' "
                                         f"AND CAR_RENTAL <= '{str(car_rental)}'"
                                         f"AND CAR_YEAR LIKE '{str(car_year)}%'"
                                         f"AND CAR_NUMBER_PLATE LIKE '%{str(car_number_plate)}';")
            filtered_cars = []
            for cars in filtered:
                # print(cars[:-2])
                filtered_cars.append(cars)
            self.conn.commit()
            return filtered_cars
        except Exception:
            return "Failed to filter cars"

    # CAR RENTAL PREVIEW
    # Tested
    def get_car_image(self, car_name, save_name=None):
        try:
            car = self.get_specific_car(car_make=car_name)
            if save_name is None:
                return car[8]
            if car:
                with open(save_name, "wb") as e:
                    e.write(car[8])
                    e.close()
                    return "Image exported"
        except Exception:
            return "Failed to get car image"

    # Tested
    def get_car_description(self, car_name):
        try:
            description = (self.get_specific_car(car_make=car_name))[7]
            return description
        except Exception:
            return f"No description found for this car {car_name}"

    @staticmethod
    def get_path():
        path = (os.path.dirname(os.path.abspath(__file__)) + "\\")
        return path


if __name__ == '__main__':
    app_database()
