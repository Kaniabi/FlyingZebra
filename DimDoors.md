Instructions
============

1. Execute "ant"

1.1 Problem: Python conflicts

Forge has his own Python, but it gets confused with our environment variables. We
remove these variables in order to make forge's python work properly.

Created setup.bat 

> set PYTHONHOME=
> set PYTHONPATH=
> call ant

1.2 Java JDK

We must install java JDK in the default locations or else force can't find it!

1.3 Ant's build.xml "build" step failed!

Ant step "build" failed with the error:

> Can not find client sources, try decompiling

It seems that ant tries to use mcp scripts instead of relying on forge scripts
I'll call "build/forge/install.cmd" manually 


2 Execute build/forge/install.cmd

2.1 Script install.cmd conflicts with environment python

Changed install.cmd to set empty PYTHONHOME and PYTHONPATH environment variables before
callying python_fml.exe
   
2.2 Missing scala-library.jar

Yes. This is missing AND we must obtain the correct version in order to work.
These files are available online, and mfl have the URL, but the changed their names.

Added file manually!


3. Execute eclipse

> eclipse -data build/forge/mcp/eclipse


4. Execute "Client" inside Eclipse

4.1 Problem downloading some .jar files:

2013-10-29 20:32:10 [SEVERE] [ForgeModLoader] There were errors during initial FML setup. Some files failed to download or were otherwise corrupted. You will need to manually obtain the following files from these download links and ensure your lib directory is clean. 
2013-10-29 20:32:10 [SEVERE] [ForgeModLoader] *** Download http://files.minecraftforge.net/fmllibs/argo-small-3.2.jar
2013-10-29 20:32:10 [SEVERE] [ForgeModLoader] *** Download http://files.minecraftforge.net/fmllibs/guava-14.0-rc3.jar
2013-10-29 20:32:10 [SEVERE] [ForgeModLoader] *** Download http://files.minecraftforge.net/fmllibs/asm-all-4.1.jar
2013-10-29 20:32:10 [SEVERE] [ForgeModLoader] *** Download http://files.minecraftforge.net/fmllibs/bcprov-jdk15on-148.jar
2013-10-29 20:32:10 [SEVERE] [ForgeModLoader] *** Download http://files.minecraftforge.net/fmllibs/deobfuscation_data_1.5.2.zip
2013-10-29 20:32:10 [SEVERE] [ForgeModLoader] *** Download http://files.minecraftforge.net/fmllibs/scala-library.jar

Two of these files have different names on the server:

* http://files.minecraftforge.net/fmllibs/bcprov-jdk15on-148.jar.stash
* http://files.minecraftforge.net/fmllibs/scala-library.jar.stash

Remove the extension ".stash" and place them on build/forge/mcp/jars/lib


*** This will successfully execute Minecraft WITHOUT DimDoors!

5. Changing MCP to use DimDoors

> copy /md /s StevenDimDoors\ build\forge\mcp\src\minecraft\StevenDimDoors
> copy /md /s schematics build\forge\mcp\src\minecraft\schematics
> copy /md /s resources\mods build\forge\mcp\eclipse\Minecraft\bin\mods

*** This will successfully execute Minecraft WITH DimDoors!



