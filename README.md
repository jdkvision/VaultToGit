# VaultToGit


This script is used to migrate repositories in SourceGear Vault to a Git repository.

### git CLI Installation and Configuration

Please refer to the documentation found [here](https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html).

### Using screen For Long-Running Migrations Via SSH

If you are running a migration via SSH through the VPN, for example on deeplearn, you will want to run it in a [screen session](https://linuxize.com/post/how-to-use-linux-screen/).

### Creating A Github Repository

Before running the migration script, create a new empty repository in github to which you will push following the migration.

### Running The Script

The script will prompt for all required information, so to begin, simply run it via:
`python VaultToGit.py`

You will be presented with the following prompts for input:

- Enter Your Vault Username:

- Enter Vault Host: (Press Enter to use default value of "syr-srv-vault1"):
	- Generally, it should always be okay to press enter to use the default vaule here.

- Enter Vault Repo (Press Enter to use default value of \"JADAK LLC\"):
	- Generally, it should always be okay to press enter to use the default vaule here.

- Enter Vault Folder:
	- For example, $/Engineering/Projects - OEM/BectonDickinson/Twister (JDK-1807 1808 1809)/

- Enter git Repo Address:
	- For example, git@github.com:jdkvision/BD_Twister_JDK-1807_JDK-1808_JDK-1809.git

- WINDOWS ONLY: Enter SourceGear Location (Press Enter to use default value of 'C:\Program Files (x86)\SourceGear\Vault Client'):<br>
  LINUX ONLY: Enter SourceGear Location (Press Enter to use default value of '/media/WD4TBSSD/vaultJavaCLC/'):
	- Generally, it should always be okay to press enter to use the default vaule here.

- Enter location in which to place the local copy of the migrated repo:
	- If the location already exists, you will be asked whether to overwrite it. If it does not already exist, it will be created.

### Pushing To Github

Once the local migration is complete, change to the directory in which the local copy of the migrated repo is (the last argument you provided to the script).

To push to github, run the script:<br>
`git_batch_pushes.sh`

This script will batch push in groups of 100 commits at a time, to avoid the 2GB maximum size limit described [here](https://www.devopsschool.com/blog/git-error-remote-fatal-pack-exceeds-maximum-allowed-size-2-00-gib/).

### Pinning In Vault

Once the migration is complete and pushed to github, pin the folder in Vault that was migrated and add an explanatory label including the URL of its github location.
