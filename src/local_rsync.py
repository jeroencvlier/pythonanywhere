import subprocess
from utils import fetch_weeks_cloud
import telegram_bot


def local_rsync():
    last_week = False
    cloud_weeks = fetch_weeks_cloud(last_week)

    for week in cloud_weeks:
        message = f"Pulling Option Data for {cloud_weeks}!\n"
        try:
            result = subprocess.call(
                [
                    "rsync",
                    "-avzhe",
                    "ssh",
                    "jeroencvlier@ssh.pythonanywhere.com:/home/jeroencvlier/option_chain_data/"
                    + week
                    + "/",
                    "/Users/jeroenvanlier/Documents/Github/TOS_predition/option_chain_data",
                ],
                capture_output=True,
                text=True,
            )
            output = result.stdout

            # Parse the output for the total number of files transferred
            for line in output.split("\n"):
                if "Number of regular files transferred" in line:
                    total_files = int(line.split(":")[1].strip())
                    message += f"Total files transferred: {total_files}\n\n"

        except Exception as error:
            message += f"Error: " + str(error.stderr)[:200] + "\n\n"

    telegram_bot.send_mess(message)


if __name__ == "__main__":
    local_rsync()
