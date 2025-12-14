# Instagram Unfollow Script

Automatically unfollows users on Instagram who don't follow you back. 

## Philosophy

You are no one's fanboy, and you shouldn't waste time on social media showing interest in the lives of those who don't reciprocate. However, if you have already made this mistake, unfollowing others can be a time consuming process. Let this script automate everything for you. 

## Usage

```bash
git clone https://github.com/aditya-arolkar-swe/instagram-unfollow.git
cd instagram-unfollow
poetry run python3 main.py
```

The script will prompt you for your Instagram session ID. To find it:

1. Open [instagram.com](https://www.instagram.com) in your browser and log in
2. Open Developer Tools:
   - **Mac**: `Cmd + Option + I`
   - **Windows/Linux**: `Ctrl + Shift + I`
3. Go to the **Application** tab (Chrome/Edge) or **Storage** tab (Firefox)
4. Navigate to: **Cookies → https://www.instagram.com**
5. Find the cookie named **`sessionid`** and copy its **Value**

⚠️ **Important**: Only use your own session ID. Never share it with others.

## How to Find Session ID (Alternative Method)

If the cookie doesn't appear in the Application tab:

1. Open Developer Tools → **Network** tab
2. Refresh the page
3. Click any request to instagram.com
4. Go to **Headers**
5. Look under **Request Headers** for `cookie: sessionid=...`

The session will be saved automatically for future use.
