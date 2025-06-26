import tkinter as tk
from tkinter import messagebox, ttk
import datetime

class EduMateAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EduMate AI: Smart Study Schedule Generator")
        self.root.geometry("700x750")
        self.root.configure(bg="#f8f8f8")

        self.subject_entries = []
        self.exam_date_entries = []
        self.chapters_entries = []
        self.priority_entries = []

        title_label = tk.Label(root, text="📚 EduMate AI: Study Planner with Smart Suggestions",
                               font=("Helvetica", 20, "bold"), bg="#f8f8f8", fg="#333")
        title_label.pack(pady=20)

        frame = tk.Frame(root, bg="#f8f8f8")
        frame.pack(pady=10)

        headers = ["Subject", "Exam Date (dd-mm-yyyy)", "Chapters Left"]
        for col, h in enumerate(headers):
            tk.Label(frame, text=h, font=("Helvetica", 12, "bold"), bg="#f8f8f8").grid(row=0, column=col, padx=10)

        self.add_subject_row(frame)

        tk.Button(root, text="➕ Add Subject", bg="#4CAF50", fg="white", font=("Helvetica", 11),
                  command=lambda: self.add_subject_row(frame)).pack(pady=8)

        tk.Label(root, text="Available Study Hours per Day:", bg="#f8f8f8", font=("Helvetica", 12)).pack(pady=5)
        self.hours_entry = tk.Entry(root, font=("Helvetica", 12), width=5)
        self.hours_entry.pack(pady=5)

        tk.Button(root, text="📊 Generate AI Schedule", font=("Helvetica", 14), bg="#2196F3", fg="white",
                  command=self.generate_schedule).pack(pady=10)

        self.result_text = tk.Text(root, height=15, width=75, font=("Consolas", 11), wrap=tk.WORD, bg="#ffffff")
        self.result_text.pack(pady=10)

    def add_subject_row(self, frame):
        row = len(self.subject_entries) + 1

        subject_entry = tk.Entry(frame, font=("Helvetica", 11), width=15)
        subject_entry.grid(row=row, column=0, padx=5, pady=5)
        self.subject_entries.append(subject_entry)

        exam_date_entry = tk.Entry(frame, font=("Helvetica", 11), width=15)
        exam_date_entry.grid(row=row, column=1, padx=5, pady=5)
        self.exam_date_entries.append(exam_date_entry)

        chapters_entry = tk.Entry(frame, font=("Helvetica", 11), width=8)
        chapters_entry.grid(row=row, column=2, padx=5, pady=5)
        self.chapters_entries.append(chapters_entry)

    def generate_schedule(self):
        subjects = [e.get() for e in self.subject_entries if e.get().strip() != ""]
        exams = [e.get() for e in self.exam_date_entries]
        chapters = [e.get() for e in self.chapters_entries]

        if not subjects:
            messagebox.showerror("Input Error", "Please add at least one subject.")
            return

        try:
            total_hours = float(self.hours_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid study hours.")
            return

        # AI Priority Calculation based on exam date proximity and chapters left
        priorities = []
        today = datetime.date.today()

        for i in range(len(subjects)):
            try:
                exam_date = datetime.datetime.strptime(exams[i], "%d-%m-%Y").date()
                days_left = (exam_date - today).days
                chapters_left = int(chapters[i])

                if days_left <= 3:
                    priority = 10
                elif days_left <= 7:
                    priority = 8
                elif chapters_left >= 10:
                    priority = 7
                elif days_left <= 14:
                    priority = 6
                else:
                    priority = 5
            except:
                priority = 5  # default

            priorities.append(priority)

        total_priority = sum(priorities)
        schedule = []
        tips = []

        for i in range(len(subjects)):
            allocated_hours = round((priorities[i] / total_priority) * total_hours, 2)
            schedule.append(f"{subjects[i]}: {allocated_hours} hrs (Priority: {priorities[i]})")

            # Smart AI tips
            if priorities[i] >= 9:
                tips.append(f"📌 Focus on {subjects[i]} — Exam soon!")
            elif priorities[i] <= 5 and allocated_hours < 1:
                tips.append(f"⚠ Consider giving more time to {subjects[i]}.")

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "📝 Your AI-Generated Study Schedule:\n\n")
        for line in schedule:
            self.result_text.insert(tk.END, f"{line}\n")

        self.result_text.insert(tk.END, "\n💡 AI Suggestions:\n")
        for tip in tips:
            self.result_text.insert(tk.END, f"{tip}\n")

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = EduMateAIApp(root)
    root.mainloop()