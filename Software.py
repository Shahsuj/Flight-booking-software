# ===================== IMPORTS =====================
import tkinter as tk
from tkinter import messagebox
import mysql.connector as sql
import random as rd
from tkcalendar import Calendar
from datetime import date as dt

# ===================== DB CONNECTION =====================
mycon = sql.connect(host="localhost", user="root", passwd="1234", database="flight_bookings")
cursor = mycon.cursor()
cursor.execute("SELECT MAX(passenger_id) FROM passengers")
data = cursor.fetchone()
count = int(data[0]) + 1 if data[0] else 1

root = tk.Tk()

# ===================== UTILS =====================
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

# ===================== TICKET PRINT =====================
def show_ticket(data):
    ticket_window = tk.Toplevel(root)
    ticket_window.title("Flight Ticket")
    ticket_window.geometry("420x400")
    tk.Label(ticket_window, text="FLIGHT TICKET", font=("Arial", 16, "bold")).pack(pady=10)
    fields = [
        "Booking ID", "Flight ID", "Passenger ID", "Name", "Source",
        "Destination", "Seat Number", "Total Cost (Rs)", "Booking Date", "Flight Date"
    ]
    for i in range(len(fields)):
        frame = tk.Frame(ticket_window)
        frame.pack(anchor="w", padx=12, pady=3)
        tk.Label(frame, text=f"{fields[i]}:", font=("Arial", 11, "bold"), width=17, anchor="w").pack(side="left")
        tk.Label(frame, text=str(data[i]), font=("Arial", 11), anchor="w").pack(side="left")
    tk.Button(ticket_window, text="PRINT", command=ticket_window.destroy).pack(pady=12)

# ===================== ADMIN LOGIN =====================
def admin_login_window():
    clear_window(root)
    root.geometry("1000x1000")
    root.title("Admin Access")
    tk.Label(root, text="-----------------------ADMIN ACCESS--------------------", font=("Arial", 30)).pack(padx=10)
    tk.Label(root, text="PLEASE LOGIN", font=("Arial", 15)).pack(padx=20)
    tk.Button(root, text="LOGIN", command=admin_login, font=("Arial", 18), width=7, height=2).pack(pady=30)

def admin_login():
    clear_window(root)
    tk.Label(root, text="Enter your admin ID").pack()
    bx8 = tk.Entry(root, width=30)
    bx8.pack()
    tk.Label(root, text="Enter your password").pack()
    bx9 = tk.Entry(root, show="*", width=30)
    bx9.pack()
    tk.Button(root, text="Back", command=admin_login_window).pack()

    def data_extraction():
        v8 = bx8.get()
        v9 = bx9.get()
        mycon_local = sql.connect(host="localhost", user="root", passwd="1234", database="flight_bookings")
        cursor_local = mycon_local.cursor()
        cursor_local.execute("SELECT * FROM admin WHERE admin_id='%s' AND admin_password='%s'" % (v8, v9))
        data_local = cursor_local.fetchone()
        if data_local:
            messagebox.showinfo("Success", "You have Successfully logged in")
            login_window()
        else:
            messagebox.showwarning("Error", "No records matched, UNABLE TO LOGIN!!!")

    tk.Button(root, text="Login", command=data_extraction).pack()
    tk.Button(root, text="Retry", command=admin_login).pack()

# ===================== MAIN LOGIN WINDOW =====================
def login_window():
    clear_window(root)
    root.geometry("1000x1000")
    root.title("TICKET BOOKING!!!")
    tk.Label(root, text="TICKET BOOKING!!!", font=("Arial", 18)).pack(padx=10)
    tk.Label(root, text="Choose from Under!!!", font=("Arial", 18)).pack(padx=10)

    tk.Button(root, text="SIGN UP", command=sign_up, font=("Arial", 11)).pack()
    tk.Button(root, text="LOGIN", command=login, font=("Arial", 11)).pack()
    tk.Button(root, text="FLIGHT DETAIL UPDATION", command=flight_edit, font=("Arial", 11)).pack()

