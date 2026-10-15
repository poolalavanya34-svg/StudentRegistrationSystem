import csv
from datetime import datetime
import json
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# File to store student records locally
DATA_FILE = "students.json"


def load_data():
  """Load student records from the JSON file."""
  if not os.path.exists(DATA_FILE):
    return []
  try:
    with open(DATA_FILE, "r") as file:
      return json.load(file)
  except json.JSONDecodeError:
    return []


def save_data(data):
  """Save student records to the JSON file."""
  with open(DATA_FILE, "w") as file:
    json.dump(data, file, indent=4)


class StudentApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Student Registration System")
    self.root.geometry("1100x680")

    self.is_dark = False
    self.bg_color = "#eef2f6"

    self.container = tk.Frame(root, bg=self.bg_color)
    self.container.pack(fill=tk.BOTH, expand=True)

    self.frames = {}

    for F in (RegistrationScreen, DashboardScreen):
      page_name = F.__name__
      frame = F(parent=self.container, controller=self)
      self.frames[page_name] = frame
      frame.grid(row=0, column=0, sticky="nsew")

    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

    self.show_frame("RegistrationScreen")

  def show_frame(self, page_name):
    frame = self.frames[page_name]
    if page_name == "DashboardScreen":
      frame.load_table()
    frame.tkraise()


