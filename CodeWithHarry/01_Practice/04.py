# list os content

import os 
directory_path= "/users/rachitgarg"

content = os.listdir(directory_path)

for item in content:
    print(item)