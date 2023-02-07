#@title Select your model below, then click the play button to start the UI.
#@markdown Afterwards, just sit tight and wait - the link to the UI should show up after it's done starting up.
import os

Model = "Pygmalion 350M" #@param ["Pygmalion 350M", "Pygmalion 1.3B", "Pygmalion 2.7B", "Pygmalion 6B", "Pygmalion 6B Experimental"] {allow-input: true}

pretty_model_name_to_hf_name = {
    "Pygmalion 350M": "PygmalionAI/pygmalion-350m",
    "Pygmalion 1.3B": "PygmalionAI/pygmalion-1.3b",
    "Pygmalion 2.7B": "PygmalionAI/pygmalion-2.7b",
    "Pygmalion 6B": "PygmalionAI/pygmalion-6b",
    "Pygmalion 6B Experimental": "PygmalionAI/pygmalion-6b"
}

model_name = pretty_model_name_to_hf_name[Model]
branch_name = "main" if Model != "Pygmalion 6B Experimental" else "dev"

# # Copy-pasted from the Kobold notebook. Seems to be necessary for Henk's script
# # to work properly.

# if not os.path.exists("./content/drive"):
#   os.makedirs("./content/drive")
# if not os.path.exists("./content/drive/MyDrive/"):
#   os.makedirs("./content/drive/MyDrive/")

# Use Henk's easy install code, but pass --init since we'll manually start the
# server in the background later.
# INSTALL MANUALLY IN CONTENT/ DIR:: git clone https://github.com/KoboldAI/KoboldAI-Client.git
# THEN RUN pip3 install -r requirements.txt from that dir
# os.system('curl https://koboldai.org/ckds -o - | zsh /dev/stdin --init only')

# Install requirements for the main app
os.system('pip3 install -r requirements.txt')

# Start up Kobold in the background.
# TODO: Figure out a way to keep logs in the foreground so the user knows what's
# going on.
print("\n\n\n")
print("* The model is about to be downloaded and loaded into the GPU.")
print("* This takes several minutes, sit tight.")
print("* A link will show up when this step is completed, keep checking back every couple minutes or so.")
print("\n\n\n")
# os.system(f"cd content/KoboldAI-Client && python3 aiserver.py --noaimenu --host --port 7861 --model {model_name} --revision {branch_name} --nobreakmodel --lowmem --quiet & python3 app.py --koboldai-url http://localhost:7861 --share")
# Below doesn't work cos no CUDA on Macos, circumvent with CPU in model.py

os.system(f"python3 app.py -m {model_name} --share")

# And start up the UI. It'll wait for Kobold to finish booting up before
# printing out its URL.
# os.system('python3 app.py --koboldai-url http://192.0.0.1:7861 --share')