import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import json

# ----------------------------------
# Dark Mode Colors Only
# ----------------------------------
DARK_BUTTON = "#3b82f6"
DARK_BG = "#0f172a"
DARK_ACCENT = "#22c55e"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Base window
        self.title("Scanner")
        self.geometry("1100x650")
        self.minsize(900, 500)

        # FORCE DARK MODE ONLY
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # History stores JSON strings
        self.history_items = []

        # Dummy JSON result
        self.example_json = {
            "workflow_status": "COMPLETED_SUCCESS",
            "flag": "SF{sf_flag1}",
            "solving_strategy": "secure-compare 라이브러리의 XOR 연산 버그를 이용하여 인증 우회",
            "key_insight": "a.charCodeAt(i) ^ a.charCodeAt(i) 버그로 인해 길이만 같으면 항상 0(true) 반환",
            "execution_summary": {
                "total_time": 420,
                "steps_executed": ["1", "2", "5-1", "5-2", "5-4", "6"],
                "tools_used": ["trivy", "perplexity_search", "curl", "execute_command"],
                "retry_count": 12,
                "critical_finding": "secure-compare 라이브러리의 XOR 연산 구현 버그"
            }
        }

        # Grid setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Screens
        self.create_main_screen()
        self.create_input_screen()
        self.create_history_screen()
        self.create_spec_screen()

        self.show_frame(self.main_frame)

    # -----------------------------
    # Utility
    # -----------------------------
    def show_frame(self, frame):
        frame.tkraise()

    def clear_main_placeholder(self, event):
        if self.main_textbox.get("1.0", "end-1c") == "input the file...":
            self.main_textbox.delete("1.0", "end")

    # ===============================
    # MAIN SCREEN
    # ===============================
    def create_main_screen(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # MAIN TEXTBOX
        self.main_textbox = ctk.CTkTextbox(self.main_frame, height=280)
        self.main_textbox.grid(row=0, column=0, padx=40, pady=(60, 20), sticky="nsew")
        self.main_textbox.insert("1.0", "input the file...")
        self.main_textbox.bind("<FocusIn>", self.clear_main_placeholder)

        # BUTTONS
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, pady=20)

        common = {"width": 200, "height": 50, "corner_radius": 22}

        ctk.CTkButton(
            buttons_frame, text="Input",
            fg_color=DARK_BUTTON, hover_color="#2563eb",
            command=lambda: self.show_frame(self.input_frame),
            **common
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            buttons_frame, text="History",
            fg_color=DARK_ACCENT, hover_color="#16a34a",
            command=self.open_history_screen,
            **common
        ).grid(row=0, column=1, padx=20)

        ctk.CTkButton(
            buttons_frame, text="Specifications",
            fg_color="#64748b", hover_color="#475569",
            command=lambda: self.show_frame(self.spec_frame),
            **common
        ).grid(row=0, column=2, padx=20)

    # ===============================
    # INPUT SCREEN
    # ===============================
    def create_input_screen(self):
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="nsew")

        self.input_frame.grid_rowconfigure(4, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # BACK
        ctk.CTkButton(
            self.input_frame, text="✕", width=40, height=40,
            corner_radius=20, fg_color="transparent",
            hover_color="#475569",
            command=lambda: self.show_frame(self.main_frame)
        ).grid(row=0, column=1, sticky="ne", padx=20, pady=20)

        # URL
        ctk.CTkLabel(self.input_frame, text="URL:").grid(
            row=0, column=0, padx=40, pady=(40, 5), sticky="w"
        )
        self.url_entry = ctk.CTkEntry(
            self.input_frame, width=450,
            placeholder_text="https://example.com"
        )
        self.url_entry.grid(row=0, column=0, padx=120, pady=(40, 5), sticky="w")

        # FILE
        ctk.CTkLabel(self.input_frame, text="File:").grid(
            row=1, column=0, padx=40, pady=(20, 5), sticky="w"
        )
        self.file_entry = ctk.CTkEntry(
            self.input_frame, width=450,
            placeholder_text="Choose .csv, .txt, .xlsx"
        )
        self.file_entry.grid(row=1, column=0, padx=120, pady=(20, 5), sticky="w")

        ctk.CTkButton(
            self.input_frame, text="Browse",
            width=90, corner_radius=18,
            command=self.choose_file
        ).grid(row=1, column=0, sticky="e", padx=40)

        self.msg = ctk.CTkLabel(self.input_frame, text="", text_color="#ef4444")
        self.msg.grid(row=2, column=0, padx=120, pady=10, sticky="w")

        ctk.CTkButton(
            self.input_frame, text="Start",
            fg_color=DARK_BUTTON, hover_color="#2563eb",
            width=180, height=50, corner_radius=22,
            command=self.record_input
        ).grid(row=3, column=0, pady=40)

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.txt *.xlsx"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path)

    # ===============================
    # SAVE JSON RESULT
    # ===============================
    def record_input(self):
        url = self.url_entry.get().strip()
        file = self.file_entry.get().strip()

        if url and file:
            self.msg.configure(text="Choose ONLY one: URL OR FILE")
            return
        if not url and not file:
            self.msg.configure(text="Please enter URL or File.")
            return

        json_string = json.dumps(self.example_json, ensure_ascii=False, indent=4)
        self.history_items.append(json_string)
        self.msg.configure(text="Analysis Result Saved!", text_color=DARK_ACCENT)

    # ===============================
    # HISTORY SCREEN
    # ===============================
    def create_history_screen(self):
        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=0, column=0, sticky="nsew")

        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            self.history_frame, text="✕", width=40,
            fg_color="transparent", hover_color="#475569",
            command=lambda: self.show_frame(self.main_frame)
        ).grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        ctk.CTkLabel(
            self.history_frame, text="History",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="nw", padx=40, pady=20)

        self.scroll = ctk.CTkScrollableFrame(self.history_frame)
        self.scroll.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")

    def open_history_screen(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for i in range(len(self.history_items)):
            ctk.CTkButton(
                self.scroll,
                text=f"Result #{i + 1}",
                width=500, corner_radius=15,
                fg_color="#334155", hover_color="#475569",
                command=lambda idx=i: self.open_selected_history(idx)
            ).pack(pady=5, anchor="w")

        self.show_frame(self.history_frame)

    def open_selected_history(self, index):
        self.spec_box.delete("1.0", "end")
        self.spec_box.insert("1.0", self.history_items[index])
        self.show_frame(self.spec_frame)

    # ===============================
    # SPEC SCREEN
    # ===============================
    def create_spec_screen(self):
        self.spec_frame = ctk.CTkFrame(self)
        self.spec_frame.grid(row=0, column=0, sticky="nsew")

        self.spec_frame.grid_rowconfigure(1, weight=1)
        self.spec_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            self.spec_frame, text="✕", width=40,
            fg_color="transparent", hover_color="#475569",
            command=lambda: self.show_frame(self.main_frame)
        ).grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        ctk.CTkLabel(
            self.spec_frame, text="Specifications (JSON View)",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="nw", padx=40, pady=20)

        self.spec_box = ctk.CTkTextbox(self.spec_frame)
        self.spec_box.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
