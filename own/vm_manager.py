import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from hypervisor import Hypervisor  # Assuming the hypervisor is saved in hypervisor.py

class VirtualMachineManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Machine Manager")

        self.hypervisor = Hypervisor()  # Initialize Hypervisor instance

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # VM Listbox
        self.vm_listbox = tk.Listbox(self.root, width=40, height=10)
        self.vm_listbox.pack(padx=20, pady=10)

        # Create VM Button
        create_vm_button = tk.Button(self.root, text="Create VM", command=self.create_new_vm)
        create_vm_button.pack(pady=5)

        # Start VM Button
        start_button = tk.Button(self.root, text="Start VM", command=self.start_vm)
        start_button.pack(pady=5)

        # Stop VM Button
        stop_button = tk.Button(self.root, text="Stop VM", command=self.stop_vm)
        stop_button.pack(pady=5)

        # Refresh List Button
        refresh_button = tk.Button(self.root, text="Refresh List", command=self.refresh_list)
        refresh_button.pack(pady=5)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.pack(pady=5)

        # Initial VM List
        self.refresh_list()

    def create_new_vm(self):
        vm_name = simpledialog.askstring("Input", "Enter VM name:")
        if not vm_name:
            messagebox.showerror("Error", "VM name is required")
            return

        iso_path = filedialog.askopenfilename(title="Select ISO File", filetypes=[("ISO files", "*.iso")])
        if not iso_path:
            messagebox.showerror("Error", "ISO file is required")
            return

        memory = simpledialog.askinteger("Input", "Enter memory in MB:")
        if not memory or memory <= 0:
            messagebox.showerror("Error", "Invalid memory size")
            return

        cpu_shares = simpledialog.askinteger("Input", "Enter CPU shares:")
        if not cpu_shares or cpu_shares <= 0:
            messagebox.showerror("Error", "Invalid CPU shares")
            return

        try:
            self.hypervisor.create_vm(vm_name, iso_path, memory * 1024 * 1024, cpu_shares)
            messagebox.showinfo("Create VM", f"VM '{vm_name}' created successfully.")
            self.refresh_list()  # Refresh VM list after creation
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_vm(self):
        selected_index = self.vm_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a VM to start.")
            return

        vm_name = self.vm_listbox.get(selected_index)
        try:
            self.hypervisor.start_vm(vm_name)
            messagebox.showinfo("VM Started", f"VM {vm_name} started successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_vm(self):
        selected_index = self.vm_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a VM to stop.")
            return

        vm_name = self.vm_listbox.get(selected_index)
        try:
            self.hypervisor.stop_vm(vm_name)
            messagebox.showinfo("VM Stopped", f"VM {vm_name} stopped successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_list(self):
        self.vm_listbox.delete(0, tk.END)
        vms = self.hypervisor.list_vms()
        for vm in vms:
            self.vm_listbox.insert(tk.END, vm)

def main():
    root = tk.Tk()
    app = VirtualMachineManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