# ===================== SIGN UP =====================
def sign_up():
    clear_window(root)
    global count
    tk.Label(root, text="Passenger ID").pack()
    bx7 = tk.Entry(root, width=30)
    bx7.pack()
    bx7.insert(0, str(count))

    tk.Label(root, text="Enter your name").pack()
    bx1 = tk.Entry(root, width=30)
    bx1.pack()

    tk.Label(root, text="Enter your email").pack()
    bx2 = tk.Entry(root, width=30)
    bx2.pack()

    tk.Label(root, text="Enter your passwd").pack()
    bx3 = tk.Entry(root, width=30)
    bx3.pack()

    tk.Label(root, text="Enter your phno").pack()
    bx4 = tk.Entry(root, width=30)
    bx4.pack()

    tk.Label(root, text="Enter your age").pack()
    bx5 = tk.Entry(root, width=30)
    bx5.pack()

    tk.Label(root, text="Choose Your Gender").pack()
    gendervar = tk.StringVar()
    tk.OptionMenu(root, gendervar, "M", "F", "O").pack()

    def connection():
        j = int(bx7.get())
        k = bx1.get()
        l = bx2.get()
        m = bx3.get()
        n = bx4.get()
        o = int(bx5.get())
        p = gendervar.get()
        mycon_local = sql.connect(host="localhost", user="root", passwd="1234", database="flight_bookings")
        cursor_local = mycon_local.cursor()
        q = "INSERT INTO passengers VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor_local.execute(q, (j, k, l, o, p, n, m))
        mycon_local.commit()
        messagebox.showinfo("Success", "Signup successful!")
        login_window()

    tk.Button(root, text="Back", command=login_window).pack()
    tk.Button(root, text="Sign Up confirmation", command=connection, font=("Arial", 11)).pack()

# ===================== PASSENGER LOGIN =====================
def login():
    clear_window(root)
    tk.Label(root, text="Enter your passenger ID").pack()
    bx8 = tk.Entry(root, width=30)
    bx8.pack()
    tk.Label(root, text="Enter your password").pack()
    bx9 = tk.Entry(root, show="*", width=30)
    bx9.pack()

    def data_extraction():
        v8 = bx8.get()
        v9 = bx9.get()
        mycon_local = sql.connect(host="localhost", user="root", passwd="1234", database="flight_bookings")
        cursor_local = mycon_local.cursor()
        cursor_local.execute("SELECT * FROM passengers WHERE passenger_id=%s AND passwd='%s'" % (v8, v9))
        data_local = cursor_local.fetchone()
        if data_local:
            messagebox.showinfo("Success", "You have Successfully logged in")
            home_page(v8)
        else:
            messagebox.showwarning("Error", "No records matched, UNABLE TO LOGIN!!!")

    tk.Button(root, text="Login", command=data_extraction).pack()
    tk.Button(root, text="Retry", command=login).pack()
    tk.Button(root, text="Back", command=login_window).pack()

# ===================== HOME PAGE =====================
def home_page(passenger_id):
    clear_window(root)
    root.geometry("1000x800")
    root.title("Flight Booking Home")

    tk.Label(root, text="Welcome Passenger " + str(passenger_id), font=("Arial", 18)).pack(pady=10)
    tk.Label(root, text="Source Airport/City").pack()
    source_entry = tk.Entry(root, width=30)
    source_entry.pack(pady=5)
    tk.Label(root, text="Destination Airport/City").pack()
    dest_entry = tk.Entry(root, width=30)
    dest_entry.pack(pady=5)
    tk.Label(root, text="Select Flight Date").pack()
    date_entry = Calendar(root, width=12, background="darkred", foreground="white", borderwidth=2, year=2025)
    date_entry.pack(pady=5)

    flights_data = []
    flight_listbox = tk.Listbox(root, width=100, height=10)
    flight_listbox.pack(pady=10)

    def search_flights():
        x = source_entry.get()
        s = dest_entry.get()
        flight_date = date_entry.selection_get()
        day_name = flight_date.strftime("%A")
        mycon_local = sql.connect(host="localhost", user="root", passwd="1234", database="flight_bookings")
        cursor_local = mycon_local.cursor()
        cursor_local.execute("SELECT * FROM flights WHERE departure_day='%s' AND source='%s' AND destination='%s'" % (day_name, x, s))
        flights_data.clear()
        for row in cursor_local.fetchall():
            flights_data.append(row)
        flight_listbox.delete(0, "end")
        for flight in flights_data:
            flight_listbox.insert("end", flight)

    def proceed():
        sel = flight_listbox.curselection()
        if not sel:
            messagebox.showwarning("Error", "No flight selected")
            return
        index = sel[0]
        flight = flights_data[index]
        seat_selection(passenger_id, flight[0], date_entry.selection_get())

    def back_to_login():
        login()

    tk.Button(root, text="Search Flights", command=search_flights).pack(pady=5)
    tk.Button(root, text="Select Flight", command=proceed).pack(pady=5)
    tk.Button(root, text="Back", command=back_to_login).pack(pady=5)

