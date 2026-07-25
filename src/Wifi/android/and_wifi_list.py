import subprocess

# Android stores Wi-Fi profiles in a configuration file (requires root)
cmd = "su -c 'cat /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml'"
try:
    result = subprocess.check_output(cmd, shell=True).decode()
    print(result)
except subprocess.CalledProcessError as e:
    print("Failed to fetch Wi-Fi data. Ensure Termux has root permissions.")
  
