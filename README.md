# Instagram-Automation

This repository contains a Python script for automating various actions on Instagram using the `seleniumbase` library. The script can perform tasks such as logging in, following users, sending direct messages, interacting with content on the Explore page, and unfollowing users.

## Features
*   **Automated Login:** Logs into your Instagram account.
*   **Session Persistence:** Uses a user data directory to maintain your login session between runs.
*   **Follow Users:** Follows users from a specified list. It keeps track of accounts it has already attempted to follow to avoid duplicates.
*   **Send Direct Messages:** Sends randomized direct messages to users from a specified list, avoiding users who have already been contacted.
*   **Explore Page Interaction:** Navigates the Explore page, browses content, and randomly likes or comments on posts to simulate human behavior.
*   **Automated Unfollowing:** Periodically (once every 24 hours) unfollows users from your "Following" list.
*   **Human-like Behavior:** Incorporates randomized delays and actions to reduce the risk of detection.

## Prerequisites
*   Python 3
*   A compatible web browser (e.g., Google Chrome)

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abdulrehman9092/instagram-automation.git
    cd instagram-automation
    ```

2.  **Install the required Python library:**
    ```bash
    pip install seleniumbase
    ```
    The script uses `undetected-chromedriver`, which `seleniumbase` will handle automatically.

3.  **Configure the `Insta.py` script:**
    Open the `Insta.py` file and modify the following sections:

    *   **Login Credentials:** Set your Instagram username and password.
        ```python
        USERNAME = "Your Username"
        PASSWORD = "Your Pass"
        ```

    *   **User Data Directory:** Change the path for `user_data_dir` to a folder on your local machine. This is crucial for saving your login session.
        ```python
        # In the main() function
        with SB(cft=True, user_data_dir=r"C:\path\to\your\user_data_folder", uc=True, test=True) as sb:
        ```

    *   **Target Users for Following:** Add the usernames you want to follow in the `follow` function.
        ```python
        # In the follow() function
        username_list = """
            target_user_1
            target_user_2
            target_user_3
            """
        ```

    *   **Target Users for Messaging:** Add the usernames you want to message in the `message` function.
        ```python
        # In the message() function
        username_list = """
            another_user_1
            another_user_2
            another_user_3
            """
        ```

    *   **Customize Messages:** (Optional) You can edit the list of random messages in the `message` function.
        ```python
        # In the message() function
        MESSAGE_TEXT = ["Your custom message 1", "Your custom message 2", "..."]
        ```

    *   **Set Your Profile for Unfollowing:** In the `unfollow` function, replace `"yourusername"` with your actual Instagram username.
        ```python
        # In the unfollow() function
        sb.open("https://www.instagram.com/yourusername/")
        ```

## Usage

Once the setup is complete, run the script from your terminal:
```bash
python Insta.py
```
The script will open a browser window, log you in (if a session is not already active), and begin its main loop of automated actions: follow -> message -> explore. The unfollow action is set to run once every 24 hours.

## How It Works

*   **Main Loop:** The script operates in an infinite loop that sequentially calls the `follow`, `message`, and `explore` functions. An `unfollow` task is triggered once every 24 hours.
*   **Action Tracking:** The `follow` and `message` functions create `dead_follow.txt` and `dead_usernames.txt` respectively. These files store the usernames of accounts that have been processed, ensuring the script doesn't interact with the same user repeatedly across multiple runs.
*   **Explore Interaction:** The `explore` function injects a complex JavaScript payload to navigate the Explore feed. It simulates human-like browsing by randomly liking (9% probability) and commenting (20% probability) on posts.
*   **Unfollowing:** The `unfollow` function navigates to your own profile, opens the "Following" list, and programmatically clicks the "Following" and then "Unfollow" buttons for users in the list.

## Disclaimer

Automating social media interactions is against the terms of service of many platforms, including Instagram. Use this script at your own risk. The developer of this repository is not responsible for any consequences, such as account suspension or banning, that may result from its use. It is recommended to use this script cautiously and with conservative settings to minimize risks.
