import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
from pathlib import Path
from src.laptop_repair.crew import LaptopRepairCrew

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class WindowsSystemDiagnosticGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows System Diagnostic Agent")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        style = ttk.Style()
        style.theme_use('clam')
        
        self.diagnosis_report = ""
        self.script_content = ""
        self.diagnosis_content = ""
        self.submitted_problem = ""
        self.show_script_permission = False
        self.user_approved_script = False
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(main_frame, text="🤖 Windows System Diagnostic Agent", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        desc_text = """Welcome! I'm an AI agent designed to help you diagnose problems with your Windows computer.
Describe the issue you're facing, provide your Gemini API key, and I'll investigate and create a fix script for you."""

        desc_label = ttk.Label(main_frame, text=desc_text, wraplength=800, justify=tk.LEFT)
        desc_label.grid(row=1, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        self.create_input_section(main_frame, row=2)
        self.create_results_section(main_frame, row=3)
        self.create_script_permission_section(main_frame, row=4)
        self.create_script_display_section(main_frame, row=5)
        
    def create_input_section(self, parent, row):
        input_frame = ttk.LabelFrame(parent, text="1. Enter Your Details", padding="10")
        input_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Gemini API Key:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(input_frame, textvariable=self.api_key_var, show="*", width=50)
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
        
        ttk.Label(input_frame, text="Problem Description:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(5, 0))
        self.problem_text = scrolledtext.ScrolledText(input_frame, height=4, width=50)
        self.problem_text.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 10), padx=(10, 0))
        
        self.diagnose_btn = ttk.Button(input_frame, text="🔍 Diagnose My System", command=self.start_diagnosis)
        self.diagnose_btn.grid(row=2, column=1, pady=(0, 5), padx=(10, 0), sticky=tk.W)
        
        self.progress_var = tk.StringVar(value="Ready to diagnose...")
        self.progress_label = ttk.Label(input_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=3, column=1, padx=(10, 0), sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(input_frame, mode='indeterminate')
        self.progress_bar.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(5, 0), padx=(10, 0))
        
    def create_results_section(self, parent, row):
        self.results_frame = ttk.LabelFrame(parent, text="2. Diagnosis Results", padding="10")
        self.results_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(1, weight=1)
        parent.rowconfigure(row, weight=1)
        
        self.problem_label = ttk.Label(self.results_frame, text="", font=("Arial", 9, "italic"))
        self.problem_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=15, state=tk.DISABLED)
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.results_frame.grid_remove()
        
    def create_script_permission_section(self, parent, row):
        self.permission_frame = ttk.LabelFrame(parent, text="3. 🔧 Proposed Fix Script", padding="10")
        self.permission_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.permission_frame.columnconfigure(0, weight=1)
        
        warning_text = """⚠️ IMPORTANT: Script Generation Request

The diagnostic agent has identified your issue and can create a Windows Batch Script (.bat file) to fix it automatically.

Before you proceed:
• The script will make changes to your system
• Always backup important data before running system repair scripts
• Review the script content carefully before execution
• Run the script as Administrator when prompted"""
        
        self.warning_label = ttk.Label(self.permission_frame, text=warning_text, foreground="orange", wraplength=800, justify=tk.LEFT)
        self.warning_label.grid(row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        buttons_frame = ttk.Frame(self.permission_frame)
        buttons_frame.grid(row=1, column=0, pady=(0, 5))
        
        ttk.Button(buttons_frame, text="✅ Yes, Create Fix Script", command=self.approve_script).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons_frame, text="❌ No, Just Show Diagnosis", command=self.decline_script).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(buttons_frame, text="🔄 Run New Diagnosis", command=self.reset_diagnosis).grid(row=0, column=2)
        self.permission_frame.grid_remove()
        
    def create_script_display_section(self, parent, row):
        self.script_frame = ttk.LabelFrame(parent, text="4. 📥 Your Fix Script", padding="10")
        self.script_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.script_frame.columnconfigure(0, weight=1)
        self.script_frame.rowconfigure(1, weight=1)
        
        self.success_label = ttk.Label(self.script_frame, text="✅ Script has been generated based on your approval!", foreground="green", font=("Arial", 10, "bold"))
        self.success_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        self.script_text = scrolledtext.ScrolledText(self.script_frame, height=10, state=tk.DISABLED, font=("Courier", 9))
        self.script_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        script_buttons_frame = ttk.Frame(self.script_frame)
        script_buttons_frame.grid(row=2, column=0, pady=(0, 10))
        
        ttk.Button(script_buttons_frame, text="📥 Save Fix Script", command=self.save_script).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(script_buttons_frame, text="🔄 Generate New Script", command=self.regenerate_script).grid(row=0, column=1)
        
        instructions_text = """📋 How to Run the Script:
1. Save the script file using the button above
2. Right-click on the saved .bat file
3. Select "Run as administrator" (very important!)
4. Follow the prompts in the command window
5. Wait for the script to complete
6. Restart your computer if prompted
7. Test if your original problem is resolved"""
        
        self.instructions_label = ttk.Label(self.script_frame, text=instructions_text, foreground="blue", wraplength=800, justify=tk.LEFT)
        self.instructions_label.grid(row=3, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        self.script_frame.grid_remove()
        
    def start_diagnosis(self):
        api_key = self.api_key_var.get().strip()
        problem = self.problem_text.get("1.0", tk.END).strip()
        
        if not api_key:
            messagebox.showwarning("Missing API Key", "Please enter your Gemini API Key to proceed.")
            return
            
        if not problem:
            messagebox.showwarning("Missing Problem Description", "Please describe the problem before starting the diagnosis.")
            return
            
        self.reset_state()
        os.environ["GEMINI_API_KEY"] = api_key
        self.submitted_problem = problem
        self.diagnose_btn.config(state=tk.DISABLED)
        self.progress_var.set("The diagnostic agents are investigating... This may take a moment.")
        self.progress_bar.start()
        thread = threading.Thread(target=self.run_diagnosis, args=(problem,))
        thread.daemon = True
        thread.start()
        
    def run_diagnosis(self, problem):
        try:
            repair_crew = LaptopRepairCrew(problem)
            report = repair_crew.run()
            self.root.after(0, self.diagnosis_complete, report)
            
        except Exception as e:
            error_msg = f"An error occurred while running the diagnosis: {e}"
            self.root.after(0, self.diagnosis_error, error_msg)
            
    def diagnosis_complete(self, report):
        self.diagnosis_report = report
        self.progress_bar.stop()
        self.progress_var.set("Diagnosis complete!")
        self.diagnose_btn.config(state=tk.NORMAL)
        
        if "--- BATCH SCRIPT START ---" in report:
            try:
                diagnosis, script_full = report.split("--- BATCH SCRIPT START ---", 1)
                script_content = script_full.split("--- BATCH SCRIPT END ---")[0].strip()
                self.diagnosis_content = diagnosis
                self.script_content = script_content
                self.show_script_permission = True
            except ValueError:
                self.diagnosis_content = report
                self.show_script_permission = False
        else:
            self.diagnosis_content = report
            self.show_script_permission = False
            
        # Update UI
        self.display_results()
        
    def diagnosis_error(self, error_msg):
        self.progress_bar.stop()
        self.progress_var.set("Diagnosis failed!")
        self.diagnose_btn.config(state=tk.NORMAL)
        messagebox.showerror("Diagnosis Error", error_msg)
        
    def display_results(self):
        self.results_frame.grid()
        self.problem_label.config(text=f"Problem Investigated: {self.submitted_problem}")
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        if self.diagnosis_content:
            self.results_text.insert(tk.END, self.diagnosis_content)
        else:
            self.results_text.insert(tk.END, self.diagnosis_report)
        self.results_text.config(state=tk.DISABLED)

        if self.show_script_permission and not self.user_approved_script:
            self.permission_frame.grid()
        else:
            self.permission_frame.grid_remove()
            
    def approve_script(self):
        self.user_approved_script = True
        self.permission_frame.grid_remove()
        self.display_script()
        
    def decline_script(self):
        self.show_script_permission = False
        self.permission_frame.grid_remove()
        
    def regenerate_script(self):
        self.user_approved_script = False
        self.show_script_permission = True
        self.script_frame.grid_remove()
        self.permission_frame.grid()
        
    def reset_diagnosis(self):
        self.reset_state()
        self.results_frame.grid_remove()
        self.permission_frame.grid_remove()
        self.script_frame.grid_remove()
        self.progress_var.set("Ready to diagnose...")
        
    def reset_state(self):
        self.diagnosis_report = ""
        self.script_content = ""
        self.diagnosis_content = ""
        self.submitted_problem = ""
        self.show_script_permission = False
        self.user_approved_script = False
        
    def display_script(self):
        if self.user_approved_script and self.script_content:
            self.script_frame.grid()
            self.script_text.config(state=tk.NORMAL)
            self.script_text.delete("1.0", tk.END)
            self.script_text.insert(tk.END, self.script_content)
            self.script_text.config(state=tk.DISABLED)
            
    def save_script(self):
        if not self.script_content:
            messagebox.showwarning("No Script", "No script content to save.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".bat",
            filetypes=[("Batch files", "*.bat"), ("All files", "*.*")],
            initialname="system_fix_script.bat"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.script_content)
                messagebox.showinfo("Script Saved", f"Fix script saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save script: {e}")

def main():
    root = tk.Tk()
    app = WindowsSystemDiagnosticGUI(root)
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    root.mainloop()

if __name__ == "__main__":
    main()