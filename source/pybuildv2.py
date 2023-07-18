import os
import json
import sys

json_filename = "buildspec.json"
prefix = " -"

def pressToClose():
    input("\nPress Enter to close this window.")
    sys.exit()

def pr(*message):
    i = str(prefix) + " "
    for msg in message:
        i += msg + " "
    print(i)

# Loading json buildspec file
if os.path.exists(json_filename):
    build_dict = json.loads(open(json_filename, 'r').read())
else:
    dict = {"name": "NAME", "icon": "NONE", "console": True, "onefile": True, "file": "ABSOLUTE_PATH", "add-data": ["ABSOLUTE_PATH;."]}
    with open(json_filename, "w") as file:
        json.dump(dict, file)
    print('Edit the', json_filename, "to use this program correctly!")
    pressToClose()



def generating_command(dict):
        add_data = ""
        for file in dict['add-data']:
            add_data += ' --add-data "{}"'.format(file)

        if not dict['icon']:
            icon = ''
        else:
            icon = ' --icon "{}"'.format(dict['icon'])

        if not dict['name']:
            name = ''
        else:
            name = ' --name "{}"'.format(dict['name'])

        if dict['console']:
            console = 'console'
        else:
            console = 'windowed'

        file = '  ' + dict['file']

        is_onefile = dict["onefile"]
        #print(onefile_index)

        if is_onefile:
            onefile = "onefile"
        else:
            onefile = "onedir"

        return f'pyi-makespec --{onefile} --{console}{icon}{name}{add_data}{file}'

if __name__ == "__main__":

    specfilename = f'{build_dict["name"]}.spec'

    if os.path.exists(specfilename):
        inLoop = True
        pr('{} already exists. Rewrite (y/n) or Build (b)?'.format(specfilename))
        while inLoop:
            ans = input("(b/y/n) ")

            if ans.lower() != "y" and ans.lower() != "n" and ans.lower() != "b":
                continue
            else:
                if ans.lower() == "y":
                    break
                elif ans.lower() == "n":
                    sys.exit()
                elif ans.lower() == "b":
                    pr('Building', specfilename)
                    os.system("pyinstaller " + specfilename)
                    pr('Finished building', specfilename + "!")
                    pressToClose()


    pr('Getting command for', specfilename)
    cmd = generating_command(build_dict)
    pr('Making', specfilename)
    os.system(cmd)
    print()
    pr("Finished", specfilename + "!")
    pressToClose()
