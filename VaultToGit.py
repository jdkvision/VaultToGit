import argparse
import os
from lazyme import color_print
import XmlParser
import gitAdressParser
import strip_xml_entities
import getpass
import platform
import shutil
import subprocess
import datetime

def safe_os_system(cmd):
    subprocess.run(cmd, shell=True)

## change these default variables as needed or use command line arguments  ##############################################################################################################################

git_repo_address = 'git@st-gitlab:test/example.git' # The address to the git repo that you wish to move the files in SourceGear Vault to
gitDestination = "" # The name of the git repo. should be the last part of the git address minus the .git

vaultRepo = "TableHeat" # change just the name of the vault repo you wish to migrate to git
vaultFolder = "EX3Main" # change just the name of the vault folder you wish to migrate to git
vaultUser = "vpuser"
vaultPasswd = "archive"
vaultHost = "st-eng"

SourceGearLocation = ""  # The location of the SourceGear Client on your machine
bIsLinux = platform.system() == "Linux"
if bIsLinux:
    cd_cmd = "cd "
else:
    cd_cmd = "cd /D "
local_repo_folder = ""

auto_pusher = 0

gitIgnoreFile = ""
###################################################################################################################################################################

parser = argparse.ArgumentParser()

parser.add_argument("--user", "-u", help="Sourcegear Vault user\n")
parser.add_argument("--password", "-p", help="SourceGear Vault password\n")
parser.add_argument("--host", help="The host that your SourceGear Vault is located on (eq: localhost)")
parser.add_argument("--vaultrepo", "-vr", help="SourceGear Vault repo name (eq: RepoName)")
parser.add_argument("--vaultfolder", "-vf", help="SourceGear Vault folder name (eq: FolderName)")
parser.add_argument("--gitaddress", "-ga", help="The git repo address that you wish to migrate your SourceGear Vault repo to (eq: git@github.com:rapaportg/VaultToGit.git")
#parser.add_argument("--gitdestination", "-gd", help="The name of the git repo. should be the last part of the git address minus the .git")
parser.add_argument("--sourcegear_location","-sgl", help="The location of the SourceGear Client on your machine")
parser.add_argument("--auto_push", "-ap", help="set to 0 or 1 if you would like the git repo to automatically push")
parser.add_argument("--gitignore", "-gi", help= "input the path to your .gitignore file")
parser.add_argument("--local_repo", "-lr", help= "input a path in which to place the local copy of the repo")

args = parser.parse_args()

if args.user:
    vaultUser = args.user
else:
    vaultUser = input( "Enter Your Vault Username: " )

if args.password:
    vaultPasswd = args.password
else:
    vaultPasswd = getpass.getpass( "Enter Your Vault Password: " )    

if args.host:
    vaultHost = args.host
else:
    vaultHost = input( "Enter Vault Host: (Press Enter to use default value of \"syr-srv-vault1\"):" )
    if( "" == vaultHost ):
        vaultHost = "syr-srv-vault1"

if args.vaultrepo:
    vaultRepo = args.vaultrepo
else:
    vaultRepo = input( "Enter Vault Repo (Press Enter to use default value of \"JADAK LLC\"): " )
    if( "" == vaultRepo ):
        vaultRepo = "\"JADAK LLC\""

if args.vaultfolder:
    vaultFolder = args.vaultfolder
else:
    vaultFolder = input( "Enter Vault Folder: " )

if args.gitaddress:
    git_repo_address = args.gitaddress
else:
    git_repo_address = input( "Enter git Repo Address: " )

#if args.gitdestination:
    #gitDestination = args.gitdestination

if args.sourcegear_location:
    SourceGearLocation = args.sourcegear_location
else:
    if bIsLinux:
        SourceGearLocation = input( "Enter SourceGear Location (Press Enter to use default value of '/media/WD4TBSSD/vaultJavaCLC/'): " )
    else:
        SourceGearLocation = input( "Enter SourceGear Location (Press Enter to use default value of 'C:\Program Files (x86)\SourceGear\Vault Client'): " )
    if( "" == SourceGearLocation ):
        if bIsLinux:
            SourceGearLocation = "/media/WD4TBSSD/vaultJavaCLC/"
        else:
            SourceGearLocation = "C:\Program Files (x86)\SourceGear\Vault Client"

