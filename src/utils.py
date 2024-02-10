import os


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
