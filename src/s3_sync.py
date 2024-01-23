import subprocess
import os

# import telegram_bot
from src import telegram_bot


# def count_files_uploaded(output):
#     count = 0
#     lines = output.split("\n")
#     for line in lines:
#         if "upload:" in line:
#             count += 1
#     return count


def count_files_uploaded(output):
    return output.count("upload:")


def fetch_last_week(datapath="/home/jeroencvlier/option_chain_data/"):
    list_of_options_per_week_on_cloud = os.listdir(datapath)
    list_of_options_per_week_on_cloud = [
        x for x in list_of_options_per_week_on_cloud if "_week_" in x
    ]
    list_of_options_per_week_on_cloud = sorted(
        list_of_options_per_week_on_cloud, reverse=True
    )
    latest_week = list_of_options_per_week_on_cloud[0]

    return latest_week


def aws_sync():
    week = fetch_last_week()
    total_files_uploaded = 0
    subprocess_errors = ""
    message = f"Pulling Option Data for {week}!"
    print(message)
    aws_command = [
        "/home/jeroencvlier/.virtualenvs/awssync/bin/aws",
        "s3",
        "sync",
        f"/home/jeroencvlier/option_chain_data/{week}/",
        "s3://option-chain-data-backup/option_chain_data",
        "--size-only",
        "--exclude",
        '"*"',
        "--include",
        "*.json.gz",
        "--profile",
        "default",
    ]

    try:
        result = subprocess.run(
            aws_command,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        total_files_uploaded += count_files_uploaded(result.stdout)

    except subprocess.CalledProcessError as error:
        print("Error:")
        print(error.stderr)
        message += f"\nError: " + str(error.stderr)[:200]

    message = f"Total files uploaded: {total_files_uploaded}"

    return message


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


if __name__ == "__main__":
    # run the script
    message = aws_sync()
    # check storage
    message += storage_check()
    # send telegram message
    telegram_bot.send_mess(message)
