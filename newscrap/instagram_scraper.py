import instaloader
import pandas as pd
import json
from datetime import datetime
import os
from typing import Dict, List, Optional

class InstagramScraper:
    def __init__(self, config_file: str = 'config.json'):
        """
        Initialize Instagram scraper with credentials from config file
        
        Args:
            config_file: Path to the configuration file
        """
        self.L = instaloader.Instaloader()
        self.config_file = config_file
        self.load_credentials()
        
    def load_credentials(self) -> None:
        """Load credentials from config file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            username = config['instagram']['username']
            password = config['instagram']['password']
            
            if not username or not password:
                print("Please set your Instagram credentials in config.json")
                self.setup_credentials()
            else:
                self.login(username, password)
                
        except FileNotFoundError:
            print("Config file not found. Creating new config file...")
            self.setup_credentials()
        except Exception as e:
            print(f"Error loading credentials: {str(e)}")
            raise
            
    def setup_credentials(self) -> None:
        """Set up new credentials and save to config file"""
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")
        
        config = {
            "instagram": {
                "username": username,
                "password": password
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
            
        self.login(username, password)
        
    def login(self, username: str, password: str) -> None:
        """Login to Instagram"""
        try:
            self.L.login(username, password)
            print("Successfully logged in to Instagram")
        except Exception as e:
            print(f"Failed to login: {str(e)}")
            raise

    def get_profile_info(self, username: str) -> Dict:
        """
        Get profile information for a given username
        
        Args:
            username: Instagram username to scrape
            
        Returns:
            Dictionary containing profile information
        """
        try:
            profile = instaloader.Profile.from_username(self.L.context, username)
            
            data = {
                'username': profile.username,
                'full_name': profile.full_name,
                'biography': profile.biography,
                'followers': profile.followers,
                'following': profile.followees,
                'posts_count': profile.mediacount,
                'is_private': profile.is_private,
                'is_verified': profile.is_verified,
                'external_url': profile.external_url,
                'scraped_at': datetime.now().isoformat()
            }
            
            return data
            
        except Exception as e:
            print(f"Error scraping profile {username}: {str(e)}")
            return None

    def get_posts(self, username: str, max_posts: int = 10) -> List[Dict]:
        """
        Get recent posts from a profile
        
        Args:
            username: Instagram username to scrape
            max_posts: Maximum number of posts to scrape
            
        Returns:
            List of dictionaries containing post information
        """
        try:
            profile = instaloader.Profile.from_username(self.L.context, username)
            posts = []
            
            for post in profile.get_posts():
                if len(posts) >= max_posts:
                    break
                    
                post_data = {
                    'shortcode': post.shortcode,
                    'date': post.date.isoformat(),
                    'caption': post.caption,
                    'likes': post.likes,
                    'comments': post.comments,
                    'is_video': post.is_video,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/"
                }
                
                posts.append(post_data)
                
            return posts
            
        except Exception as e:
            print(f"Error scraping posts for {username}: {str(e)}")
            return []

    def save_data(self, data: Dict, filename: str, format: str = 'json') -> None:
        """
        Save scraped data to file
        
        Args:
            data: Data to save
            filename: Output filename
            format: Output format ('json' or 'csv')
        """
        try:
            if format.lower() == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            elif format.lower() == 'csv':
                df = pd.DataFrame([data])
                df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

def main():
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Initialize scraper (will load credentials from config file)
    scraper = InstagramScraper()
    
    # Get target username to scrape
    target_username = input("Enter the Instagram username to scrape: ")
    
    # Scrape profile information
    profile_data = scraper.get_profile_info(target_username)
    if profile_data:
        # Save profile data
        scraper.save_data(profile_data, f'output/{target_username}_profile.json', 'json')
        scraper.save_data(profile_data, f'output/{target_username}_profile.csv', 'csv')
        
        # Scrape recent posts
        posts = scraper.get_posts(target_username, max_posts=10)
        if posts:
            # Save posts data
            with open(f'output/{target_username}_posts.json', 'w', encoding='utf-8') as f:
                json.dump(posts, f, indent=4, ensure_ascii=False)
            
            # Convert posts to DataFrame and save as CSV
            df_posts = pd.DataFrame(posts)
            df_posts.to_csv(f'output/{target_username}_posts.csv', index=False)
            
            print(f"\nScraped {len(posts)} posts from {target_username}")
        
        print("\nProfile Information:")
        for key, value in profile_data.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main() 