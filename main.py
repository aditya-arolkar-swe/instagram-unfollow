#!/usr/bin/env python3
"""
Instagram Unfollow Script
Automatically unfollows users who don't follow you back.
"""

from instagrapi import Client
import time
import random
from pathlib import Path

# Session file to save login credentials
SESSION_FILE = Path("session.json")


def login_client() -> Client:
    """
    Login to Instagram using session ID.
    Saves session to file for future use.
    """
    cl = Client()
    
    # Try to load existing session
    if SESSION_FILE.exists():
        try:
            print("Loading saved session...")
            cl.load_settings(SESSION_FILE)
            # Try to get user info to verify session is still valid
            try:
                cl.user_id
                print(f"✓ Session loaded successfully!")
                return cl
            except:
                print("Session expired, need to login again.")
        except Exception as e:
            print(f"Could not load session: {e}")
    
    # Interactive login with session ID
    print("\n=== Instagram Login ===")
    print("\nTo find your session ID:")
    print("1. Open instagram.com in your browser and log in")
    print("2. Open Developer Tools (Cmd+Option+I on Mac, Ctrl+Shift+I on Windows/Linux)")
    print("3. Go to Application tab (Chrome/Edge) or Storage tab (Firefox)")
    print("4. Navigate to Cookies → https://www.instagram.com")
    print("5. Find the 'sessionid' cookie and copy its value")
    print("\n⚠️  Important: Only use your own session ID. Never share it with others.")
    
    session_id = input("\nEnter your Instagram session ID: ").strip()
    
    if not session_id:
        raise ValueError("Session ID cannot be empty.")
    
    try:
        print("\nLogging in...")
        cl.login_by_sessionid(sessionid=session_id)
        print("✓ Login successful!")
        
        # Save session for future use
        cl.dump_settings(SESSION_FILE)
        print(f"✓ Session saved to {SESSION_FILE}")
        
    except Exception as e:
        print(f"✗ Login failed: {e}")
        print("\nMake sure your session ID is correct and hasn't expired.")
        raise
    
    return cl


def unfollow_non_followers(cl: Client, dry_run: bool = False):
    """
    Unfollow users who don't follow you back.
    
    Parameters:
    -----------
    cl : Client
        Authenticated Instagram client
    dry_run : bool
        If True, only show what would be unfollowed without actually unfollowing
    """
    print("\n" + "="*60)
    print("FETCHING FOLLOWERS AND FOLLOWING")
    print("="*60)
    
    print("Fetching your followers...")
    followers = cl.user_followers(cl.user_id)
    print(f"✓ Found {len(followers)} followers")
    
    print("Fetching accounts you follow...")
    following = cl.user_following(cl.user_id)
    print(f"✓ Found {len(following)} accounts you follow")
    
    followers_set = set(followers.keys())
    following_set = set(following.keys())
    
    non_followers = following_set - followers_set
    
    print(f"\n📊 Found {len(non_followers)} users who do not follow you back.")
    
    if len(non_followers) == 0:
        print("🎉 Everyone you follow also follows you back!")
        return
    
    # Show list of users to unfollow
    print("\nUsers who don't follow you back:")
    usernames = [following[user_id].username for user_id in non_followers]
    for i, username in enumerate(usernames[:20], 1):  # Show first 20
        print(f"  {i}. @{username}")
    if len(usernames) > 20:
        print(f"  ... and {len(usernames) - 20} more")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE: No users will be unfollowed.")
        return
    
    # Confirm before proceeding
    print(f"\n⚠️  WARNING: This will unfollow {len(non_followers)} users.")
    confirm = input("Do you want to continue? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    print("\n" + "="*60)
    print("UNFOLLOWING USERS")
    print("="*60)
    
    for i, user_id in enumerate(non_followers, 1):
        username = following[user_id].username
        print(f"[{i}/{len(non_followers)}] Unfollowing @{username}...")
        
        try:
            cl.user_unfollow(user_id)
            print(f"  ✓ Unfollowed @{username}")
        except Exception as e:
            print(f"  ✗ Error unfollowing @{username}: {e}")
        
        # Random delay to avoid rate limits (2-5 seconds)
        if i < len(non_followers):  # Don't delay after last user
            delay = random.uniform(2, 5)
            time.sleep(delay)
    
    print("\n" + "="*60)
    print("✓ Finished unfollowing non-followers.")
    print("="*60)


def main():
    """Main function"""
    try:
        # Login
        cl = login_client()
        
        # Ask if user wants dry run
        print("\n" + "="*60)
        print("INSTAGRAM UNFOLLOW SCRIPT")
        print("="*60)
        dry_run_input = input("\nDo you want to do a dry run first? (yes/no) [default: yes]: ").strip().lower()
        dry_run = dry_run_input not in ['no', 'n']
        
        # Unfollow non-followers
        unfollow_non_followers(cl, dry_run=dry_run)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
