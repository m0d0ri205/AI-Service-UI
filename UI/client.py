import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import json
import os

# ----------------------------------
# 다크 모드에서 사용할 색상 설정
# ----------------------------------
DARK_BUTTON = "#3b82f6"
DARK_ACCENT = "#22c55e"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 기본 윈도우 설정
        self.title("Scanner")
        self.geometry("1100x650")
        self.minsize(900, 500)

        # 다크 모드 강제 적용
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # History에 저장될 데이터 리스트
        self.history_items = []

        # 기본 JSON (Specification 화면에 초기 표시됨)
        self.default_json = """{
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
}"""

        # 화면 레이아웃 영역 생성
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # UI 화면(프레임) 생성
        self.create_main_screen()
        self.create_input_screen()
        self.create_history_screen()
        self.create_spec_screen()

        # 첫 화면 표시
        self.show_frame(self.main_frame)

    # ------------------------------------
    # 공용 함수: 주어진 프레임을 화면에 표시
    # ------------------------------------
    def show_frame(self, frame):
        frame.tkraise()

    # ------------------------------------
    # 메인 화면 Textbox 기본 문구 제거
    # ------------------------------------
    def clear_main_placeholder(self, event):
        if self.main_textbox.get("1.0", "end-1c") == "input the file...":
            self.main_textbox.delete("1.0", "end")

    # ===============================
    # 메인 화면
    # ===============================
    def create_main_screen(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # 메인 화면 레이아웃 설정
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 메인 텍스트 입력 박스 (Attack Type 입력용)
        self.main_textbox = ctk.CTkTextbox(self.main_frame, height=280)
        self.main_textbox.grid(row=0, column=0, padx=40, pady=(60, 20), sticky="nsew")
        self.main_textbox.insert("1.0", "input the file...")
        self.main_textbox.bind("<FocusIn>", self.clear_main_placeholder)

        # 버튼 영역
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, pady=20)

        common = {"width": 200, "height": 50, "corner_radius": 22}

        # 입력 화면 이동 버튼
        ctk.CTkButton(
            buttons_frame, text="Input",
            fg_color=DARK_BUTTON, hover_color="#2563eb",
            command=lambda: self.show_frame(self.input_frame),
            **common
        ).grid(row=0, column=0, padx=20)

        # History 화면 이동 버튼
        ctk.CTkButton(
            buttons_frame, text="History",
            fg_color=DARK_ACCENT, hover_color="#16a34a",
            command=self.open_history_screen,
            **common
        ).grid(row=0, column=1, padx=20)

        # Specification 화면 이동 버튼
        ctk.CTkButton(
            buttons_frame, text="Specifications",
            fg_color="#64748b", hover_color="#475569",
            command=self.open_spec_default,
            **common
        ).grid(row=0, column=2, padx=20)

    # ===============================
    # Input 화면
    # ===============================
    def create_input_screen(self):
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="nsew")

        self.input_frame.grid_rowconfigure(5, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # 뒤로가기 버튼
        ctk.CTkButton(
            self.input_frame, text="✕", width=40, height=40,
            corner_radius=20, fg_color="transparent",
            hover_color="#475569",
            command=lambda: self.show_frame(self.main_frame)
        ).grid(row=0, column=1, sticky="ne", padx=20, pady=20)

        # URL 입력 영역
        ctk.CTkLabel(self.input_frame, text="URL:").grid(
            row=0, column=0, padx=40, pady=(40, 5), sticky="w"
        )
        self.url_entry = ctk.CTkEntry(
            self.input_frame, width=450,
            placeholder_text="https://example.com"
        )
        self.url_entry.grid(row=0, column=0, padx=120, pady=(40, 5), sticky="w")

        # 파일 선택 영역
        ctk.CTkLabel(self.input_frame, text="File:").grid(
            row=1, column=0, padx=40, pady=(20, 5), sticky="w"
        )
        self.file_entry = ctk.CTkEntry(
            self.input_frame, width=450,
            placeholder_text="Choose .csv, .txt, .xlsx"
        )
        self.file_entry.grid(row=1, column=0, padx=120, pady=(20, 5), sticky="w")

        # 파일 선택 버튼
        ctk.CTkButton(
            self.input_frame, text="Browse",
            width=90, corner_radius=18,
            command=self.choose_file
        ).grid(row=1, column=0, sticky="e", padx=40)

        # 메시지 출력 라벨
        self.msg = ctk.CTkLabel(self.input_frame, text="", text_color="#ef4444")
        self.msg.grid(row=2, column=0, padx=120, pady=10, sticky="w")

        # Start 버튼
        ctk.CTkButton(
            self.input_frame, text="Start",
            fg_color=DARK_BUTTON, hover_color="#2563eb",
            width=180, height=50, corner_radius=22,
            command=self.start_analysis
        ).grid(row=3, column=0, pady=20)

        # 결과 출력 박스 (Start 클릭 후 생성)
        self.output_box = None

    # 파일 선택 기능
    def choose_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.txt *.xlsx"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, file_path)

    # --------------------------------------------------
    # Start 버튼 클릭 시 Prompt 생성 및 History 저장
    # --------------------------------------------------
    def start_analysis(self):
        url = self.url_entry.get().strip()
        file = self.file_entry.get().strip()
        attack_type = self.main_textbox.get("1.0", "end-1c").strip()

        # 기본 문구 삭제 처리
        if attack_type == "input the file...":
            attack_type = ""

        # URL과 File 둘 다 입력된 경우 오류 처리
        if url and file:
            self.msg.configure(text="URL 또는 File 중 하나만 선택해야 합니다.")
            return

        # -------------------------------
        # CASE 1: URL 또는 File 입력 → Prompt 1 생성
        # -------------------------------
        if url or file:
            filename = os.path.basename(file) if file else "None"

            prompt = f"""
당신은 입력한 접속 경로와 파일들을 토대로 kali mcp를 사용해서 해당 사이트의 설정 값이나 구성들을 분석해서 예측되는 시나리오를 분석해서 알려주셔야 합니다. 당신은 CTF 전문가이며, 해당 시나리오는 우리가 만든 ai 모델을 통해 해당 시나리오를 통해 'attack type'을 출력하도록 만들 겁니다.

### 접속 정보 : {url}
### 파일 구성 : {filename}
### result :
### 시나리오 : 예상되는 시나리오를 입력하면 됩니다.
""".strip()

            self.show_output(prompt)
            self.history_items.append(prompt)
            self.msg.configure(text="Prompt 생성 완료", text_color=DARK_ACCENT)
            return

        # -------------------------------
        # CASE 2: Attack Type 입력 → Prompt 2 생성
        # -------------------------------
        if attack_type:
            prompt = f"""
입력한 '{attack_type}'를 토대로 실제로 해당 취약점이 있는지 판단 후, 이를 레포트 형태로 만들어주세요.
""".strip()

            self.show_output(prompt)
            self.history_items.append(prompt)
            self.msg.configure(text="Attack Type Prompt 생성 완료", text_color=DARK_ACCENT)
            return

        # -------------------------------
        # CASE 3: 아무 입력도 없을 때
        # -------------------------------
        self.msg.configure(text="URL, File 또는 Attack Type 중 하나를 입력해주세요.")

    # --------------------------------------------------
    # Prompt 출력 박스 생성
    # --------------------------------------------------
    def show_output(self, text):
        if self.output_box is None:
            self.output_box = ctk.CTkTextbox(self.input_frame, height=250)
            self.output_box.grid(row=4, column=0, padx=120, pady=20, sticky="nsew")

        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)

    # ===============================
    # History 화면
    # ===============================
    def create_history_screen(self):
        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=0, column=0, sticky="nsew")

        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        # 뒤로가기 버튼
        ctk.CTkButton(
            self.history_frame, text="✕", width=40,
            fg_color="transparent", hover_color="#475569",
            command=lambda: self.show_frame(self.main_frame)
        ).grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        # 타이틀
        ctk.CTkLabel(
            self.history_frame, text="History",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="nw", padx=40, pady=20)

        # 스크롤 프레임
        self.scroll = ctk.CTkScrollableFrame(self.history_frame)
        self.scroll.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")

    # History 화면 열기
    def open_history_screen(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        # 저장된 Prompt 목록 버튼 생성
        for i, prompt in enumerate(self.history_items):
            ctk.CTkButton(
                self.scroll,
                text=f"Entry #{i + 1}",
                width=500, corner_radius=15,
                fg_color="#334155", hover_color="#475569",
                command=lambda idx=i: self.open_selected_history(idx)
            ).pack(pady=5, anchor="w")

        self.show_frame(self.history_frame)

    # History 항목 선택 시 Specification에 표시
    def open_selected_history(self, index):
        self.spec_box.delete("1.0", "end")
        self.spec_box.insert("1.0", self.history_items[index])
        self.show_frame(self.spec_frame)

    # ===============================
    # Specification 화면
    # ===============================
    def create_spec_screen(self):
        self.spec_frame = ctk.CTkFrame(self)
        self.spec_frame.grid(row=0, column=0, sticky="nsew")

        self.spec_frame.grid_rowconfigure(1, weight=1)
        self.spec_frame.grid_columnconfigure(0, weight=1)

        # 뒤로가기 버튼
        ctk.CTkButton(
            self.spec_frame, text="✕", width=40,
            fg_color="transparent", hover_color="#475569",
            command=lambda: self.show_frame(self.main_frame)
        ).grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        # 타이틀
        ctk.CTkLabel(
            self.spec_frame, text="Specifications (JSON View)",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="nw", padx=40, pady=20)

        # JSON 표시 Textbox
        self.spec_box = ctk.CTkTextbox(self.spec_frame)
        self.spec_box.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")

        # 기본 JSON 로드
        self.spec_box.insert("1.0", self.default_json)

    # Specification 버튼 클릭 시 기본 JSON 표시
    def open_spec_default(self):
        self.spec_box.delete("1.0", "end")
        self.spec_box.insert("1.0", self.default_json)
        self.show_frame(self.spec_frame)


# ------------------------------------
# 실행
# ------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
