import modal

image = modal.Image.debian_slim().pip_install(
    "streamlit",
    "pandas", 
    "plotly",
    "supabase"
)

app = modal.App("cage-matcher")

@app.function(
    image=image,
    secrets=[modal.Secret.from_name("my-supabase-secret")],
    timeout=600,
)
@modal.web_server(8000)
def run():
    import subprocess
    import sys
    import os
    
    # Check what files are available
    print("Current directory:", os.getcwd())
    print("Files in directory:", os.listdir('.'))
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "app.py",
        "--server.port=8000",
        "--server.enableCORS=false", 
        "--server.enableXsrfProtection=false",
        "--server.headless=true",
        "--browser.serverAddress=0.0.0.0"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    app.serve()