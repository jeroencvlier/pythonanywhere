import os
import shutil
from src.s3_sync import fetch_last_week
import time


def test_fetch_last_week():
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

    # Call the fetch_last_week function
    result_week = fetch_last_week(temp_dir)

    # Assert that the result is the latest week file
    assert result_week == "2024_week_03"

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
