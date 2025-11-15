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