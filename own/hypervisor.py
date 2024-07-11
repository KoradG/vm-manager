import os
import subprocess
import psutil

class VirtualMachine:
    def __init__(self, name, disk_path, memory_limit, cpu_shares):
        self.name = name
        self.disk_path = disk_path
        self.memory_limit = memory_limit
        self.cpu_shares = cpu_shares
        self.process = None

    def start(self):
        if self.process is not None:
            raise RuntimeError(f"VM {self.name} is already running")

        # Command to start the VM in a new namespace
        cmd = ["unshare", "--fork", "--pid", "--mount-proc", "--ipc", "--net", "--uts", "--mount", "bash"]
        self.process = subprocess.Popen(cmd)
        
        # Setting up cgroups
        self.setup_cgroups()

    def stop(self):
        if self.process is None:
            raise RuntimeError(f"VM {self.name} is not running")
        
        self.process.terminate()
        self.process.wait()
        self.process = None

    def setup_cgroups(self):
        # Creating cgroup for CPU and memory
        cgroup_path = f"/sys/fs/cgroup/memory/{self.name}"
        os.makedirs(cgroup_path, exist_ok=True)
        with open(os.path.join(cgroup_path, "memory.limit_in_bytes"), "w") as f:
            f.write(str(self.memory_limit))
        with open(os.path.join(cgroup_path, "cgroup.procs"), "w") as f:
            f.write(str(self.process.pid))

        cgroup_path = f"/sys/fs/cgroup/cpu/{self.name}"
        os.makedirs(cgroup_path, exist_ok=True)
        with open(os.path.join(cgroup_path, "cpu.shares"), "w") as f:
            f.write(str(self.cpu_shares))
        with open(os.path.join(cgroup_path, "cgroup.procs"), "w") as f:
            f.write(str(self.process.pid))

    def status(self):
        if self.process is not None and self.process.is_alive():
            return f"VM {self.name} is running"
        else:
            return f"VM {self.name} is stopped"

class Hypervisor:
    def __init__(self):
        self.vms = {}

    def create_vm(self, name, disk_path, memory_limit, cpu_shares):
        if name in self.vms:
            raise RuntimeError(f"VM {name} already exists")

        vm = VirtualMachine(name, disk_path, memory_limit, cpu_shares)
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
