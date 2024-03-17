import os
import subprocess

def fetch_weeks_cloud(
    last_week: bool, datapath: str = "/home/jeroencvlier/option_chain_data/"
):
    list_of_options_per_week_on_cloud = os.listdir(datapath)
    list_of_options_per_week_on_cloud = [
        x for x in list_of_options_per_week_on_cloud if "_week_" in x
    ]
    list_of_options_per_week_on_cloud = sorted(
        list_of_options_per_week_on_cloud, reverse=True
    )
    if last_week:
        result_week = [list_of_options_per_week_on_cloud[0]]
    else:
        result_week = list_of_options_per_week_on_cloud

    return result_week


def get_used_space():
    """Get the used disk space in bytes."""
    command = "du -s -B 1 /tmp ~/.[!.]* ~/"
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode != 0:
        print("Error in executing du command")
        return None
    total_used_space = sum(
        int(line.split()[0]) for line in result.stdout.strip().split("\n")
    )
    return total_used_space

def calculate_percentage_used(used_space, total_quota):
    """Calculate the percentage of disk space used."""
    return (used_space / total_quota) * 100


def storage_check():
    total_quota = 10 * 1024 * 1024 * 1024  # 10GB in bytes
    used_space = get_used_space()
    if used_space is not None:
        percentage_used = calculate_percentage_used(used_space, total_quota)
        print(f"Disk Usage: {percentage_used:.2f}%")

    # send telegram message
    return f"\nDisk Usage: {percentage_used:.2f}%"