PROXY_USER_DATA =  """#!/bin/bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip python3-venv -y
sudo mkdir -p /home/ubuntu/my_project
sudo chown -R ubuntu:ubuntu /home/ubuntu/my_project/
cd /home/ubuntu/my_project/
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn boto3 ping3 pymysql sshtunnel
"""

LAUNCH_SERVER_COMMAND = """
exec nohup /home/ubuntu/my_project/venv/bin/uvicorn proxy:app --host 0.0.0.0 --port 80  > /home/ubuntu/my_project/uvicorn.log 2>&1 &

"""


VAR_ENV = """
aws_access_key_id="{0}"
aws_secret_access_key="{1}"
aws_session_token="{2}"
"""


def escape_single_quotes(script):
    return script.replace("'", "'\\''")

def get_proxy_user_data(
        aws_access_key_id, 
        aws_secret_access_key, 
        aws_session_token):
    
    proxy_user_data = PROXY_USER_DATA
    var_env_temp = VAR_ENV.format(
        aws_access_key_id, 
        aws_secret_access_key, 
        aws_session_token)
    
    main_script =  escape_single_quotes(var_env_temp + "\n" + open("ressources/proxy/proxy.py", "r").read())
    main_script_creation = f"""
        echo '{main_script}' > /home/ubuntu/my_project/proxy.py
    """
    proxy_user_data += "\n" + main_script_creation + "\n" +  LAUNCH_SERVER_COMMAND
    return proxy_user_data