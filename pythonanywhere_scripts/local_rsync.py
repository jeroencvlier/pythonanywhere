import subprocess
import logging
from pythonanywhere_scripts import telegram_bot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def local_rsync():
    try:
        list_of_options_per_week_on_cloud = subprocess.check_output(
            [
                "ssh",
                "jeroencvlier@ssh.pythonanywhere.com",
                "ls",
                "/home/jeroencvlier/option_chain_data/",
            ]
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to list directories: {e}")
        telegram_bot.send_mess(
            "Failed to initiate data sync: could not list directories on remote server."
        )

    list_of_options_per_week_on_cloud = [
        x for x in list_of_options_per_week_on_cloud.decode().split() if "_week_" in x
    ]

    if not list_of_options_per_week_on_cloud:
        logging.info("No directories found for sync.")
        telegram_bot.send_mess("No directories found for sync.")

    total_files = 0
    # list_of_options_per_week_on_cloud = [list_of_options_per_week_on_cloud[-1]]
    message = "Data Sync with PythonAnywhere to local:\n\n"
    for week in sorted(list_of_options_per_week_on_cloud, reverse=True):
        logging.info(f"Pulling Option Data for {week}!")
        try:
            result = subprocess.run(
                [
                    "rsync",
                    "-avzhe",
                    "ssh",
                    "jeroencvlier@ssh.pythonanywhere.com:/home/jeroencvlier/option_chain_data/"
                    + week
                    + "/",
                    "/Users/jeroenvanlier/Documents/Github/TOS_predition/option_chain_data",
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Parsing rsync output for the number of files transferred
            week_file_count = 0

            for line in result.stdout.split("\n"):
                if line.strip().endswith(".json.gz"):
                    week_file_count += 1
                    total_files += 1
                if line.startswith("total size is"):
                    replaced_line = line.replace("total size is ", "").strip()
                    parsed_line = replaced_line.split(" ")[0]

            message += f"Synced {week}:\n"
            message += f"Total size: {parsed_line}\n"
            message += f"Files: {week_file_count}\n\n"

        except subprocess.CalledProcessError as e:
            logging.error(f"Rsync failed for {week}: {e}")
            message += f"\n\nError {week}: " + str(e)[:200] + "\n\n"

    message += f"Total files Synced: {total_files}"

    telegram_bot.send_mess(message)
