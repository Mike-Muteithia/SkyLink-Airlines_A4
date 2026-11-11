import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_NAME = 'flight_ticketing.db'

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Table 1: Flights
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            airline_name TEXT NOT NULL,
            departure_city TEXT NOT NULL,
            destination_city TEXT NOT NULL,
            departure_date DATE NOT NULL,
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            travel_class TEXT NOT NULL,
            ticket_price REAL NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL
        )
    ''')

    # Table 2: Passengers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            identification_number TEXT NOT NULL
        )
    ''')

    # Table 3: Bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_reference TEXT UNIQUE NOT NULL,
            passenger_id INTEGER NOT NULL,
            flight_id INTEGER NOT NULL,
            number_of_passengers INTEGER NOT NULL,
            travel_class TEXT NOT NULL,
            total_cost REAL NOT NULL,
            booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            booking_status TEXT NOT NULL CHECK(booking_status IN ('Pending', 'Confirmed', 'Cancelled')),
            FOREIGN KEY (passenger_id) REFERENCES passengers (passenger_id),
            FOREIGN KEY (flight_id) REFERENCES flights (flight_id)
        )
    ''')

    # Table 4: Administrators
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administrators (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Table 5: Contact Messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            submission_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")

def seed_data():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Check if admin exists; if not, create one securely
    cursor.execute("SELECT * FROM administrators WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO administrators (username, password_hash) VALUES (?, ?)", ('admin', hashed_pw))
        print("Default admin account created (username: admin, password: admin123).")

    # Insert sample flights if the flights table is empty
    cursor.execute("SELECT COUNT(*) FROM flights")
    if cursor.fetchone()[0] == 0:
        sample_flights = [
            ('SL401', 'Jasiri Air', 'Eldoret (EDL)', 'Nairobi (NBO)', '2026-11-15', '13:45', '15:00', 'Economy', 5174.44, 150, 86),
            ('SL402', 'SkyLink Airlines', 'Malindi (MYD)', 'Mombasa (MBA)', '2026-11-22', '18:45', '20:00', 'Economy', 8602.59, 80, 39),
            ('SL403', 'Jasiri Air', 'Eldoret (EDL)', 'Kisumu (KIS)', '2026-11-17', '11:45', '12:30', 'Business', 21272.38, 30, 8),
            ('SL404', 'SkyLink Airlines', 'Eldoret (EDL)', 'Kisumu (KIS)', '2026-11-16', '10:30', '12:00', 'Business', 16785.57, 12, 9),
            ('SL405', 'Jasiri Air', 'Malindi (MYD)', 'Nairobi (NBO)', '2026-11-20', '18:15', '19:15', 'Economy', 8404.65, 100, 97),
            ('SL406', 'SkyLink Airlines', 'Kisumu (KIS)', 'Eldoret (EDL)', '2026-11-12', '16:30', '17:15', 'Economy', 11924.14, 100, 5),
            ('SL407', 'Jasiri Air', 'Nairobi (NBO)', 'Kisumu (KIS)', '2026-11-10', '08:30', '09:45', 'Business', 18812.32, 30, 26),
            ('SL408', 'Jasiri Air', 'Kisumu (KIS)', 'Nairobi (NBO)', '2026-11-21', '16:30', '17:45', 'Economy', 9613.66, 150, 87),
            ('SL409', 'SkyLink Airlines', 'Mombasa (MBA)', 'Malindi (MYD)', '2026-11-12', '14:45', '16:00', 'Economy', 10259.73, 80, 32),
            ('SL410', 'SkyLink Airlines', 'Kisumu (KIS)', 'Eldoret (EDL)', '2026-11-14', '17:00', '18:00', 'Business', 20995.39, 20, 18),
            ('SL411', 'Jasiri Air', 'Kisumu (KIS)', 'Eldoret (EDL)', '2026-11-11', '16:45', '18:15', 'Business', 17816.51, 12, 9),
            ('SL412', 'Jasiri Air', 'Mombasa (MBA)', 'Kisumu (KIS)', '2026-11-22', '19:00', '20:15', 'Economy', 11344.66, 100, 50),
            ('SL413', 'Jasiri Air', 'Kisumu (KIS)', 'Malindi (MYD)', '2026-11-15', '08:15', '09:00', 'Business', 23332.12, 12, 5),
            ('SL414', 'Jasiri Air', 'Nairobi (NBO)', 'Kisumu (KIS)', '2026-11-19', '08:00', '09:15', 'Business', 16764.27, 30, 19),
            ('SL415', 'SkyLink Airlines', 'Mombasa (MBA)', 'Eldoret (EDL)', '2026-11-22', '18:00', '19:30', 'Business', 22952.21, 12, 5),
            ('SL416', 'SkyLink Airlines', 'Kisumu (KIS)', 'Malindi (MYD)', '2026-11-16', '17:00', '18:15', 'Business', 23903.11, 30, 5),
            ('SL417', 'SkyLink Airlines', 'Nairobi (NBO)', 'Kisumu (KIS)', '2026-11-11', '12:15', '13:15', 'Economy', 9427.7, 150, 139),
            ('SL418', 'Jasiri Air', 'Eldoret (EDL)', 'Kisumu (KIS)', '2026-11-16', '20:15', '21:30', 'Economy', 11912.85, 80, 38),
            ('SL419', 'SkyLink Airlines', 'Malindi (MYD)', 'Nairobi (NBO)', '2026-11-09', '08:15', '09:45', 'Economy', 5104.94, 80, 13),
            ('SL420', 'SkyLink Airlines', 'Nairobi (NBO)', 'Eldoret (EDL)', '2026-11-20', '17:30', '18:45', 'Economy', 6510.13, 80, 29)
        ]
        cursor.executemany('''
            INSERT INTO flights (
                flight_number, airline_name, departure_city, destination_city, 
                departure_date, departure_time, arrival_time, travel_class, 
                ticket_price, total_seats, available_seats
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_flights)
        print(f"{len(sample_flights)} sample flights inserted.")
        
        # Insert 20 Sample Passengers
        sample_passengers = [
            ('Jane Mwangi', 'jane.mwangi@example.com', '+254 745 350 328', '24682115'),
            ('Mary Mwangi', 'mary.mwangi@example.com', '+254 721 323 338', '36956909'),
            ('Naomi Odhiambo', 'naomi.odhiambo@example.com', '+254 738 559 703', '29334531'),
            ('Peter Wanjiku', 'peter.wanjiku@example.com', '+254 729 320 881', '31294238'),
            ('Grace Akinyi', 'grace.akinyi@example.com', '+254 754 718 370', '21457954'),
            ('Simon Kamau', 'simon.kamau@example.com', '+254 780 400 949', '32134457'),
            ('Mary Onyango', 'mary.onyango@example.com', '+254 739 891 396', '22677374'),
            ('Samuel Onyango', 'samuel.onyango@example.com', '+254 756 266 479', '31920906'),
            ('David Wambui', 'david.wambui@example.com', '+254 791 275 646', '28214491'),
            ('Naomi Mutua', 'naomi.mutua@example.com', '+254 797 432 963', '21876966'),
            ('Simon Wanjiku', 'simon.wanjiku@example.com', '+254 718 316 680', '30558837'),
            ('Samuel Ochieng', 'samuel.ochieng@example.com', '+254 743 242 352', '38836388'),
            ('Faith Nanjala', 'faith.nanjala@example.com', '+254 784 508 470', '27359183'),
            ('Mary Akinyi', 'mary.akinyi@example.com', '+254 724 256 742', '25368105'),
            ('Esther Kipkorir', 'esther.kipkorir@example.com', '+254 777 357 666', '20385239'),
            ('Peter Kamau', 'peter.kamau@example.com', '+254 747 545 261', '35224441'),
            ('Alice Mutuku', 'alice.mutuku@example.com', '+254 723 991 740', '30014145'),
            ('Alice Mutuku', 'alice.mutuku@example.com', '+254 777 100 713', '30876872'),
            ('Grace Nanjala', 'grace.nanjala@example.com', '+254 749 345 159', '28082309'),
            ('Joy Akinyi', 'joy.akinyi@example.com', '+254 718 878 645', '24219822')
        ]
        cursor.executemany('''
            INSERT INTO passengers (full_name, email, phone, identification_number) 
            VALUES (?, ?, ?, ?)
        ''', sample_passengers)
        
        # Insert 20 Sample Bookings
        sample_bookings = [
            ('SLK-1BF4A3', 1, 4, 1, 'Business', 16785.57, 'Confirmed'),
            ('SLK-EA6488', 2, 20, 1, 'Economy', 6510.13, 'Confirmed'),
            ('SLK-0AA204', 3, 1, 2, 'Economy', 10348.88, 'Confirmed'),
            ('SLK-3EF991', 4, 4, 1, 'Business', 16785.57, 'Confirmed'),
            ('SLK-567D0E', 5, 15, 1, 'Business', 22952.21, 'Cancelled'),
            ('SLK-70B3DD', 6, 19, 2, 'Economy', 10209.88, 'Confirmed'),
            ('SLK-9921B0', 7, 8, 1, 'Economy', 9613.66, 'Confirmed'),
            ('SLK-F8C49C', 8, 7, 3, 'Business', 56436.96, 'Confirmed'),
            ('SLK-66E428', 9, 6, 4, 'Economy', 47696.56, 'Confirmed'),
            ('SLK-2C3E55', 10, 8, 1, 'Economy', 9613.66, 'Cancelled'),
            ('SLK-830DAA', 11, 7, 4, 'Business', 75249.28, 'Confirmed'),
            ('SLK-05FBA1', 12, 18, 3, 'Economy', 35738.55, 'Confirmed'),
            ('SLK-B6E652', 13, 5, 4, 'Economy', 33618.6, 'Confirmed'),
            ('SLK-67D505', 14, 14, 1, 'Business', 16764.27, 'Confirmed'),
            ('SLK-5819C0', 15, 4, 3, 'Business', 50356.71, 'Confirmed'),
            ('SLK-87FA97', 16, 1, 3, 'Economy', 15523.32, 'Cancelled'),
            ('SLK-BD871D', 17, 17, 2, 'Economy', 18855.4, 'Confirmed'),
            ('SLK-CF92EF', 18, 16, 1, 'Business', 23903.11, 'Confirmed'),
            ('SLK-7D3371', 19, 19, 1, 'Economy', 5104.94, 'Confirmed'),
            ('SLK-1A5E25', 20, 5, 4, 'Economy', 33618.6, 'Cancelled')
        ]
        cursor.executemany('''
            INSERT INTO bookings (booking_reference, passenger_id, flight_id, number_of_passengers, travel_class, total_cost, booking_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_bookings)
        print(f"{len(sample_bookings)} sample bookings and passengers inserted.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    seed_data()