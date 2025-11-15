import subprocess
import sys
import os
import shutil

def setup_and_run():
    """
    Creates a virtual environment, activates it, installs requirements, and runs uvicorn.
    """
    venv_path = ".venv"
    
    # Check if virtual environment already exists and remove it
    if os.path.exists(venv_path):
        print(f"Virtual environment '{venv_path}' already exists. Removing it...")
        shutil.rmtree(venv_path)
        print("Cleanup complete.")
    
    # Create virtual environment
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    
    # Determine the python executable in the virtual environment
    if os.name == "nt":  # Windows
        python_executable = os.path.join(venv_path, "Scripts", "python.exe")
        pip_executable = os.path.join(venv_path, "Scripts", "pip.exe")
        acivate_script = os.path.join(venv_path, "Scripts", "activate.bat")
    else:  # Unix/Linux/Mac
        python_executable = os.path.join(venv_path, "bin", "python")
        pip_executable = os.path.join(venv_path, "bin", "pip")
        acivate_script = os.path.join(venv_path, "bin", "activate")
        
    # Activate the virtual environment
    print(f"Activating virtual environment using {acivate_script}...")
    subprocess.run([acivate_script], shell=True, check=True)

    # Upgrade pip
    print("Upgrading pip...")
    subprocess.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # Install requirements
    print("Installing requirements...")
    subprocess.run([pip_executable, "install", "-r", "requirements.txt"], check=True)
    
    # Deactivate the virtual environment
    print("Deactivating virtual environment...")
    subprocess.run(["deactivate"], shell=True, check=True)

    # create .env file template if not exists
    print("Creating .env file template if not exists...")
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"Creating {env_file} file...")
        with open(env_file, "w") as f:
            f.write("LLM_API_KEY=your_llm_api_key\n")
            f.write("LLM_MODEL_NAME=your_llm_model_name\n")
            f.write("SECRET_KEY=your_secret_key\n")
            f.write("DEBUG=True\n")
        print(f"{env_file} file created.")
        # securely generate a random SECRET_KEY and update the .env file
        import secrets
        secret_key = secrets.token_urlsafe(32)
        with open(env_file, "a") as f:
            f.write(f"SECRET_KEY={secret_key}\n")
        print("A secure random SECRET_KEY has been generated and added to the .env file.")
        print("Please update the other values in the .env file as needed.")
    else:
        print(f"{env_file} file already exists. Skipping creation.")  

    print("\nSetup complete!")
    print("To activate the virtual environment manually, run:")
    if os.name == "nt":
        print(f"    {venv_path}\\Scripts\\activate")
    else:
        print(f"    source {venv_path}/bin/activate")
    
    print("To run the FastAPI application, use:")
    print(f"{python_executable} -m uvicorn main:app --reload")
    print("Visit https://localhost:8000/docs to access the API documentation.")
    # Run uvicorn
    # print("Starting uvicorn server...")
    # subprocess.run([python_executable, "-m", "uvicorn", "main:app", "--reload"], check=True)

if __name__ == "__main__":
    setup_and_run()