import subprocess
import logging
from pythonanywhere_scripts import telegram_bot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def local_rsync():
    list_of_options_per_week_on_cloud = subprocess.check_output(
        [
            "ssh",
            "jeroencvlier@ssh.pythonanywhere.com",
            "ls",
            "/home/jeroencvlier/option_chain_data/",
        ]
    )
    list_of_options_per_week_on_cloud = [
        x for x in list_of_options_per_week_on_cloud.decode().split() if "_week_" in x
    ]
    total_files = 0
    # list_of_options_per_week_on_cloud = [list_of_options_per_week_on_cloud[-1]]
    message = "Data Sync with PythonAnywhere to local:\n\n"
    for week in sorted(list_of_options_per_week_on_cloud, reverse=True):

        try:
            logging.info    (f"Pulling Option Data for {week}!")
            # result = subprocess.run(
            #     [
            #         "rsync",
            #         "-avzhe",
            #         "ssh",
            #         "jeroencvlier@ssh.pythonanywhere.com:/home/jeroencvlier/option_chain_data/"
            #         + week
            #         + "/",
            #         "/Users/jeroenvanlier/Documents/Github/TOS_predition/option_chain_data",
            #     ],
            #     check=True,
            #     text=True,
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE
            #     )

            # print(result)
            # count = 0
            # for line in result.stdout.split("\n"):
            #     if "upload:" in line:
            #         count += 1

            # # Parse the output for the total number of files transferred
            # for line in result.stdout.split("\n"):
            #     # print("PRINTING LINE")
            #     # print(line)

            #     if "Number of regular files transferred" in line:
            #         print("PRINTING LINE")
            #         week_file_count = int(line.split(":")[1].strip())
            #         total_files += week_file_count
            #         message += f"{week}: {week_file_count} files\n"

        except Exception as error:
            message += f"\n\nError {week}: " + str(error)[:200] + "\n\n"
    message += f"Total files: {total_files}"

    telegram_bot.send_mess(message)


if __name__ == "__main__":
    local_rsync()
