import subprocess
import os
from dotenv import load_dotenv, find_dotenv
import telegram_bot


def aws_sync():
    list_of_options_per_week_on_cloud = os.listdir(
        "/home/jeroencvlier/option_chain_data/"
    )
    list_of_options_per_week_on_cloud = [
        x for x in list_of_options_per_week_on_cloud if "_week_" in x
    ]

    for week in sorted(list_of_options_per_week_on_cloud, reverse=True):
        print(f"Pulling Option Data for {week}!")
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
            subprocess.run(aws_command, check=True, text=True)

        except subprocess.CalledProcessError as e:
            print("Error:")
            print(e.stderr)


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
    telegram_bot.send_message(f"Disk Usage: {percentage_used:.2f}%")


if __name__ == "__main__":
    # load env variables
    load_dotenv(find_dotenv())
    # install requirements
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    # run the script
    aws_sync()
    # check storage
    storage_check()
