import streamlit as st
import os
import subprocess
import psutil
import platform
import socket
from datetime import datetime

def get_system_info():
    """Collect and return system information."""
    try:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        st.error(f"Error getting system info: {e}")
        return {}

def get_system_resources():
    """Collect and return system resource usage."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu_percent,
            "memory": {
                "percent": memory.percent,
                "used_gb": memory.used / (1024**3),
                "total_gb": memory.total / (1024**3)
            },
            "disk": {
                "percent": disk.percent,
                "used_gb": disk.used / (1024**3),
                "total_gb": disk.total / (1024**3)
            },
            "network": {
                "hostname": socket.gethostname(),
                "ip_address": socket.gethostbyname(socket.gethostname())
            }
        }
    except Exception as e:
        st.error(f"Error getting system resources: {e}")
        return {}

def show_windows_automation():
    """Display the Windows Automation interface in the Streamlit app."""
    st.title("🪟 Windows Automation")
    st.write("Automate common Windows tasks and get system information.")
    
    # System Information
    with st.expander("📊 System Information", expanded=True):
        sys_info = get_system_info()
        if sys_info:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("OS", sys_info["os"])
                st.metric("OS Version", sys_info["os_version"])
                st.metric("Hostname", sys_info["hostname"])
            
            with col2:
                st.metric("Processor", sys_info["processor"])
                st.metric("Architecture", sys_info["architecture"])
                st.metric("IP Address", sys_info["ip_address"])
    
    # System Resources
    with st.expander("📈 System Resources", expanded=True):
        resources = get_system_resources()
        if resources:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("CPU Usage", f"{resources['cpu_percent']}%")
                
                # Memory Gauge
                mem = resources['memory']
                st.metric("Memory Usage", 
                         f"{mem['percent']}%", 
                         f"{mem['used_gb']:.1f} GB / {mem['total_gb']:.1f} GB")
            
            with col2:
                # Disk Gauge
                disk = resources['disk']
                st.metric("Disk Usage",
                         f"{disk['percent']}%",
                         f"{disk['used_gb']:.1f} GB / {disk['total_gb']:.1f} GB")
                
                # Network Info
                net = resources['network']
                st.metric("Network", net["ip_address"])
    
    # System Commands
    with st.expander("⚙️ System Commands", expanded=True):
        st.subheader("Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Open Notepad", use_container_width=True):
                try:
                    subprocess.Popen('notepad.exe')
                    st.success("Opened Notepad")
                except Exception as e:
                    st.error(f"Failed to open Notepad: {e}")
            
            if st.button("📁 Open File Explorer", use_container_width=True):
                try:
                    subprocess.Popen('explorer')
                    st.success("Opened File Explorer")
                except Exception as e:
                    st.error(f"Failed to open File Explorer: {e}")
        
        with col2:
            if st.button("🌐 Open Web Browser", use_container_width=True):
                try:
                    subprocess.Popen('start chrome' if 'chrome' in [p.name().lower() for p in psutil.process_iter(attrs=['name'])] else 'start msedge')
                    st.success("Opened Web Browser")
                except Exception as e:
                    st.error(f"Failed to open Web Browser: {e}")
            
            if st.button("📊 Open Task Manager", use_container_width=True):
                try:
                    subprocess.Popen('taskmgr')
                    st.success("Opened Task Manager")
                except Exception as e:
                    st.error(f"Failed to open Task Manager: {e}")
        
        with col3:
            if st.button("📸 Take Screenshot", use_container_width=True):
                try:
                    import pyautogui
                    screenshot = pyautogui.screenshot()
                    screenshot_path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    screenshot.save(screenshot_path)
                    st.image(screenshot, caption="Screenshot")
                    st.success(f"Screenshot saved as {screenshot_path}")
                except Exception as e:
                    st.error(f"Failed to take screenshot: {e}")
    
    # Power Options
    with st.expander("🔌 Power Options", expanded=False):
        st.warning("⚠️ Use with caution!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🛑 Shutdown Computer", type="primary", use_container_width=True):
                if st.warning("Are you sure you want to shut down the computer?"):
                    try:
                        os.system("shutdown /s /t 1")
                    except Exception as e:
                        st.error(f"Failed to initiate shutdown: {e}")
        
        with col2:
            if st.button("🔄 Restart Computer", type="primary", use_container_width=True):
                if st.warning("Are you sure you want to restart the computer?"):
                    try:
                        os.system("shutdown /r /t 1")
                    except Exception as e:
                        st.error(f"Failed to initiate restart: {e}")
    
    # Add some spacing at the bottom
    st.write("")
    st.info("ℹ️ Note: Some features may require administrator privileges to work properly.")

show_windows_automation()
