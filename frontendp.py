from tkinter import *
from tkinter import messagebox, ttk
import dbbackend  # keep your existing database module

class StudentUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database Management System")
        self.root.geometry("1280x720")
        self.root.configure(bg="#f7fbff")

        # ================ THEME / COLORS ================
        self.palette = {
            "sidebar_bg": "#0f172a",   # deep navy
            "accent1": "#06b6d4",      # cyan
            "accent2": "#f97316",      # orange
            "accent3": "#8b5cf6",      # purple
            "card_bg": "#ffffff",
            "muted": "#6b7280",        # text-muted
            "form_bg": "#eef2ff",
            "entry_focus": "#a78bfa",  # lilac
            "row_alt": "#f8fafc",
            "row_main": "#ffffff"
        }

        # ================= VARIABLES =================
        self.StdID = StringVar()
        self.Firstname = StringVar()
        self.Surname = StringVar()
        self.DoB = StringVar()
        self.Age = StringVar()
        self.Gender = StringVar()
        self.Address = StringVar()
        self.Mobile = StringVar()

        # ================= SIDEBAR =================
        sidebar = Frame(self.root, bg=self.palette["sidebar_bg"], width=260)
        sidebar.pack(side=LEFT, fill=Y)

        # Logo / title
        logo_frame = Frame(sidebar, bg=self.palette["sidebar_bg"])
        logo_frame.pack(pady=28)
        Label(logo_frame, text="🎓 Student DB", fg="white", bg=self.palette["sidebar_bg"],
              font=('Segoe UI Black', 22, 'bold')).pack()

        # Sidebar buttons (with hover)
        buttons = [
            ("➕ Add", self.addData, self.palette["accent1"]),
            ("📋 View All", self.openDisplayWindow, self.palette["accent3"]),
            ("🧹 Clear", self.clearData, "#f59e0b"),
            ("❌ Delete", self.DeleteData, "#ef4444"),
            ("🔍 Search", self.searchDatabase, "#06b6d4"),
            ("♻ Update", self.update, "#0ea5a4"),
            ("🚪 Exit", self.iExit, "#ef476f"),
        ]

        for (text, command, color) in buttons:
            btn = Label(sidebar, text=text, bg=self.palette["sidebar_bg"], fg="white",
                        font=('Segoe UI Semibold', 13), bd=0, relief=FLAT, padx=12, pady=10, cursor="hand2")
            btn.pack(fill=X, pady=8, padx=12)
            # create a pill-like colored left accent bar using a frame
            accent = Frame(btn, bg=color, width=8)
            accent.place(x=0, y=0, relheight=1)

            # Hover effects
            def on_enter(e, b=btn, c=color):
                b.configure(bg=c, fg="white")
            def on_leave(e, b=btn):
                b.configure(bg=self.palette["sidebar_bg"], fg="white")
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.bind("<Button-1>", lambda e, cmd=command: cmd())

        # ================= MAIN FORM =================
        main_frame = Frame(self.root, bg=self.palette["card_bg"], bd=0)
        main_frame.pack(fill=BOTH, expand=True, padx=16, pady=16)

        # Header / hero
        header = Frame(main_frame, bg=self.palette["accent1"], height=90)
        header.pack(fill=X, padx=6, pady=(6, 12))
        header.pack_propagate(False)
        Label(header, text="Student Information Form", bg=self.palette["accent1"], fg="white",
              font=('Segoe UI Black', 24, 'bold')).pack(side=LEFT, padx=20, pady=16)
        Label(header, text="🌟 Add • Manage • Explore", bg=self.palette["accent1"], fg="white",
              font=('Segoe UI Semibold', 12)).pack(side=RIGHT, padx=20)

        # Form container
        form_frame = Frame(main_frame, bg=self.palette["form_bg"], bd=0, relief=FLAT)
        form_frame.pack(pady=8, padx=12, fill=X)

        labels = ["Student ID", "Firstname", "Surname", "Date of Birth",
                  "Age", "Gender", "Address", "Mobile"]
        variables = [self.StdID, self.Firstname, self.Surname, self.DoB,
                     self.Age, self.Gender, self.Address, self.Mobile]
        self.entries = []

        # grid layout: two columns of fields to shorten the vertical space
        for i, (label, var) in enumerate(zip(labels, variables)):
            r = i // 2
            c = (i % 2) * 2  # 0 or 2 so we can leave column 1 as label, column 2 entry
            Label(form_frame, text=label + ":", bg=self.palette["form_bg"], fg=self.palette["muted"],
                  font=('Segoe UI Semibold', 12)).grid(row=r, column=c, sticky=W, padx=12, pady=12)

            entry = Entry(form_frame, textvariable=var, font=('Segoe UI', 12),
                          width=28, bd=2, relief=GROOVE, highlightthickness=2, highlightbackground="#e6edf3")
            entry.grid(row=r, column=c+1, padx=(0,16), pady=12, sticky=W)
            # focus highlight
            entry.bind("<FocusIn>", lambda e, w=entry: w.config(highlightbackground=self.palette["entry_focus"]))
            entry.bind("<FocusOut>", lambda e, w=entry: w.config(highlightbackground="#e6edf3"))
            self.entries.append(entry)

        # Action row under form
        action_frame = Frame(main_frame, bg=self.palette["card_bg"])
        action_frame.pack(fill=X, padx=12, pady=10)

        def make_action_button(parent, text, cmd, bg):
            b = Button(parent, text=text, command=cmd, bg=bg, fg="white",
                       font=('Segoe UI Semibold', 12), bd=0, relief=FLAT, padx=14, pady=8, cursor="hand2")
            b.pack(side=LEFT, padx=8)
            # hover
            b.bind("<Enter>", lambda e, btn=b, c=bg: btn.config(bg=self._darker(c)))
            b.bind("<Leave>", lambda e, btn=b, c=bg: btn.config(bg=c))
            return b

        make_action_button(action_frame, "➕ Add", self.addData, self.palette["accent1"])
        make_action_button(action_frame, "🔍 Search", self.searchDatabase, self.palette["accent3"])
        make_action_button(action_frame, "🧹 Clear", self.clearData, "#f59e0b")
        make_action_button(action_frame, "❌ Delete", self.DeleteData, "#ef4444")
        make_action_button(action_frame, "♻ Update", self.update, "#0ea5a4")

        # status / footer
        footer = Frame(main_frame, bg=self.palette["card_bg"])
        footer.pack(fill=X, padx=12, pady=(6, 12))
        Label(footer, text="Made with ❤️ in Python — vibrant UI by your friendly assistant ✨",
              bg=self.palette["card_bg"], fg=self.palette["muted"], font=('Segoe UI', 10)).pack(side=LEFT, padx=6)

    # small helper to darken a hex color for hover effect
    def _darker(self, hex_color, factor=0.9):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    # ================= FUNCTION DEFINITIONS =================
    def iExit(self):
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.root.destroy()

    def clearData(self):
        for e in self.entries:
            e.delete(0, END)

    def addData(self):
        if len(self.StdID.get()) != 0:
            dbbackend.addStdRec(
                self.StdID.get(), self.Firstname.get(), self.Surname.get(),
                self.DoB.get(), self.Age.get(), self.Gender.get(),
                self.Address.get(), self.Mobile.get()
            )
            messagebox.showinfo("Success", "Record added successfully!")

    def DeleteData(self):
        if len(self.StdID.get()) != 0:
            all_records = dbbackend.viewData()
            found = False
            for row in all_records:
                if row[1] == self.StdID.get():
                    dbbackend.deleteRec(row[0])
                    found = True
                    break
            if found:
                messagebox.showinfo("Deleted", "Record deleted successfully!")
                self.clearData()
            else:
                messagebox.showwarning("Error", "Record not found!")

    def searchDatabase(self):
        results = dbbackend.searchData(
            self.StdID.get(), self.Firstname.get(), self.Surname.get(),
            self.DoB.get(), self.Age.get(), self.Gender.get(),
            self.Address.get(), self.Mobile.get()
        )
        if not results:
            messagebox.showinfo("No Results", "No matching records found.")
        else:
            self.openDisplayWindow(results)

    def update(self):
        all_records = dbbackend.viewData()
        found = False
        for row in all_records:
            if row[1] == self.StdID.get():
                dbbackend.deleteRec(row[0])
                found = True
                break
        if found:
            dbbackend.addStdRec(
                self.StdID.get(), self.Firstname.get(), self.Surname.get(),
                self.DoB.get(), self.Age.get(), self.Gender.get(),
                self.Address.get(), self.Mobile.get()
            )
            messagebox.showinfo("Updated", "Record updated successfully!")
        else:
            messagebox.showwarning("Error", "No record found with this ID.")

    # ================= SEPARATE DISPLAY WINDOW =================
    def openDisplayWindow(self, records=None):
        # Create new window
        display_window = Toplevel(self.root)
        display_window.title("Student Records")
        display_window.geometry("1100x520")
        display_window.config(bg="#f3f7fb")

        Label(display_window, text="📋 Student Records",
              font=("Segoe UI Black", 20, "bold"), bg="#f3f7fb", fg="#0f172a").pack(pady=10)

        # Table styling
        style = ttk.Style(display_window)
        style.theme_use('default')
        style.configure("Vibrant.Treeview", highlightthickness=0, bd=0, font=('Segoe UI', 11),
                        background=self.palette["row_main"], foreground="#0f172a", rowheight=28, fieldbackground=self.palette["row_main"])
        style.configure("Vibrant.Treeview.Heading", font=('Segoe UI Semibold', 12), background=self.palette["accent3"], foreground="white")
        style.map('Vibrant.Treeview', background=[('selected', self.palette["accent1"])])

        cols = ("ID", "Student ID", "Firstname", "Surname", "DOB", "Age", "Gender", "Address", "Mobile")
        tree = ttk.Treeview(display_window, columns=cols, show='headings', style="Vibrant.Treeview")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Scrollbars
        vsb = ttk.Scrollbar(display_window, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(display_window, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        hsb.pack(side=BOTTOM, fill=X)
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Load data (with zebra rows)
        data = records if records else dbbackend.viewData()
        for i, row in enumerate(data):
            tag = 'odd' if i % 2 == 0 else 'even'
            tree.insert("", "end", values=row, tags=(tag,))

        tree.tag_configure('odd', background=self.palette["row_main"])
        tree.tag_configure('even', background=self.palette["row_alt"])

# ================= MAIN =================
if __name__ == "__main__":
    root = Tk()
    # increase default font scaling slightly for a more modern look
    default_font = ('Segoe UI', 10)
    root.option_add("*Font", default_font)
    app = StudentUI(root)
    root.mainloop()
