import re
import os


def convert(file, newname, prefix):
    with open(file, 'r') as f:
        lines = f.readlines()
        
    file = open("Converted/"+ newname,"w")
    file.write("{% extends '"+prefix+"/base.html' %}\n")
    file.write("{% load static %}\n")

    for line in lines:
        if 'src' in line and not 'http' in line:
            #change src="...." to src="{% static '....' %}"
            line = re.sub(r'src="(.+?)"', r'src="{% static "'+ prefix + r'/\1" %}"', line)

        if 'href' in line and not 'http' in line and not '<a' in line:
            line = re.sub(r'href="(.+?)"', r'href="{% static "' + prefix + r'/\1" %}"', line)
        
        
        file.write(line)
        
    file.close()


def main():
    directory = input("Enter the directory: ")
    prefix = input("Enter the prefix: ")
    os.chdir(directory)
    if not os.path.exists("Converted"):
        os.makedirs("Converted")
    for file in os.listdir():
        if file.endswith(".html"):
            name = file.split('/')[-1].split('.')[0]
            newname = name + ".html"
            convert(file, newname, prefix)


      
            

if __name__ == "__main__":
    main()