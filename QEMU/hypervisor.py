import subprocess
import os

class VirtualMachine:
    def __init__(self, name, iso_path=None, disk_path=None):
        self.name = name
        self.iso_path = iso_path
        self.disk_path = disk_path
        self.process = None

    def create_disk(self, size_gb):
        self.disk_path = f"{self.name}.qcow2"
        cmd = [
            "qemu-img", "create", "-f", "qcow2", self.disk_path, f"{size_gb}G"
        ]
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            print(f"Error creating disk for {self.name}: {e}")
            self.disk_path = None

    def start(self):
        if not self.iso_path:
            raise RuntimeError(f"No ISO file selected for {self.name}")
        
        if not self.disk_path:
            raise RuntimeError(f"No disk created for {self.name}")

        if self.process:
            raise RuntimeError(f"VM {self.name} is already running")

        # QEMU command to start the VM
        cmd = [
            "qemu-system-x86_64",
            "-name", self.name,
            "-cdrom", self.iso_path,
            "-drive", f"file={self.disk_path},format=qcow2",
            "-m", "1024",
            "-enable-kvm"
        ]
        try:
            self.process = subprocess.Popen(cmd)
        except subprocess.CalledProcessError as e:
            print(f"Error starting {self.name}: {e}")
            self.process = None

    def stop(self):
        if not self.process:
            raise RuntimeError(f"VM {self.name} is not running")

        try:
            self.process.terminate()
            self.process.wait()
            self.process = None
        except Exception as e:
            print(f"Error stopping {self.name}: {e}")

    def status(self):
        if self.process:
            return f"VM {self.name} is running"
        else:
            return f"VM {self.name} is stopped"

class Hypervisor:
    def __init__(self):
        self.vms = {}

    def create_vm(self, name, iso_path, disk_size_gb):
        if name in self.vms:
            raise RuntimeError(f"VM {name} already exists")

        vm = VirtualMachine(name, iso_path)
        vm.create_disk(disk_size_gb)
        self.vms[name] = vm
        return vm

    def start_vm(self, name):
        if name not in self.vms:
            raise RuntimeError(f"VM {name} does not exist")

        self.vms[name].start()

    def stop_vm(self, name):
        if name not in self.vms:
            raise RuntimeError(f"VM {name} does not exist")

        self.vms[name].stop()

    def list_vms(self):
        return list(self.vms.keys())

    def get_vm_status(self, name):
        if name not in self.vms:
            raise RuntimeError(f"VM {name} does not exist")

        return self.vms[name].status()
