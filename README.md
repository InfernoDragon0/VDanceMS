# V Dance (Maplestory)

Automatically complete the V Dance PvP minigame in Maplestory! A GPU with CUDA compatiblity is necessary for high performance detection. If you are running it via a CPU, it will be much slower.

### Installation
- Tested on Python 3.11
- Install the requirements.txt
- (Optional, Recommended) If running on a GPU, go to https://pytorch.org/ and select your configuration to install.
- If you already had the CPU version of pyTorch and want to convert to GPU, you should `pip uninstall torch, torchaudio and torchvision` first to avoid conflicts

### Configuration
- Configure your `h` and `w` variables to your window size.
- Set your `npc` button accordingly
- Increase or Decrease `confidence` if you encounter false positives or negatives accordingly
- Increase `sleepAfterSuccess` if it presses NPC button too early after a success

### Model
- A simple model `vdanceprops.pt` based on the `yolov8m.pt` model is trained to detect the success box and the V droplet. When using this mode, it will check if the V droplet is between the success zone and presses a button. The success zone is anywhere in the yellow or pink region.
- An alternate model which is riskier is provided `vdancepink.pt`, if you are using this, uncomment lines 98 to 100 for pressing the NPC button