gitDestination = gitAdressParser.gitParser(git_repo_address)
print('gitDestination is: ', gitDestination, '\n')

if args.local_repo:
    local_repo_folder = args.local_repo
else:
    while local_repo_folder == "":
        local_repo_folder = input( "Enter location in which to place the local copy of the migrated repo: " )
        if "" != local_repo_folder:
            local_repo_folder = os.path.join(local_repo_folder, "")
            if os.path.exists(local_repo_folder + gitDestination):
                if "Y" == input("The directory " + local_repo_folder + gitDestination + " already exists. Overwrite? (y/n): ").upper():
                    shutil.rmtree(local_repo_folder + gitDestination)
                    os.mkdir(local_repo_folder + gitDestination)
                else:
                    local_repo_folder = ""
            else:
                os.mkdir(local_repo_folder + gitDestination)

if args.auto_push:
    auto_pusher = args.auto_push    

if args.gitignore:
        gitIgnoreFile = args.gitignore

if( not vaultRepo.startswith( "\"" ) ):
    vaultRepo = "\"" + vaultRepo
if( not vaultRepo.endswith( "\"" ) ):
    vaultRepo = vaultRepo + "\""
if( vaultFolder.startswith( "$" ) ):
    vaultFolder = vaultFolder[1:]
if( vaultFolder.startswith( "/" ) ):
    vaultFolder = vaultFolder[1:]
if( not vaultFolder.startswith( "\"" ) ):
    vaultFolder = "\"" + vaultFolder
if( not vaultFolder.endswith( "\"" ) ):
    vaultFolder = vaultFolder + "\""
if( not vaultPasswd.startswith( "\"" ) ):
    vaultPasswd = "\"" + vaultPasswd
if( not vaultPasswd.endswith( "\"" ) ):
    vaultPasswd = vaultPasswd + "\""

# initalizing local git repo
print("CALLING: " + cd_cmd + local_repo_folder + ' && git clone ' + git_repo_address)
safe_os_system(cd_cmd + local_repo_folder + ' && git clone ' + git_repo_address)
safe_os_system('git config user.name "' + vaultUser + '"')
safe_os_system('git config push.default current')

# creating .gitignore
#gitpathcommand = 'cd /D C:\Temp\\' + gitDestination

#safe_os_system(gitpathcommand + " && del .gitignore")
if not gitIgnoreFile == "":
    if bIsLinux:
        gitpath = "cp " + gitIgnoreFile + " " + os.path.join(local_repo_folder, gitDestination, "")
    else:
        gitpath = "copy " + gitIgnoreFile + " " + os.path.join(local_repo_folder, gitDestination, "")
    color_print(gitpath, color='red')
    safe_os_system(gitpath)

# Grabing the Revision History to use as a guide for cloning each commit
credentials = " -host " + vaultHost + " -user " + vaultUser + " -password " + vaultPasswd
getRevHistory = ("./" if bIsLinux else "") + "vault VERSIONHISTORY  -rowlimit 0 " + credentials
beginVersion = " -beginversion 0 "
RevHistoryLocation = '"' + os.path.join(local_repo_folder, "") + 'temp_raw.xml"'
vaultFolder_full = " $/" + vaultFolder
getRevHistoryCommand = getRevHistory + " -repository " + vaultRepo + beginVersion + vaultFolder_full + " > " + RevHistoryLocation

color_print(getRevHistoryCommand.replace(vaultPasswd, "XXXXXXXX"), color='blue')

print("Calling: " + cd_cmd + SourceGearLocation + " && " + getRevHistoryCommand.replace(vaultPasswd, "XXXXXXXX"))
safe_os_system(cd_cmd + SourceGearLocation + " && " + getRevHistoryCommand)
#safe_os_system("cd /D"+ vault2git_script_location)

strip_xml_entities.strip_chars(os.path.join(local_repo_folder, "") + "temp_raw.xml", os.path.join(local_repo_folder, "") + "temp.xml")

input("Press Enter to continue...")

migration_start = datetime.datetime.now()
XmlParser.init(os.path.join(local_repo_folder, "") + "temp.xml")
comments = XmlParser.CommentA()
version = XmlParser.VersionA()
txid = XmlParser.TxidA()
objverid = XmlParser.ObjveridA()
date = XmlParser.DateA()
user = XmlParser.UserA()

