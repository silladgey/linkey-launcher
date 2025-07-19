import platform
import os

# Executable paths for various browsers on different operating systems
CHROME_WIN_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_MAC_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_LINUX_PATH = "google-chrome"
CHROMIUM_WIN_PATH = r"C:\Program Files (x86)\Chromium\Application\chrome.exe"
CHROMIUM_MAC_PATH = "/Applications/Chromium.app/Contents/MacOS/Chromium"
CHROMIUM_LINUX_PATH = "chromium-browser"
BRAVE_WIN_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
BRAVE_MAC_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
BRAVE_LINUX_PATH = "brave-browser"

# Local State file paths for various browsers on different operating systems
CHROME_WIN_LS_PATH = r"%LOCALAPPDATA%\Google\Chrome\User Data\Local State"
CHROME_MAC_LS_PATH = "~/Library/Application Support/Google/Chrome/Local State"
CHROME_LINUX_LS_PATH = "~/.config/google-chrome/Local State"
CHROMIUM_WIN_LS_PATH = r"%LOCALAPPDATA%\Chromium\User Data\Local State"
CHROMIUM_MAC_LS_PATH = "~/Library/Application Support/Chromium/Local State"
CHROMIUM_LINUX_LS_PATH = "~/.config/chromium/Local State"
BRAVE_WIN_LS_PATH = r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Local State"
BRAVE_MAC_LS_PATH = (
    "~/Library/Application Support/BraveSoftware/Brave-Browser/Local State"
)
BRAVE_LINUX_LS_PATH = "~/.config/BraveSoftware/Brave-Browser/Local State"


class UnsupportedOSException(Exception):
    """Custom exception for unsupported operating systems."""

    def __init__(self, message):
        super().__init__(message)


def get_browser_executable_path(browser: str) -> str:
    """Get the executable path for a specific browser."""
    system = platform.system()

    if system == "Windows":
        if browser == "chrome":
            return CHROME_WIN_PATH
        elif browser == "chromium":
            return CHROMIUM_WIN_PATH
        elif browser == "brave":
            return BRAVE_WIN_PATH
    elif system == "Darwin":
        if browser == "chrome":
            return CHROME_MAC_PATH
        elif browser == "chromium":
            return CHROMIUM_MAC_PATH
        elif browser == "brave":
            return BRAVE_MAC_PATH
    elif system == "Linux":
        if browser == "chrome":
            return CHROME_LINUX_PATH
        elif browser == "chromium":
            return CHROMIUM_LINUX_PATH
        elif browser == "brave":
            return BRAVE_LINUX_PATH

    raise UnsupportedOSException("Unsupported OS or browser")


def get_local_state_path() -> dict[str, str]:
    """Get the local state path for different browsers based on the OS."""
    system = platform.system()
    paths = {}

    if system == "Windows":
        paths["chrome"] = os.path.expandvars(CHROME_WIN_LS_PATH)
        paths["chromium"] = os.path.expandvars(CHROMIUM_WIN_LS_PATH)
        paths["brave"] = os.path.expandvars(BRAVE_WIN_LS_PATH)
    elif system == "Darwin":
        paths["chrome"] = os.path.expanduser(CHROME_MAC_LS_PATH)
        paths["chromium"] = os.path.expanduser(CHROMIUM_MAC_LS_PATH)
        paths["brave"] = os.path.expanduser(BRAVE_MAC_LS_PATH)
    elif system == "Linux":
        paths["chrome"] = os.path.expanduser(CHROME_LINUX_LS_PATH)
        paths["chromium"] = os.path.expanduser(CHROMIUM_LINUX_LS_PATH)
        paths["brave"] = os.path.expanduser(BRAVE_LINUX_LS_PATH)
    else:
        raise UnsupportedOSException("Unsupported OS")

    return paths