# ===================== SEAT SELECTION =====================
def seat_selection(passenger_id, flight_id, flight_date):
    clear_window(root)
    tk.Label(root, text="Select Seats for " + str(flight_id), font=("Arial", 18)).pack(pady=10)

    cursor.execute("SELECT seatno FROM bookings WHERE flight_id='%s' AND flight_date='%s'" % (flight_id, flight_date))
    booked = [r[0] for r in cursor.fetchall()]

    seat_frame = tk.Frame(root)
    seat_frame.pack(pady=10)
    chosen_seats = []

    def select_deselect_seat(seat, btn):
        if seat in chosen_seats:
            chosen_seats.remove(seat)
            btn.config(bg="lightgreen")
        else:
            chosen_seats.append(seat)
            btn.config(bg="yellow")

    def create_button(seat, row, col):
        color = "red" if seat in booked else "lightgreen"
        btn = tk.Button(seat_frame, text=seat, width=5, bg=color)
        if seat not in booked:
            def on_click():
                select_deselect_seat(seat, btn)
            btn.config(command=on_click)
        btn.grid(row=row, column=col, padx=5, pady=5)

    seats = ["A" + str(i) for i in range(1, 31)]
    row, col = 0, 0
    for seat in seats:
        create_button(seat, row, col)
        col += 1
        if col == 6:
            col = 0
            row += 1

    def confirm_booking():
        if not chosen_seats:
            messagebox.showwarning("Error", "No seats selected")
            return
        payment_window(passenger_id, flight_id, flight_date, chosen_seats)

    def go_back_home():
        home_page(passenger_id)

    tk.Button(root, text="Proceed to Payment", command=confirm_booking).pack(pady=10)
    tk.Button(root, text="Back", command=go_back_home).pack(pady=5)

