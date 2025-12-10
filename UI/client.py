import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import json

# ----------------------------------
# Modern Colors (Dark / Light themes)
# ----------------------------------
DARK_BUTTON = "#3b82f6"
DARK_BG = "#0f172a"
DARK_ACCENT = "#22c55e"

LIGHT_BUTTON = "#3b82f6"
LIGHT_BG = "#ffffff"
LIGHT_ACCENT = "#16a34a"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Base window
        self.title("Scanner")
        self.geometry("1100x650")
        self.minsize(900, 500)

        # Default theme = dark
        self.current_theme = "dark"
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # History now stores JSON strings
        self.history_items = []

        # Example JSON result (dummy data)
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

    # -------------------------------------
    # DARK/LIGHT MODE
    # -------------------------------------
    def toggle_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌙", text_color="black")
        else:
            self.current_theme = "dark"
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="☀", text_color="white")

    def show_frame(self, frame):
        frame.tkraise()

    # Clears default placeholder text
    def clear_main_placeholder(self, event):
        if self.main_textbox.get("1.0", "end-1c").strip() == "input the file...":
            self.main_textbox.delete("1.0", "end")

    # ===============================
    # MAIN SCREEN
    # ===============================
    def create_main_screen(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # THEME BUTTON
        self.theme_btn = ctk.CTkButton(
            self.main_frame, text="☀", text_color="white",
            width=40, height=40, corner_radius=20,
            fg_color="transparent", hover_color="#475569",
            command=self.toggle_theme
        )
        self.theme_btn.grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        # MAIN BIG TEXTBOX
        self.main_textbox = ctk.CTkTextbox(self.main_frame, height=280)
        self.main_textbox.grid(row=0, column=0, padx=40, pady=(70, 20), sticky="nsew")
        self.main_textbox.insert("1.0", "input the file...")
        self.main_textbox.bind("<FocusIn>", self.clear_main_placeholder)

        # BUTTON ROW
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
            fg_color="#22c55e", hover_color="#16a34a",
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
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=0, column=0, sticky="nsew")

        for r in range(5):
            self.input_frame.grid_rowconfigure(r, weight=0)
        self.input_frame.grid_rowconfigure(4, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # BACK BUTTON
        back = ctk.CTkButton(
            self.input_frame, text="✕", width=40, height=40,
            corner_radius=20, fg_color="transparent",
            hover_color="#475569", command=self.back_from_input
        )
        back.grid(row=0, column=1, sticky="ne", padx=20, pady=20)

        # URL INPUT
        ctk.CTkLabel(self.input_frame, text="URL:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=40, pady=(40, 5), sticky="w"
        )
        self.url_entry = ctk.CTkEntry(self.input_frame, width=450,
                                      placeholder_text="https://example.com")
        self.url_entry.grid(row=0, column=0, padx=120, pady=(40, 5), sticky="w")

        # FILE INPUT
        ctk.CTkLabel(self.input_frame, text="File:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=40, pady=(20, 5), sticky="w"
        )
        self.file_entry = ctk.CTkEntry(self.input_frame, width=450,
                                       placeholder_text="Choose .csv, .txt, .xlsx")
        self.file_entry.grid(row=1, column=0, padx=120, pady=(20, 5), sticky="w")

        browse = ctk.CTkButton(
            self.input_frame, text="Browse", width=90,
            corner_radius=18, command=self.choose_file
        )
        browse.grid(row=1, column=0, sticky="e", padx=40, pady=5)

        # MESSAGE
        self.msg = ctk.CTkLabel(self.input_frame, text="", text_color="#ef4444")
        self.msg.grid(row=2, column=0, padx=120, pady=10, sticky="w")

        # START BUTTON
        start_btn = ctk.CTkButton(
            self.input_frame, text="Start",
            fg_color=DARK_BUTTON, hover_color="#2563eb",
            width=180, height=50, corner_radius=22,
            command=self.record_input
        )
        start_btn.grid(row=3, column=0, pady=40)

    def back_from_input(self):
        self.url_entry.delete(0, "end")
        self.file_entry.delete(0, "end")
        self.msg.configure(text="")
        self.url_entry.configure(placeholder_text="https://example.com")
        self.file_entry.configure(placeholder_text="Choose .csv, .txt, .xlsx")
        self.show_frame(self.main_frame)

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.txt *.xlsx"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path)

    # ===============================
    # STORE JSON RESULT (NOT URL/FILE)
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

        # Save JSON result (dummy for now)
        json_string = json.dumps(self.example_json, ensure_ascii=False, indent=4)

        self.history_items.append(json_string)
        self.msg.configure(text="Analysis Result Saved!", text_color="#22c55e")

    # ===============================
    # HISTORY SCREEN
    # ===============================
    def create_history_screen(self):
        self.history_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.history_frame.grid(row=0, column=0, sticky="nsew")

        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        # BACK BUTTON
        back = ctk.CTkButton(
            self.history_frame, text="✕", width=40, height=40,
            corner_radius=20, fg_color="transparent",
            hover_color="#475569", command=lambda: self.show_frame(self.main_frame)
        )
        back.grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        # TITLE
        ctk.CTkLabel(
            self.history_frame, text="History",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="nw", padx=40, pady=20)

        # SCROLL AREA
        self.scroll = ctk.CTkScrollableFrame(self.history_frame)
        self.scroll.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")

    def open_history_screen(self):
        self.refresh_history()
        self.show_frame(self.history_frame)

    # CLICK RESULT → LOAD JSON IN SPEC PAGE
    def open_selected_history(self, index):
        self.spec_box.delete("1.0", "end")
        self.spec_box.insert("1.0", self.history_items[index])
        self.show_frame(self.spec_frame)

    def refresh_history(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for i, item in enumerate(self.history_items):
            btn = ctk.CTkButton(
                self.scroll,
                text=f"Result #{i+1}",
                width=500,
                corner_radius=15,
                fg_color="#334155",
                hover_color="#475569",
                command=lambda idx=i: self.open_selected_history(idx)
            )
            btn.grid(row=i, column=0, sticky="w", pady=5)

    # ===============================
    # SPECIFICATION SCREEN
    # ===============================
    def create_spec_screen(self):
        self.spec_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.spec_frame.grid(row=0, column=0, sticky="nsew")

        self.spec_frame.grid_rowconfigure(1, weight=1)
        self.spec_frame.grid_columnconfigure(0, weight=1)

        # BACK BUTTON
        back = ctk.CTkButton(
            self.spec_frame, text="✕", width=40, height=40,
            corner_radius=20, fg_color="transparent",
            hover_color="#475569",
            command=lambda: self.show_frame(self.main_frame)
        )
        back.grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        # TITLE
        ctk.CTkLabel(
            self.spec_frame, text="Specifications (JSON View)",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="nw", padx=40, pady=20)

        # FULL SIZE TEXTBOX
        self.spec_box = ctk.CTkTextbox(self.spec_frame)
        self.spec_box.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")


# ------------------------------------------
# RUN
# ------------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
