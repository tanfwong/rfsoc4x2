import vitis
import os

# Create a client object
client = vitis.create_client()

# Set workspace 
workspace = os.path.expanduser('~')+'/workspace'
client.set_workspace(workspace)

# Create platform
