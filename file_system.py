import tkinter as tk
from tkinter import messagebox, simpledialog

class FileSystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("파일 시스템 시뮬레이터")
        self.current_directory = "/"
        self.file_system = {"root": {"files": {}, "directories": {}}}

        self.create_widgets()

    #tk 위젯 생성
    def create_widgets(self):
        self.text_area = tk.Text(self.root, height=20, width=60)
        self.text_area.pack()

        self.command_entry = tk.Entry(self.root, width=50)
        self.command_entry.pack()

        self.run_button = tk.Button(self.root, text="실행", command=self.run_command)
        self.run_button.pack()

        self.show_commands()

    #명령어 리스트
    def show_commands(self):
        self.text_area.insert(tk.END, """
사용 가능한 명령어 목록:
    create <filename> <content> - 파일 생성
    delete <filename> - 파일 삭제
    read <filename> - 파일 읽기
    write <filename> <content> - 파일 쓰기
    mkdir <dirname> - 디렉토리 생성
    rmdir <dirname> - 디렉토리 삭제
    cd <dirname> - 디렉토리 이동
    search <filename> - 파일 검색
    list - 현재 디렉토리의 파일 및 디렉토리 목록 출력
    show - 사용 가능한 명령어 목록 출력
    exit - 시뮬레이터 종료
        """)

    #명령어 실행
    def run_command(self):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.text_area.insert(tk.END, f"\n명령어: {command}\n")
        parts = command.split()
        cmd = parts[0]

        if cmd == "create":
            self.create_file(parts[1], " ".join(parts[2:]))
        elif cmd == "delete":
            self.delete_file(parts[1])
        elif cmd == "read":
            self.read_file(parts[1])
        elif cmd == "write":
            self.write_file(parts[1], " ".join(parts[2:]))
        elif cmd == "mkdir":
            self.make_directory(parts[1])
        elif cmd == "rmdir":
            self.remove_directory(parts[1])
        elif cmd == "cd":
            self.change_directory(parts[1])
        elif cmd == "search":
            self.search_file(parts[1])
        elif cmd == "list":
            self.list_directory()
        elif cmd == "show":
            self.show_commands()
        elif cmd == "exit":
            self.root.quit()
        else:
            messagebox.showerror("Error", "잘못된 명령어")

    #현재 디렉터리 위치 파악
    def get_current_directory(self):
        parts = self.current_directory.split("/")
        directory = self.file_system["root"]
        for part in parts:
            if part and part in directory["directories"]:
                directory = directory["directories"][part]
        return directory

    #파일 생성
    def create_file(self, filename, content):
        directory = self.get_current_directory()
        directory["files"][filename] = content
        self.text_area.insert(tk.END, f"파일 생성: '{filename}' 내용: '{content}' 위치: {self.current_directory}\n")

    #파일 삭제
    def delete_file(self, filename):
        directory = self.get_current_directory()
        if filename in directory["files"]:
            del directory["files"][filename]
            self.text_area.insert(tk.END, f"파일 삭제: '{filename}' 위치: {self.current_directory}\n")
        else:
            self.text_area.insert(tk.END, f"파일을 찾을 수 없음\n")

    #파일 읽기
    def read_file(self, filename):
        directory = self.get_current_directory()
        if filename in directory["files"]:
            content = directory["files"][filename]
            self.text_area.insert(tk.END, f"파일 읽기: '{filename}' 위치: {self.current_directory} 내용: '{content}'\n")
        else:
            self.text_area.insert(tk.END, f"파일을 찾을 수 없음\n")

    #파일 쓰기
    def write_file(self, filename, content):
        directory = self.get_current_directory()
        if filename in directory["files"]:
            directory["files"][filename] += content
            self.text_area.insert(tk.END, f"파일 쓰기: '{filename}' 내용: '{content}' 위치: {self.current_directory}\n")
        else:
            self.text_area.insert(tk.END, f"파일을 찾을 수 없음\n")

    #디렉터리 생성
    def make_directory(self, dirname):
        directory = self.get_current_directory()
        if dirname not in directory["directories"]:
            directory["directories"][dirname] = {"files": {}, "directories": {}}
            self.text_area.insert(tk.END, f"디렉토리 생성: '{dirname}' 위치: {self.current_directory}\n")
        else:
            self.text_area.insert(tk.END, f"디렉토리가 이미 존재: '{dirname}' 위치: {self.current_directory}\n")

    #디렉터리 삭제
    def remove_directory(self, dirname):
        directory = self.get_current_directory()
        if dirname in directory["directories"]:
            if not directory["directories"][dirname]["files"] and not directory["directories"][dirname]["directories"]:
                del directory["directories"][dirname]
                self.text_area.insert(tk.END, f"디렉토리 삭제: '{dirname}' 위치: {self.current_directory}\n")
            else:
                self.text_area.insert(tk.END, f"디렉토리가 비어있지 않음\n")
        else:
            self.text_area.insert(tk.END, f"디렉토리를 찾을 수 없음\n")

    #위치 변경
    def change_directory(self, dirname):
        if dirname == "/":
            self.current_directory = "/"
            self.text_area.insert(tk.END, "디렉토리를 루트로 변경\n")
        elif dirname == "..":
            parts = self.current_directory.split("/")
            if len(parts) > 1:
                self.current_directory = "/".join(parts[:-1]) or "/"
                self.text_area.insert(tk.END, "상위 디렉토리로 이동\n")
            else:
                self.text_area.insert(tk.END, "현재 루트 디렉토리에 있음\n")
        else:
            directory = self.get_current_directory()
            if dirname in directory["directories"]:
                self.current_directory += f"/{dirname}"
                self.text_area.insert(tk.END, f"디렉토리 위치 변경: '{dirname}'\n")
            else:
                self.text_area.insert(tk.END, f"디렉토리를 찾을 수 없음\n")

    #파일 검색
    def search_file(self, filename):
        def search_recursive(directory, path):
            if filename in directory["files"]:
                return f"{path}/{filename}"
            for dir_name, sub_dir in directory["directories"].items():
                result = search_recursive(sub_dir, f"{path}/{dir_name}")
                if result:
                    return result
            return None

        path = search_recursive(self.file_system["root"], "/root")
        if path:
            self.text_area.insert(tk.END, f"검색한 파일: '{filename}' 위치: {path}\n")
        else:
            self.text_area.insert(tk.END, f"파일을 찾을 수 없음\n")

    #리스트 출력
    def list_directory(self):
        directory = self.get_current_directory()
        files = directory["files"].keys()
        directories = directory["directories"].keys()
        self.text_area.insert(tk.END, f"{self.current_directory}의 내용:\n")
        self.text_area.insert(tk.END, "디렉토리:\n")
        for dir_name in directories:
            self.text_area.insert(tk.END, f"  {dir_name}/\n")
        self.text_area.insert(tk.END, "파일:\n")
        for file_name in files:
            self.text_area.insert(tk.END, f"  {file_name}\n")


root = tk.Tk()
fs_simulator = FileSystemSimulator(root)
root.mainloop()
 