# ===================== PAYMENT =====================
def payment_window(passenger_id, flight_id, flight_date, seat_list):
    clear_window(root)
    tk.Label(root, text="Choose Payment Method", font=("Arial", 18)).pack(pady=10)

    cursor.execute("SELECT rate FROM flights WHERE flight_id=%s", (flight_id,))
    rate_data = cursor.fetchone()
    seat_price = rate_data[0] if rate_data and rate_data[0] else 0
    total_price = seat_price * len(seat_list)

    tk.Label(root, text=f"Seat Price: Rs {seat_price}", font=("Arial", 12)).pack(pady=3)
    tk.Label(root, text=f"Seats Selected: {len(seat_list)}", font=("Arial", 12)).pack(pady=3)
    tk.Label(root, text=f"Total Amount: Rs {total_price}", font=("Arial", 14, "bold")).pack(pady=8)

    def process_booking_and_show_tickets():
        today = dt.today()
        booked_rows = []
        for seatno in seat_list:
            booking_id = rd.randint(10000, 99999)
            cursor.execute(
                """
                INSERT INTO bookings (booking_id, flight_id, passenger_id, name, source, destination, seatno, total_cost, date_of_booking, flight_date)
                SELECT %s, f.flight_id, %s, p.name, f.source, f.destination, %s, %s, %s, %s
                FROM flights f, passengers p
                WHERE f.flight_id=%s AND p.passenger_id=%s
                LIMIT 1
                """,
                (booking_id, passenger_id, seatno, total_price, today, flight_date, flight_id, passenger_id)
            )
            mycon.commit()
            cursor.execute("SELECT * FROM bookings WHERE booking_id=%s", (booking_id,))
            row = cursor.fetchone()
            if row:
                booked_rows.append(row)

        for row in booked_rows:
            show_ticket(row)
        messagebox.showinfo("Success", f"Booking Successful!\nTotal Cost: Rs {total_price}")
        home_page(passenger_id)

    # Cash payment
    def pay_cash():
        cash_window = tk.Toplevel(root)
        cash_window.title("Admin Confirmation")
        cash_window.geometry("360x180")
        tk.Label(cash_window, text="Waiting for Admin Confirmation...", font=("Arial", 14)).pack(pady=15)
        tk.Label(cash_window, text="Click OK once Admin confirms payment.", font=("Arial", 10)).pack(pady=5)

        def confirm_cash_payment():
            cash_window.destroy()
            process_booking_and_show_tickets()

        tk.Button(cash_window, text="OK", command=confirm_cash_payment, width=12).pack(pady=12)

    # Card payment
    def card_payment():
        clear_window(root)
        tk.Label(root, text="Enter Card Details", font=("Arial", 16)).pack(pady=10)
        tk.Label(root, text="Card Number").pack()
        card_num = tk.Entry(root, width=30)
        card_num.pack()
        tk.Label(root, text="Expiry Date (MM/YY)").pack()
        expiry = tk.Entry(root, width=30)
        expiry.pack()
        tk.Label(root, text="CVV").pack()
        cvv = tk.Entry(root, show="*", width=30)
        cvv.pack()

        def validate_and_pay():
            if not card_num.get().isdigit() or len(card_num.get()) not in [12, 16]:
                messagebox.showwarning("Error", "Invalid Card Number")
                return
            if len(expiry.get()) < 4:
                messagebox.showwarning("Error", "Invalid Expiry Date")
                return
            if not cvv.get().isdigit() or len(cvv.get()) != 3:
                messagebox.showwarning("Error", "Invalid CVV")
                return
            process_booking_and_show_tickets()

        def back_to_payment():
            payment_window(passenger_id, flight_id, flight_date, seat_list)

        tk.Button(root, text="Confirm Payment", command=validate_and_pay, width=20).pack(pady=20)
        tk.Button(root, text="Back", command=back_to_payment).pack(pady=5)

    def back_to_seats():
        seat_selection(passenger_id, flight_id, flight_date)

    tk.Button(root, text="Pay with Cash", command=pay_cash, width=20).pack(pady=5)
    tk.Button(root, text="Pay with Card", command=card_payment, width=20).pack(pady=5)
    tk.Button(root, text="Back", command=back_to_seats).pack(pady=5)

# ===================== FLIGHT EDIT =====================
def flight_edit():
    clear_window(root)
    tk.Label(root, text="Choose the field you want to edit").pack()
    flightvar = tk.StringVar()
    tk.OptionMenu(root, flightvar, "DEPARTURE_TIME", "ARRIVAL_TIME", "status", "rate").pack()
    tk.Label(root, text="enter the flight id").pack()
    bx11 = tk.Entry(root, width=30)
    bx11.pack()
    tk.Label(root, text="enter the new record").pack()
    bx12 = tk.Entry(root, width=30)
    bx12.pack()

    def updation():
        selection = flightvar.get()
        flight_id = bx11.get()
        input2 = bx12.get()
        mycon_local = sql.connect(host="localhost", user="root", passwd="1234", database="flight_bookings")
        cursor_local = mycon_local.cursor()
        query = "UPDATE flights SET %s='%s' WHERE flight_id='%s'" % (selection, input2, flight_id)
        cursor_local.execute(query)
        mycon_local.commit()
        messagebox.showinfo("Success", "Flight details updated successfully!")

    tk.Button(root, text="OK", command=updation).pack(pady=5)
    tk.Button(root, text="Back", command=login_window).pack(pady=5)

# ===================== START =====================
admin_login_window()
root.mainloop()
