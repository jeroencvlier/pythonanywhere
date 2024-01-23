import os
import shutil
from src.utils import fetch_weeks_cloud


def create_test_files():
    # Create a temporary directory for testing
    temp_dir = "/tmp/test_option_chain_data"
    os.makedirs(temp_dir, exist_ok=True)

    # Create some test files with "_week_" in their names
    test_folders = [
        "2023_week_52",
        "2024_week_01",
        "2024_week_02",
        "2024_week_03",
    ]
    for folder in test_folders:
        os.makedirs(os.path.join(temp_dir, folder), exist_ok=True)
    return temp_dir, test_folders


def test_fetch_last_week():
    temp_dir, _ = create_test_files()

    # Call the fetch_last_week function
    last_week = True
    result_week = fetch_weeks_cloud(last_week, temp_dir)

    # Assert that the result is the latest week file
    assert result_week == "2024_week_03"

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


def test_fetch_last_weeks():
    temp_dir, test_folders = create_test_files()

    # Call the fetch_last_week function
    last_week = False
    result_week = fetch_weeks_cloud(last_week, temp_dir)

    # Assert that the result is the latest week file
    assert result_week == sorted(test_folders, reverse=True)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
