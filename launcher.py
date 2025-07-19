import subprocess

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uvicorn

import browser_paths
import config
from detect import detect_browsers, load_profiles


class ProfileRequest(BaseModel):
    browser: str


class LaunchRequest(BaseModel):
    url: str
    browser: str
    profiles: list[str]


app = FastAPI()


@app.get("/browsers")
async def get_browsers(authorization: str = Header(None)):
    """Get the list of detected browsers."""
    if authorization != f"Bearer {config.SECRET_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    browsers = detect_browsers()
    return {"browsers": list(browsers.keys())}


@app.get("/profiles")
async def get_profiles(payload: ProfileRequest, authorization: str = Header(None)):
    if authorization != f"Bearer {config.SECRET_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    browser = payload.browser
    if browser not in detect_browsers():
        raise HTTPException(status_code=404, detail="Browser not found")

    return {
        "profiles": list(
            load_profiles(browser_paths.get_local_state_path().get(browser, "")).keys()
        )
    }


@app.post("/open")
async def open_url(payload: LaunchRequest, authorization: str = Header(None)):
    if authorization != f"Bearer {config.SECRET_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    url = payload.url
    browser = payload.browser
    profiles = payload.profiles

    if browser not in detect_browsers():
        raise HTTPException(status_code=404, detail="Browser not found")

    if not profiles:
        raise HTTPException(status_code=400, detail="Profiles must be specified")

    available_profiles = load_profiles(
        browser_paths.get_local_state_path().get(browser, "")
    ).keys()
    invalid_profiles = [
        profile for profile in profiles if profile not in available_profiles
    ]

    if invalid_profiles:
        raise HTTPException(
            status_code=400, detail=f"Invalid profiles: {', '.join(invalid_profiles)}"
        )

    browser_path = browser_paths.get_browser_executable_path(browser)

    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    for profile in profiles:
        subprocess.Popen([browser_path, f"--profile-directory={profile}", url])

    return {
        "status": "opened",
        "url": url,
        "browser_executable": browser_path,
    }


if __name__ == "__main__":
    uvicorn.run("launcher:app", host="0.0.0.0", port=5005, reload=True)
