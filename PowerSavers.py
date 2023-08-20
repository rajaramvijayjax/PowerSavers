import os
import tkinter as tk
import psutil
import pygetwindow as gw

# Function to hide the IDLE window
def hide_idle_window():
    windows = gw.getWindowsWithTitle('')
    for win in windows:
        if "IDLE" in win.title:
            win.minimize()

# Function from Script B
def kill_non_essential_processes():
    essential_processes = [
        "System", "svchost.exe", "explorer.exe", "winlogon.exe",
        "csrss.exe", "lsass.exe", "spoolsv.exe", "services.exe",
        "smss.exe", "conhost.exe", "wininit.exe", "pythonw.exe","python.exe",
        "python.exe", "py.exe",
        "searchapp.exe",
        "runtimebroker.exe", 
        "startmenuexperiencehost.exe",
        "dllhost.exe",
        "sihost.exe",
        "textinputhost.exe",
        "ctfmon.exe",
        "smartscreen.exe"
    ]

    terminated_processes = []
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name'])
            process_name = process_info['name']
            process_pid = process_info['pid']

            if process_name.lower() not in essential_processes:
                psutil.Process(process_pid).terminate()
                terminated_processes.append(process_name)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return terminated_processes

# Script A with modification
class ProcessKillerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Power Options")
        self.root.geometry("600x350")

        self.label = tk.Label(root, text="Select an option:")
        self.label.pack(padx=10, pady=10)

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(padx=10, pady=5)

        self.button_power_saver = tk.Button(root, text="Power Saver Mode", command=self.set_power_saver_mode)
        self.button_power_saver.pack(padx=10, pady=5, fill=tk.X)

        self.button_high_performance = tk.Button(root, text="High Performance Mode", command=self.set_high_performance_mode)
        self.button_high_performance.pack(padx=10, pady=5, fill=tk.X)

        self.button_kill_processes = tk.Button(root, text="Kill Non-Critical Processes", command=self.on_kill_processes_button)
        self.button_kill_processes.pack(padx=10, pady=5, fill=tk.X)

        self.scroll_frame = tk.Frame(root)
        self.scroll_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Adjusting the text widget's height
        self.text_widget = tk.Text(self.scroll_frame, height=20, width=40)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a Scrollbar
        self.scrollbar = tk.Scrollbar(self.scroll_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configuring the text widget to work with the scrollbar
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_widget.yview)

    def set_power_saver_mode(self):
        self.clear_status()
        self.log_message("Switching to Power Saver Mode...")
        os.system("powercfg -s a1841308-3541-4fab-bc81-f71556f20b4a")
        self.root.after(5000, self.update_power_scheme_status)

    def set_high_performance_mode(self):
        self.clear_status()
        self.log_message("Switching to High Performance Mode...")
        os.system("powercfg -s 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
        self.root.after(5000, self.update_power_scheme_status)

    def update_power_scheme_status(self):
        self.current_power_scheme = self.get_current_power_scheme()
        self.log_message(f"SUCCESS. Current Power Scheme: {self.current_power_scheme}", status=True)


    def on_kill_processes_button(self):
        self.clear_status()
        self.text_widget.delete(1.0, tk.END)  # Clear previous contents

        hide_idle_window()  # Hide IDLE window before terminating processes

        terminated_processes = kill_non_essential_processes()

        for proc_name in terminated_processes:
            self.log_message(f"Terminated {proc_name}")

        self.log_message("All non-critical processes killed.", status=True)

    def log_message(self, message, status=False):
        if status:
            self.status_label.config(text=message, fg="green")
        else:
            self.text_widget.insert(tk.END, message + "\n")
            self.text_widget.see(tk.END)

    def clear_status(self):
        self.status_label.config(text="", fg="blue")

    def get_current_power_scheme(self):
        result = os.popen("powercfg -getactivescheme").read()
        lines = result.split('\n')
        for line in lines:
            if "Power Scheme GUID:" in line:
                return line.split(":")[1].strip()
        return ""

def main():
    root = tk.Tk()
    app = ProcessKillerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
