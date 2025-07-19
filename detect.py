import json
import os

import browser_paths


def detect_browsers() -> dict[str, str]:
    """Detect which browsers are installed on the user's computer.

    Args:
        paths: Dictionary of browser names to their Local State paths

    Returns:
        Dictionary of browser names to their valid Local State paths
    """
    paths = browser_paths.get_local_state_path()
    valid_browsers = {}
    for browser, local_state_path in paths.items():
        if os.path.exists(local_state_path):
            valid_browsers[browser] = {
                "local_state_path": local_state_path,
                "executable_path": browser_paths.get_browser_executable_path(browser),
            }
    return valid_browsers


def load_profiles(local_state_path: str) -> dict[str, dict[str, str]]:
    """Load profiles from the Local State file."""
    if not os.path.exists(local_state_path):
        raise FileNotFoundError(f"Local State file not found at: {local_state_path}")

    with open(local_state_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    profiles = data.get("profile", {}).get("info_cache", {})
    return profiles


def print_profiles(profiles: dict[str, dict[str, str]], browser_name: str) -> None:
    """Print the available profiles in a formatted way."""
    print(f'\n📂 Available "{browser_name}" Profiles:')
    for idx, (profile_dir, info) in enumerate(profiles.items()):
        name = info.get("name", "N/A")
        user_name = info.get("user_name", "N/A")
        print(f"[{idx}] {profile_dir} → {name} ({user_name})")


def main():
    try:
        browsers = detect_browsers()
        for browser, info in browsers.items():
            local_state_path = info["local_state_path"]
            print(f"Local State found for {browser}: {local_state_path}")
            profiles = load_profiles(local_state_path)
            print_profiles(profiles, browser)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
