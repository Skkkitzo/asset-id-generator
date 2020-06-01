# Foundation Asset Generator

This program is designed to help you, as a modder, more easily combine your generated_ids.lua files.

"What do you mean by that?", I hear you saying. When you are creating your mod, and testing it locally, the game generates a file to hold all of the asset ids. This file is important to bundle with your mod when you upload it, so that other people can use your mod. Without this file, others are unable to install your mod. 

The problem arises when you generate the file, and then add another item to your mod (say a building). This new building needs another asset ID, but Foundation doesn't re-generate this file if it finds it in the mod directory. Instead, it just loads up the file like normal. 

To re-generate the asset IDs, you must delete the generated_ids.lua file in the directory of your mod (NOT the working directory - I will explain further in the steps below). But when you delete this file, you also slightly corrupt your mod. Using this process, a player with a save-game using your mod cannot update to the newest version of your mod and then reload their save-game; it will cause Foundation to crash. 

This program solves this problem, by looking for new (previously unused) asset IDs in the freshly generated lua file, and then adds them to your mod's previous version's asset ID lua file.

### Important Note
This program assumes that you create mods according to the standard procedure of software development; meaning that you have a dedicated directory for your coding projects that is not inside the 'working directory' (in this case, the mods folder of Foundation). I store all my local mods (for testing and developing purposes) inside C:/Coding/Foundation/mymod and then copy this folder into C:/users/me/Documents/Polymorph Games/Foundation/mods.

## Instructions
1. Copy your mod directory to the Foundation mods directory
2. Delete generated_ids.lua (make a backup just in case)
3. Load Foundation + create a new save with your mod to generate the asset IDs
4. Download [the latest release](https://github.com/Skkkitzo/asset-id-generator/releases)
5. Your OS may give you a warning explaining how the file is unknown and may be a virus, I assure you it's not but my word isn't really worth anything. I advise you scan the file using your software of choice, and check the MD5 hash as well.
6. Run the file and select the original generated_ids.lua file. This should be the one in your working directory, where you create your mod, _**NOT**_ the mods folder of Foundation that you created in step 3.
7. Select the generated_ids.lua file that you want to _combine_ with the main file, this is the file that you created in step 3.
8. Before you click Calculate, you should know that this program will overwrite the main generated_ids.lua file and add the new asset IDs. Just in case I screwed something up while programming this, I _highly_ advise you create a backup of your asset IDs file.
9. Click Calculate
10. Your file has now been updated with all the newest asset IDs

**All bugs and errors should be reported on the [issue tracker](https://github.com/Skkkitzo/asset-id-generator/issues)**

MD5 Checksum: ee21b45be157fb8877dd4fd3ebdcaeb8