class RegistrationScreen(tk.Frame):

  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    self.config(bg="#e2e8f0")

    # Vibrant Header
    header = tk.Frame(self, bg="#0f172a", pady=15)
    header.pack(fill=tk.X)

    title_label = tk.Label(
        header,
        text="🎓 STUDENT REGISTRATION PORTAL",
        font=("Segoe UI", 18, "bold"),
        bg="#0f172a",
        fg="#38bdf8",
    )
    title_label.pack()

    subtitle = tk.Label(
        header,
        text="Fill in the details below to enroll a new student",
        font=("Segoe UI", 9),
        bg="#0f172a",
        fg="#94a3b8",
    )
    subtitle.pack(pady=(2, 0))

    # Main Card
    card = tk.Frame(self, bg="#ffffff", bd=2, relief="groove", padx=30, pady=20)
    card.pack(padx=40, pady=25, fill=tk.BOTH, expand=True)

    card_title = tk.Label(
        card,
        text="Enter Student Information",
        font=("Segoe UI", 14, "bold"),
        bg="#ffffff",
        fg="#1e293b",
    )
    card_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

    # Input Variables (Blank default values)
    self.id_var = tk.StringVar()
    self.name_var = tk.StringVar()
    self.dob_var = tk.StringVar()
    self.gender_var = tk.StringVar(value="Male")
    self.email_var = tk.StringVar()
    self.phone_var = tk.StringVar()
    self.course_var = tk.StringVar()
    self.year_var = tk.StringVar(value="1st Year")
    self.address_var = tk.StringVar()

    # Column 1 Fields
    col1_fields = [
        ("Student ID:", self.id_var),
        ("Full Name:", self.name_var),
        ("Date of Birth (DD-MM-YYYY):", self.dob_var),
        ("Email Address:", self.email_var),
    ]

    r = 1
    for label_text, var in col1_fields:
      lbl = tk.Label(
          card,
          text=label_text,
          font=("Segoe UI", 10, "bold"),
          bg="#ffffff",
          fg="#334155",
      )
      lbl.grid(row=r, column=0, sticky="w", pady=(8, 2))
      ent = tk.Entry(
          card,
          textvariable=var,
          font=("Segoe UI", 10),
          width=35,
          bd=1,
          relief="solid",
          bg="#f8fafc",
      )
      ent.grid(row=r + 1, column=0, sticky="w", pady=(0, 8), padx=(0, 20))
      r += 2

    # Column 2 Fields
    col2_fields = [
        ("Phone Number:", self.phone_var),
        ("Course:", self.course_var),
        ("Address:", self.address_var),
    ]

    r2 = 1
    for label_text, var in col2_fields:
      lbl = tk.Label(
          card,
          text=label_text,
          font=("Segoe UI", 10, "bold"),
          bg="#ffffff",
          fg="#334155",
      )
      lbl.grid(row=r2, column=1, sticky="w", pady=(8, 2))
      ent = tk.Entry(
          card,
          textvariable=var,
          font=("Segoe UI", 10),
          width=35,
          bd=1,
          relief="solid",
          bg="#f8fafc",
      )
      ent.grid(row=r2 + 1, column=1, sticky="w", pady=(0, 8))
      r2 += 2

    # Gender & Year in Column 2
    lbl_gender = tk.Label(
        card,
        text="Gender:",
        font=("Segoe UI", 10, "bold"),
        bg="#ffffff",
        fg="#334155",
    )
    lbl_gender.grid(row=r2, column=1, sticky="w", pady=(8, 2))

    g_frame = tk.Frame(card, bg="#ffffff")
    g_frame.grid(row=r2 + 1, column=1, sticky="w", pady=(0, 8))
    tk.Radiobutton(
        g_frame,
        text="Male",
        variable=self.gender_var,
        value="Male",
        bg="#ffffff",
        fg="#0f172a",
        font=("Segoe UI", 9, "bold"),
    ).pack(side=tk.LEFT, padx=(0, 10))
    tk.Radiobutton(
        g_frame,
        text="Female",
        variable=self.gender_var,
        value="Female",
        bg="#ffffff",
        fg="#0f172a",
        font=("Segoe UI", 9, "bold"),
    ).pack(side=tk.LEFT)

    # Year of Study
    lbl_year = tk.Label(
        card,
        text="Year of Study:",
        font=("Segoe UI", 10, "bold"),
        bg="#ffffff",
        fg="#334155",
    )
    lbl_year.grid(row=r, column=0, sticky="w", pady=(8, 2))

    year_combo = ttk.Combobox(
        card,
        textvariable=self.year_var,
        values=["1st Year", "2nd Year", "3rd Year", "4th Year"],
        state="readonly",
        width=33,
        font=("Segoe UI", 10),
    )
    year_combo.grid(row=r + 1, column=0, sticky="w", pady=(0, 8), padx=(0, 20))

    # Action Buttons Bar
    btn_frame = tk.Frame(card, bg="#ffffff")
    btn_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(25, 0))

    tk.Button(
        btn_frame,
        text="✨ Register Student",
        command=self.register_student,
        bg="#16a34a",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8,
        bd=0,
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=(0, 10))
    tk.Button(
        btn_frame,
        text="🔄 Clear Form",
        command=self.clear_form,
        bg="#64748b",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8,
        bd=0,
        cursor="hand2",
    ).pack(side=tk.LEFT)
    tk.Button(
        btn_frame,
        text="📋 View Records Dashboard ➔",
        command=lambda: controller.show_frame("DashboardScreen"),
        bg="#2563eb",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=8,
        bd=0,
        cursor="hand2",
    ).pack(side=tk.RIGHT)

  def validate_inputs(self):
    sid = self.id_var.get().strip()
    name = self.name_var.get().strip()
    dob = self.dob_var.get().strip()
    email = self.email_var.get().strip()
    phone = self.phone_var.get().strip()
    course = self.course_var.get().strip()
    address = self.address_var.get().strip()

    if not all([sid, name, dob, email, phone, course, address]):
      messagebox.showerror("Validation Error", "All fields must be filled!")
      return False

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
      messagebox.showerror("Validation Error", "Invalid email format!")
      return False

    if not phone.isdigit() or len(phone) != 10:
      messagebox.showerror(
          "Validation Error", "Phone number must be exactly 10 digits!"
      )
      return False

    for s in load_data():
      if s["ID"] == sid:
        messagebox.showerror("Error", f"Student with ID '{sid}' already exists!")
        return False
    return True

  def register_student(self):
    if not self.validate_inputs():
      return

    new_student = {
        "ID": self.id_var.get().strip(),
        "Name": self.name_var.get().strip(),
        "DOB": self.dob_var.get().strip(),
        "Gender": self.gender_var.get(),
        "Email": self.email_var.get().strip(),
        "Phone": self.phone_var.get().strip(),
        "Course": self.course_var.get().strip(),
        "Year": self.year_var.get(),
        "Address": self.address_var.get().strip(),
    }

    students = load_data()
    students.append(new_student)
    save_data(students)
    messagebox.showinfo("Success", "Student registered successfully!")
    self.clear_form()

  def clear_form(self):
    self.id_var.set("")
    self.name_var.set("")
    self.dob_var.set("")
    self.gender_var.set("Male")
    self.email_var.set("")
    self.phone_var.set("")
    self.course_var.set("")
    self.year_var.set("1st Year")
    self.address_var.set("")


