import psutil


# Function to get process ID by name
def get_process_id(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            return proc.info['pid']
    return None

# Function to get base address
def get_base_address(process_name):
    pid = get_process_id(process_name)
    if not pid:
        print("Process not found.")
        return
    
    process = psutil.Process(pid)
    base_address = process.memory_maps()[0].addr
    print(f"Base Address of {process_name}: {hex(base_address)}")


for proc in psutil.process_iter(['pid', 'name']):
    print(proc.info)  # Prints all running processes
# user input name
name = input("Enter name of process: ")
# Example usage
get_base_address(name)
