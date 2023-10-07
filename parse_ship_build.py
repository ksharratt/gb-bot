import pandas as pd
import textwrap
from tabulate import tabulate

text = """
###Marshal Crux - Carrier
##"White Flashing" Integrated Armory
  #System Automated Maintenance Lv.1
##Integrated Aircraft Hangar
  #System Automated Maintenance Lv.1
  #Aircraft Lock-on Warning Lv.5
  #Rearmament Acceleration Lv.5
  #Aircraft Maintenance Acceleration Lv.5
  #Airborne Weapon Maintenance Lv.5
##Additional Aircraft System
  #Rearmament Acceleration Lv.5
  #Battlefield Radar Enhancement Lv.1
  #Airborne Weapon Maintenance Lv.4
##Armor System
  #Armor Rigidity Enhancement Lv.5
  #Armor Hardening Process Lv.5
  #Kernel Structure Enhancement II Lv.7
  #Welding Tech Enhancement II Lv.7
##Propulsion System
  #System Failure Lv.1
##Command System
  #Focus Fire Lv.1
  #Strategic Strike II Lv.1
  #System Automated Maintenance Lv.1
"""

lines = text.strip().split('\n')
systems = []
modules = []
data = []

for line in lines:
    if line.startswith('###'):
        ship_name = line[3:].strip()
    elif line.startswith('##'):
        ship_system = line[2:].strip()
    elif line.startswith('  #'):
        # split subheading and level
        ship_module, module_level  = line[3:].rsplit(' ', 1)
        # remove 'Lv.' from level and convert to integer
        systems.append(ship_system)
        modules.append(ship_module)
        module_level = int(module_level.replace('Lv.', ''))
        data.append(module_level)

# Assuming 'modules' is a list of module names
wrapped_modules = [textwrap.fill(module, width=20) for module in modules]

# Print wrapped modules
for wrapped_module in wrapped_modules:
    print(wrapped_module)

# Create DataFrame with 'System', 'Module', and 'Level' columns
df = pd.DataFrame({'System': systems, 'Module': modules, 'Level': data})

# Set 'System' and 'Module' as index
df.set_index(['System', 'Module'], inplace=True)

# Add an extra level of indexing
df['Data'] = ''
df.set_index('Data', append=True, inplace=True)

# Transpose DataFrame
df = df.T



# Print DataFrame
print(df)


# Assuming df is your DataFrame
# Split column names with line breaks
# df.columns = df.columns.str.split('\n')

# Convert DataFrame to a list of lists
data = df.values.tolist()

# Get the header row from the DataFrame
header = df.columns.to_list()

# Format the table using tabulate
table = tabulate(data, headers=header, tablefmt='fancy_grid')

# Print the formatted table
print(table)