gitDestination_full = " " + os.path.join(local_repo_folder, "") + gitDestination
print('gitDestination_full is: ', gitDestination_full, '\n')

# if the script fails part way through change startVersion to match the last know vault version to be committed to git.
# vault version are recorded at the beginning of the git commit messages 
startVersion = 0

loopLength = len(version)
print('\n\nThere are ', loopLength, ' commits to migrate\n\n')

for x in range(startVersion, loopLength, 1):
    commit_version = str(version[x])
    commit_user = str(user[x])
    commit_message = str(comments[x])
    commit_txid = str(txid[x]) 
    commit_objverid = str(objverid[x])
    commit_date = str(date[x])

    git_commit_msg = '"'+ commit_message + "                                                                         " + 'Original Vault commit: version ' + commit_version + " on " + commit_date + "(txid="+commit_txid+')"'

    if(commit_message == "None"):
        git_commit_msg = '"Original Vault commit version ' + commit_version + " on " + commit_date + " (txid="+commit_txid+')"'

    getRepoCommand = ("./" if bIsLinux else "") + "vault GETVERSION" + credentials +" -repository " + vaultRepo +" "+ commit_version + vaultFolder_full +" " + gitDestination_full
    color_print( getRepoCommand.replace(vaultPasswd, "XXXXXXXX"), color="pink")
    color_print( git_commit_msg,color="yellow")
    
    safe_os_system(cd_cmd + SourceGearLocation + " && " + getRepoCommand)

    safe_os_system(cd_cmd + gitDestination_full + " &&  git add . ")
    safe_os_system("git branch --unset-upstream ")
    git_user_email = commit_user+'@autobag.com'
    git_commit = cd_cmd + gitDestination_full + " && "+ " git commit" + ' --author '+'"'+ commit_user + '<'+ git_user_email +'>"' +" --date=" + '"'+ commit_date +'" ' +" -m " + git_commit_msg
    
    print('\n\n', git_commit, '\n\n')

    safe_os_system("git gc")
    safe_os_system(git_commit)

    if( x + 1 < loopLength ):
        clearWorkingDir = cd_cmd + gitDestination_full + ' && git rm -r .'
        safe_os_system(clearWorkingDir)

'''
# jcairns 06162022: I'm leaving this in, just in case it still proves useful in
# ths future, but I believe that the fix in the loop above to do a 'git rm -r .'
# on all but the most recent commit obviates the need to check for and remove
# any files or folders we have in our git repo that are not in the Vault tips.
#
# Remove anything not in the tips
import tempfile
import shutil

bRemoved = False
tipsdir = os.path.join( tempfile.gettempdir(), gitDestination )
print( "Getting tips of Vault folder to " + tipsdir )
getRepoCommand = "vault GETVERSION" + credentials +" -repository " + vaultRepo +" "+ commit_version + vaultFolder_full +" " + tipsdir
safe_os_system("cd /D " + SourceGearLocation + " && " + getRepoCommand)
safe_os_system("cd /D " + gitDestination_full)
for filename in os.listdir(gitDestination_full.strip()):
    if( filename.startswith( ".git" ) ):
        continue
    f = os.path.join(tipsdir, filename)
    if( not os.path.exists( f ) ):
        bRemoved = True
        print( "FILE DOES NOT EXIST IN VAULT TIPS: " + filename )
        print( "REMOVING FROM GIT" )
        if( os.path.isdir( filename ) ):
            safe_os_system("git rm -r " + filename)
        else:
            safe_os_system("git rm " + filename)
            
try:
    print( "Deleting temporary Vault tips folder " + tipsdir )
    shutil.rmtree(tipsdir)
except OSError as e:
    print("Error: %s : %s" % (tipsdir, e.strerror))
            
if( bRemoved ):
    git_commit = "git commit" + ' --author '+'"'+ commit_user + '<'+ git_user_email +'>"' +" --date=" + '"'+ commit_date +'" ' +" -m Removed files and folders not present in the tips of the Vault folder"    
    print('\n\n', git_commit, '\n\n')
    safe_os_system("git gc")
    safe_os_system(git_commit)
'''

if (auto_pusher == 1):
    safe_os_system("git push -u origin master")
else:
    color_print("To push the git repository please go to the directory it is located in review the repo and push manually", color="green")

print("Migration took: " + str(datetime.datetime.now() - migration_start))