class DashboardScreen(tk.Frame):

  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    self.config(bg="#f1f5f9")

    # Header Title & Navigation Back
    header_frame = tk.Frame(self, bg="#0f172a", pady=12)
    header_frame.pack(fill=tk.X)

    tk.Button(
        header_frame,
        text="⬅ Back to Registration",
        command=lambda: controller.show_frame("RegistrationScreen"),
        bg="#334155",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        padx=10,
        pady=4,
        bd=0,
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=15)
    tk.Label(
        header_frame,
        text="📊 STUDENT RECORDS DASHBOARD",
        font=("Segoe UI", 15, "bold"),
        bg="#0f172a",
        fg="#38bdf8",
    ).pack(side=tk.LEFT, padx=20)

    # Main Dashboard Body
    body = tk.Frame(self, bg="#f1f5f9", padx=15, pady=15)
    body.pack(fill=tk.BOTH, expand=True)

    # Toolbar
    toolbar = tk.LabelFrame(
        body,
        text=" Management Tools ",
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
        padx=10,
        pady=8,
    )
    toolbar.pack(fill=tk.X, pady=(0, 10))

    self.search_var = tk.StringVar()
    tk.Label(
        toolbar,
        text="Search:",
        font=("Segoe UI", 9, "bold"),
        bg="#ffffff",
        fg="#334155",
    ).pack(side=tk.LEFT, padx=2)
    tk.Entry(
        toolbar,
        textvariable=self.search_var,
        font=("Segoe UI", 9),
        width=12,
        bd=1,
        relief="solid",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Find",
        command=self.search_student,
        bg="#0284c7",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)

    tk.Button(
        toolbar,
        text="Reset",
        command=self.load_table,
        bg="#64748b",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Sort A-Z",
        command=self.sort_students,
        bg="#8b5cf6",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="ID Card",
        command=self.generate_id_card,
        bg="#0ea5e9",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Receipt",
        command=self.export_receipt,
        bg="#ec4899",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Age",
        command=self.calculate_age,
        bg="#6366f1",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Demo",
        command=self.load_demo_data,
        bg="#14b8a6",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Export CSV",
        command=self.export_to_csv,
        bg="#10b981",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Analytics",
        command=self.show_analytics,
        bg="#f59e0b",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Delete",
        command=self.delete_student,
        bg="#ef4444",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)
    tk.Button(
        toolbar,
        text="Clear DB",
        command=self.clear_all_records,
        bg="#991b1b",
        fg="white",
        font=("Segoe UI", 8, "bold"),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=2)

    self.count_label = tk.Label(
        toolbar,
        text="Total: 0",
        font=("Segoe UI", 10, "bold"),
        bg="#ffffff",
        fg="#0284c7",
    )
    self.count_label.pack(side=tk.RIGHT, padx=5)

    # Table Container
    table_frame = tk.Frame(body, bg="#ffffff")
    table_frame.pack(fill=tk.BOTH, expand=True)

    tree_scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
    tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

    self.tree = ttk.Treeview(
        table_frame,
        columns=(
            "ID",
            "Name",
            "DOB",
            "Gender",
            "Email",
            "Phone",
            "Course",
            "Year",
            "Address",
        ),
        show="headings",
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set,
    )

    tree_scroll_y.config(command=self.tree.yview)
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_scroll_x.config(command=self.tree.xview)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    self.tree.pack(fill=tk.BOTH, expand=True)

    columns_config = [
        ("ID", 70),
        ("Name", 120),
        ("DOB", 90),
        ("Gender", 70),
        ("Email", 150),
        ("Phone", 90),
        ("Course", 100),
        ("Year", 80),
        ("Address", 130),
    ]

    for col, width in columns_config:
      self.tree.heading(col, text=col)
      self.tree.column(col, width=width, anchor=tk.W)

    self.load_table()

  def load_table(self, data=None):
    for row in self.tree.get_children():
      self.tree.delete(row)

    students = data if data is not None else load_data()
    for s in students:
      self.tree.insert(
          "",
          tk.END,
          values=(
              s["ID"],
              s["Name"],
              s["DOB"],
              s["Gender"],
              s["Email"],
              s["Phone"],
              s["Course"],
              s["Year"],
              s["Address"],
          ),
      )
    self.count_label.config(text=f"Total: {len(load_data())}")

  def search_student(self):
    query = self.search_var.get().strip().lower()
    if not query:
      messagebox.showwarning("Warning", "Enter ID or Name to search!")
      return
    students = load_data()
    filtered = [
        s
        for s in students
        if query in s["ID"].lower() or query in s["Name"].lower()
    ]
    if not filtered:
      messagebox.showinfo("Not Found", "No records found!")
      return
    self.load_table(filtered)

  def sort_students(self):
    students = load_data()
    if not students:
      messagebox.showwarning("Warning", "No records to sort!")
      return
    self.load_table(sorted(students, key=lambda s: s["Name"].lower()))

  def delete_student(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning(
          "Warning", "Select a student record from the table to delete!"
      )
      return
    if messagebox.askyesno(
        "Confirm Delete", "Are you sure you want to delete this record?"
    ):
      row_data = self.tree.item(selected[0])["values"]
      sid = str(row_data[0])
      students = [s for s in load_data() if s["ID"] != sid]
      save_data(students)
      self.load_table()
      messagebox.showinfo("Success", "Record deleted successfully!")

  def generate_id_card(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning("Warning", "Select a student from the table!")
      return
    r = self.tree.item(selected[0])["values"]
    win = tk.Toplevel(self.controller)
    win.title(f"ID Card - {r[1]}")
    win.geometry("380x250")
    win.config(bg="#ffffff")
    tk.Label(
        win,
        text="UNIVERSITY STUDENT ID",
        font=("Segoe UI", 12, "bold"),
        bg="#0f172a",
        fg="white",
        pady=8,
    ).pack(fill=tk.X)
    f = tk.Frame(win, bg="#ffffff", padx=15, pady=10)
    f.pack(fill=tk.BOTH, expand=True)
    for label, val in [
        ("Student ID:", r[0]),
        ("Full Name:", r[1]),
        ("Course:", r[6]),
        ("Year:", r[7]),
        ("Phone:", r[5]),
        ("Address:", r[8]),
    ]:
      rf = tk.Frame(f, bg="#ffffff")
      rf.pack(fill=tk.X, anchor="w", pady=2)
      tk.Label(
          rf,
          text=label,
          font=("Segoe UI", 9, "bold"),
          width=12,
          anchor="w",
          bg="#ffffff",
          fg="#475569",
      ).pack(side=tk.LEFT)
      tk.Label(
          rf,
          text=str(val),
          font=("Segoe UI", 9),
          anchor="w",
          bg="#ffffff",
          fg="#0f172a",
      ).pack(side=tk.LEFT)

  def export_receipt(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning("Warning", "Select a student to export receipt!")
      return
    r = self.tree.item(selected[0])["values"]
    path = filedialog.asksaveasfilename(
        defaultextension=".txt", initialfile=f"Receipt_{r[0]}.txt"
    )
    if path:
      with open(path, "w", encoding="utf-8") as f:
        f.write(
            f"=== RECEIPT ===\nID: {r[0]}\nName: {r[1]}\nCourse: {r[6]}\nYear:"
            f" {r[7]}\nStatus: VERIFIED\n"
        )
      messagebox.showinfo("Success", f"Receipt saved to:\n{path}")

  def calculate_age(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning("Warning", "Select a student to calculate age!")
      return
    r = self.tree.item(selected[0])["values"]
    try:
      dob = datetime.strptime(r[2], "%d-%m-%Y")
      today = datetime.today()
      age = (
          today.year
          - dob.year
          - ((today.month, today.day) < (dob.month, dob.day))
      )
      messagebox.showinfo(
          "Age Calculator", f"Student: {r[1]}\nAge: {age} years old"
      )
    except ValueError:
      messagebox.showerror(
          "Error", "Invalid DOB format (DD-MM-YYYY required)."
      )

  def load_demo_data(self):
    demo = [
        {
            "ID": "101",
            "Name": "Rahul Sharma",
            "DOB": "12-05-2004",
            "Gender": "Male",
            "Email": "rahul@gmail.com",
            "Phone": "9876543210",
            "Course": "B.Tech CSE",
            "Year": "2nd Year",
            "Address": "Delhi",
        },
        {
            "ID": "102",
            "Name": "Priya Verma",
            "DOB": "20-08-2003",
            "Gender": "Female",
            "Email": "priya@gmail.com",
            "Phone": "9123456789",
            "Course": "B.Sc IT",
            "Year": "3rd Year",
            "Address": "Mumbai",
        },
    ]
    students = load_data()
    ids = {s["ID"] for s in students}
    added = 0
    for d in demo:
      if d["ID"] not in ids:
        students.append(d)
        added += 1
    save_data(students)
    self.load_table()
    messagebox.showinfo("Demo", f"Loaded {added} sample records!")

  def clear_all_records(self):
    if messagebox.askyesno("Warning", "Delete ALL records?"):
      save_data([])
      self.load_table()
      messagebox.showinfo("Cleared", "Database wiped successfully.")

  def show_analytics(self):
    students = load_data()
    if not students:
      messagebox.showwarning("Analytics", "No records found!")
      return
    total = len(students)
    years = {"1st Year": 0, "2nd Year": 0, "3rd Year": 0, "4th Year": 0}
    for s in students:
      y = s.get("Year", "1st Year")
      if y in years:
        years[y] += 1
    report = f"Total Students: {total}\n\nBreakdown by Year:\n"
    for y, count in years.items():
      report += f" • {y}: {count}\n"
    messagebox.showinfo("Analytics", report)

  def export_to_csv(self):
    students = load_data()
    if not students:
      messagebox.showwarning("Warning", "No data to export!")
      return
    path = filedialog.asksaveasfilename(defaultextension=".csv")
    if path:
      with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID",
            "Name",
            "DOB",
            "Gender",
            "Email",
            "Phone",
            "Course",
            "Year",
            "Address",
        ])
        for s in students:
          writer.writerow([
              s["ID"],
              s["Name"],
              s["DOB"],
              s["Gender"],
              s["Email"],
              s["Phone"],
              s["Course"],
              s["Year"],
              s["Address"],
          ])
      messagebox.showinfo("Success", f"Exported successfully to:\n{path}")


if __name__ == "__main__":
  root = tk.Tk()
  app = StudentApp(root)
  root.mainloop()