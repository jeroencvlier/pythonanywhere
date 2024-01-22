import subprocess

# Define the remote server and rsync command
remote_server = "user@remote_server:/path/to/source"
rsync_command = [
    "rsync",
    "-avz",  # Add rsync options as needed (e.g., -a for archive mode, -v for verbose)
    "--progress",  # Show progress during transfer
    remote_server,
    "/path/to/destination",
]

try:
    # Run the rsync command
    result = subprocess.run(rsync_command, capture_output=True, text=True, check=True)

    # Get the standard output and standard error
    stdout = result.stdout
    stderr = result.stderr

    # Print the standard output and standard error
    print("Rsync Output:")
    print(stdout)
    print("Rsync Error (if any):")
    print(stderr)

    # Get available space on the cloud disk
    df_command = ["df", "-h", "/path/to/cloud/disk"]
    df_result = subprocess.run(df_command, capture_output=True, text=True, check=True)

    # Get available space from df command output
    available_space = df_result.stdout.splitlines()[1].split()[3]

    # Print available space
    print(f"Available space on cloud disk: {available_space}")

except subprocess.CalledProcessError as e:
    # Handle any errors here
    print("Error:")
    print(e.stderr)

except Exception as e:
    print("An error occurred:")
    print(str(e))
    
    
    
import shutil

# Replace '/' with the path of the disk you want to check, e.g., 'C:\\' on Windows
total, used, free = shutil.disk_usage("/home/jeroencvlier")

print("Total: %d GiB" % (total // (2**30)))
print("Used: %d GiB" % (used // (2**30)))
print("Free: %d GiB" % (free // (2**30)))

