import psutil
import platform
import socket
import time
import os
import re
from datetime import datetime, timedelta


REFRESH_INTERVAL = 30 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 


def get_cpu_info():
    freq_mhz = psutil.cpu_freq().current if psutil.cpu_freq() else None
    return {
        "cores": psutil.cpu_count(logical=True),
        "freq": freq_mhz, 
        "usage": psutil.cpu_percent(interval=0.1) 
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "used_gb": mem.used / (1024**3),
        "total_gb": mem.total / (1024**3),
        "percent": mem.percent
    }

def get_system_info():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = time.time() - psutil.boot_time()
    return {
        "machine": platform.node(),
        "os": platform.platform(),
        "boot_time": boot_time,
        "uptime": uptime_seconds,
        "users": len(psutil.users()),
        "ip": socket.gethostbyname(socket.gethostname())
    }

def get_process_info():
    processes = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(p.info)
        except psutil.NoSuchProcess:
            pass
    top3 = sorted(processes, key=lambda x: x.get("cpu_percent", 0), reverse=True)[:3]
    return processes, top3

def analyze_folder(path):
    exts = {"txt": 0, "py": 0, "pdf": 0, "jpg": 0}
    total_files = 0
    
    if not os.path.isdir(path):
        percentages = {k: 0 for k in exts.keys()}
        return exts, percentages, total_files

    for root, dirs, files in os.walk(path):
        for f in files:
            total_files += 1
            ext = f.split('.')[-1].lower() 
            if ext in exts:
                exts[ext] += 1
    
    total = sum(exts.values()) 
    percentages = {k: (v / total * 100 if total > 0 else 0) for k, v in exts.items()}
    return exts, percentages, total_files


def get_usage_color(percent):
    percent = float(percent)
    if percent <= 50.0:
        return "green"
    elif percent <= 80.0:
        return "orange"
    else:
        return "red"

def generate_dashboard():

    cpu_data = get_cpu_info()
    mem_data = get_memory_info()
    sys_data = get_system_info()
    processes, top3 = get_process_info()
    folder_path = os.path.join(os.path.expanduser('~'), "Documents")
    file_counts, file_percentages, total_files = analyze_folder(folder_path)

    data = {}

    data["system_hostname"] = sys_data['machine']
    data["system_os_name"] = sys_data['os']
    data["system_uptime"] = str(timedelta(seconds=int(sys_data['uptime']))).split('.')[0]
    data["system_users_count"] = sys_data['users']
    data["network_ip_address"] = sys_data['ip']
    data["system_boot_time"] = sys_data['boot_time'].strftime("%Y-%m-%d %H:%M:%S")

    cpu_usage = cpu_data['usage']
    data["cpu_core_count"] = cpu_data['cores']
    data["cpu_frequency_mhz"] = f"{cpu_data['freq']:.0f}" if cpu_data['freq'] else "N/A"
    data["cpu_usage_percent"] = f"{cpu_usage:.1f}"
    data["cpu_usage_color"] = get_usage_color(cpu_usage)

    mem_percent = mem_data['percent']
    data["memory_total_gb"] = f"{mem_data['total_gb']:.2f}"
    data["memory_used_gb"] = f"{mem_data['used_gb']:.2f}"
    data["memory_usage_percent"] = f"{mem_percent:.1f}"
    data["memory_usage_color"] = get_usage_color(mem_percent)

    process_list_html = ""
    for proc in top3:
        name = proc.get("name", "N/A")
        cpu = f"{proc.get('cpu_percent', 0):.1f}%"
        mem = f"{proc.get('memory_percent', 0):.1f}%"
        process_list_html += f"<tr><td>{name}</td><td>{cpu}</td><td>{mem}</td></tr>\n"
    data["process_list_html"] = process_list_html
    data["process_total_count"] = len(processes)

    data["file_analysis_directory"] = folder_path
    data["files_total_count"] = total_files
    for ext in ["txt", "py", "pdf", "jpg"]:
        count = file_counts.get(ext, 0)
        percent = file_percentages.get(ext, 0)
        data[f"files_{ext}_count"] = count
        data[f"files_{ext}_percent"] = f"{percent:.1f}"

    data["generation_timestamp"] = datetime.now().strftime("%H:%M:%S")
    data["generation_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        template_file_path = os.path.join(BASE_DIR, "template.html")
        with open(template_file_path, "r", encoding="utf-8") as f: 
            template_content = f.read()
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{template_file_path}' est introuvable. Arrêt.")
        return 

    for key, value in data.items():
        template_content = template_content.replace("{{ " + key + " }}", str(value))

    index_file_path = os.path.join(BASE_DIR, "index.html")
    with open(index_file_path, "w", encoding="utf-8") as f:
        f.write(template_content)

    print(f"Dashboard généré avec succès dans {index_file_path} à {data['generation_timestamp']}")


if __name__ == "__main__":
    print("Démarrage du service de monitoring...")
    
    while True:
        generate_dashboard()

        print(f"Attente de {REFRESH_INTERVAL} secondes avant la prochaine génération...")
        time.sleep(REFRESH_INTERVAL)