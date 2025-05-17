import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Data
students = {}
attendance = defaultdict(list)
grades = {}

# App Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("900x600")

# Background image
bg_img = Image.open("school_bg.png")
bg_img = bg_img.resize((900, 600))
bg_photo = ImageTk.PhotoImage(bg_img)

# Container for all pages
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Function to switch frames
def show_frame(page):
    frame = pages[page]
    frame.tkraise()

# Base class for all pages
class BasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.bg_label = tk.Label(self, image=bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Page 1: Add Student ---
class AddStudentPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Add Student Details", font=("Arial", 18, "bold"), bg="white").place(relx=0.5, rely=0.1, anchor="center")
        
        form_frame = tk.Frame(self, bg="white")
        form_frame.place(relx=0.5, rely=0.3, anchor="center")

        tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Roll No:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5)
        self.roll_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.roll_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Grade (%):", font=("Arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=5)
        self.grade_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.grade_entry.grid(row=2, column=1)

        tk.Button(self, text="Add Student", font=("Arial", 12, "bold"), command=self.add_student).place(relx=0.5, rely=0.5, anchor="center")

    def add_student(self):
        name = self.name_entry.get()
        roll = self.roll_entry.get()
        grade = self.grade_entry.get()
        if name and roll:
            students[roll] = name
            grades[roll] = int(grade)
            messagebox.showinfo("Success", f"{name} added!")
        else:
            messagebox.showwarning("Missing Info", "Name and Roll No required.")

# --- Page 2: Attendance ---
class AttendancePage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Mark Attendance", font=("Arial", 18, "bold"), bg="white").place(relx=0.5, rely=0.2, anchor="center")
        
        self.roll_entry = tk.Entry(self, font=("Arial", 12))
        self.roll_entry.place(relx=0.5, rely=0.3, anchor="center")

        tk.Button(self, text="Mark Attendance", font=("Arial", 12, "bold"), command=self.mark_attendance).place(relx=0.5, rely=0.4, anchor="center")

    def mark_attendance(self):
        roll = self.roll_entry.get()
        if roll in students:
            today = datetime.now().strftime("%Y-%m-%d")
            attendance[roll].append(today)
            messagebox.showinfo("Success", f"Attendance marked for {students[roll]}")
        else:
            messagebox.showerror("Error", "Student not found")

# --- Page 3: Records and Export ---
class RecordsPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Student Records", font=("Arial", 18, "bold"), bg="white").place(relx=0.5, rely=0.1, anchor="center")

        self.text = tk.Text(self, wrap="word", font=("Arial", 10))
        self.text.place(relx=0.5, rely=0.45, anchor="center", width=700, height=300)

        tk.Button(self, text="Show Records", font=("Arial", 12), command=self.show_records).place(relx=0.3, rely=0.85, anchor="center")
        tk.Button(self, text="Export to Excel", font=("Arial", 12), command=self.export).place(relx=0.7, rely=0.85, anchor="center")

    def show_records(self):
        self.text.delete("1.0", tk.END)
        for roll, name in students.items():
            grade = grades.get(roll, "N/A")
            self.text.insert(tk.END, f"Name: {name}, Roll: {roll}, Grade: {grade}\n")
            self.text.insert(tk.END, f"Attendance: {attendance[roll]}\n\n")

    def export(self):
        df = pd.DataFrame([
            {"Roll No": roll, "Name": students[roll], "Grade": grades[roll], "Attendance Days": len(set(attendance[roll]))}
            for roll in students
        ])
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file:
            df.to_excel(file, index=False)
            messagebox.showinfo("Exported", "Data saved to Excel.")

# --- Page 4: Grade & Attendance Progress ---
class ProgressPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Student Progress", font=("Arial", 18, "bold"), bg="white").place(relx=0.5, rely=0.2, anchor="center")
        tk.Button(self, text="Show Progress Chart", font=("Arial", 12), command=self.show_graph).place(relx=0.5, rely=0.3, anchor="center")

    def show_graph(self):
        rolls = list(students.keys())
        names = [students[r] for r in rolls]
        grades_list = [grades.get(r, 0) for r in rolls]
        att_list = [len(set(attendance[r])) for r in rolls]

        fig, ax = plt.subplots()
        bar1 = ax.barh(names, grades_list, label="Grade (%)", color='skyblue')
        ax.barh(names, att_list, left=grades_list, label="Attendance", color='orange')
        ax.set_xlabel("Performance")
        ax.set_title("Grade and Attendance Progress")
        ax.legend()
        plt.tight_layout()
        plt.show()

# Create all pages
pages = {}
for PageClass in (AddStudentPage, AttendancePage, RecordsPage, ProgressPage):
    page = PageClass(container)
    pages[PageClass] = page
    page.place(relx=0, rely=0, relwidth=1, relheight=1)

# Navigation Buttons
nav_frame = tk.Frame(root, bg="lightgray")
nav_frame.place(relx=0, rely=0, relwidth=1)

tk.Button(nav_frame, text="Add Student", command=lambda: show_frame(AddStudentPage), font=("Arial", 10)).pack(side="left", padx=10, pady=5)
tk.Button(nav_frame, text="Attendance", command=lambda: show_frame(AttendancePage), font=("Arial", 10)).pack(side="left", padx=10, pady=5)
tk.Button(nav_frame, text="Records/Export", command=lambda: show_frame(RecordsPage), font=("Arial", 10)).pack(side="left", padx=10, pady=5)
tk.Button(nav_frame, text="Progress", command=lambda: show_frame(ProgressPage), font=("Arial", 10)).pack(side="left", padx=10, pady=5)

# Show default page
show_frame(AddStudentPage)

root.mainloop()
