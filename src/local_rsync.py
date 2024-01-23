import subprocess
import telegram_bot


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
    for week in sorted(list_of_options_per_week_on_cloud, reverse=True):
        message = f"Pulling Option Data for {week}!\n"
        try:
            result = subprocess.check_output(
                [
                    "rsync",
                    "-avzhe",
                    "ssh",
                    "jeroencvlier@ssh.pythonanywhere.com:/home/jeroencvlier/option_chain_data/"
                    + week
                    + "/",
                    "/Users/jeroenvanlier/Documents/Github/TOS_predition/option_chain_data",
                ],
            )
            output = result.stdout

            # Parse the output for the total number of files transferred
            for line in output.split("\n"):
                if "Number of regular files transferred" in line:
                    total_files = int(line.split(":")[1].strip())
                    message += f"Total files transferred: {total_files}\n\n"

        except Exception as error:
            message += f"Error: " + str(error)[:200] + "\n\n"

    telegram_bot.send_mess(message)


if __name__ == "__main__":
    local_rsync()
