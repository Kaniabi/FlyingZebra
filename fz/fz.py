from ben10.clikit.app import App
from ben10.filesystem import CopyFile, Cwd, IsDir, DeleteDirectory, CopyFiles, \
    CopyDirectory
from ben10.foundation.pushpop import PushPop
import os
import subprocess


app = App('fz')


FORGE_DIR = os.path.abspath('forge')
MFL_DIR = os.path.abspath('forge/fml')
MCP_DIR = os.path.abspath('mcp')
FORGE_URL = 'https://github.com/MinecraftForge/MinecraftForge.git'


def SubVars(x):
    for i in ('FORGE_DIR','MFL_DIR','MCP_DIR','FORGE_URL'):
        x = x.replace('$' + i, globals()[i])
    return x


def Execute(console_, cmd, cwd='.', env={}):
    with Cwd(cwd):
        new_env = os.environ.copy()
        new_env.update(env)
        subprocess.check_call(cmd, env=new_env)


def Patch(console_, filename):
    filename = filename.replace('$FORGE_DIR', FORGE_DIR)
    dirname, filename = os.path.split(filename)
    patches_dir = os.path.abspath('patches')
    patch_filename = os.path.join(patches_dir, filename) + ".patch"
    Execute(console_, 'patch -i %s %s' % (patch_filename, filename), cwd=dirname)


def MyCopyFiles(a, b):
    a = SubVars(a)
    b = SubVars(b)
    CopyFiles(a, b)


def MyCopyFile(a, b):
    a = SubVars(a)
    b = SubVars(b)
    CopyFile(a, b)


def MyCopyDirectory(a, b):
    a = SubVars(a)
    b = SubVars(b)
    CopyDirectory(a, b, True)


@app
def setup(console_):
    '''
    Setup Minecraft Mod Development Environment.
    '''
    console_.Print('<white>Cloning forge/FML</>')
    if IsDir(FORGE_DIR):
        Execute(console_, 'git fetch', cwd=FORGE_DIR)
    else:
        Execute(console_, 'git clone %s %s' % (FORGE_URL, FORGE_DIR))

    # Recommended for 1.6.4
    Execute(console_, 'git checkout 7d5d191', cwd=FORGE_DIR)
    Execute(console_, 'git submodule update --init', cwd=FORGE_DIR)

    # Clean any changes
    #console_.Print('<white>Cleanup changes</>')
    #Execute(console_, 'git checkout -- . ', cwd=FORGE_DIR)
    #Execute(console_, 'git checkout -- . ', cwd=FORGE_DIR + '/fml')

    # Patches
    console_.Print('<white>Install files</>')
    MyCopyFiles('$FORGE_DIR/install/*.py', '$FORGE_DIR')
    MyCopyFiles('$FORGE_DIR/fml/install/*.py', '$FORGE_DIR/fml')
        #MyCopyDirectory('$FORGE_DIR/fml/install/eclipse', '$FORGE_DIR/fml/eclipse')
        #Patch(console_, '$FORGE_DIR/fml/build.xml')

    #console_.Print('<white>Patching Forge/FML to find java/python in our environment</>')
    #Patch(console_, '$FORGE_DIR/fml/fml.py')

    console_.Print('<white>Forge install</>')
    Execute(console_, 'python install.py --mcp-dir=x:\\FlyingZebra\\mcp', cwd=FORGE_DIR)

    # REF: ant writeversion : Generate fmlconfig.properties
    # REF:

    # TODO: Fix python path on fml/build.xml
    # TODO: Execute ant on fml (to generate deobfuscated lzma files)
    # TODO: When executing, missing the MC version in deobfuscated filename



@app
def gen_deobf(console_):
    '''
    Generate deobfuscation data *.lzma)
    '''
    Execute(
        console_,
        'ant.bat -f ..\\forge\\fml\\build.xml build-deobf-data -Dbasedir=%s' % MFL_DIR,
        cwd=MCP_DIR,
        env={
             'PYTHONPATH' : MCP_DIR,
             'PYTHONHOME' : '',
             'WORKSPACE' : os.getcwd(),
        }
    )
    MyCopyFile(
        '$MFL_DIR/deobfuscation_data-1.6.4.lzma',
        '$MCP_DIR/src/minecraft/deobfuscation_data-1.6.4.lzma',
    )
    MyCopyFile(
        '$MFL_DIR/fmlversion.properties',
        '$MCP_DIR/src/minecraft/fmlversion.properties',
    )



if __name__ == '__main__':
    app.Main()


