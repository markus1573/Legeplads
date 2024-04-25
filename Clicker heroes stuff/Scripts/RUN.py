from Functions import *
from Autoclicker import*
import sys
if sys.platform == "win32":
    os.chdir("C:/Users/marku/Documents/GitHub/Legeplads/Clicker heroes stuff")
elif sys.platform == "darwin":
    os.chdir("/Users/markus/Documents/Legeplads/Clicker heroes stuff")
# os.chdir("Clicker heroes stuff")
MAX_HERO = "Moeru"
GUILDED_HERO = "Tsuchi"
DEEP_RUN = False
START_IDLE = True
if __name__ == '__main__':
    Initialize_program()
    

    # FocusWindowAndGetWindowPOS()
    
# YOLOv5  2024-4-25 Python-3.11.8 torch-2.2.2 CUDA:0 (NVIDIA GeForce RTX 2060, 6144MiB)

# Traceback (most recent call last):
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\yolov5\hubconf.py", line 50, in _create
#     model = DetectMultiBackend(path, device=device, fuse=autoshape)  # detection model
#             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\yolov5\models\common.py", line 467, in __init__
#     model = attempt_load(weights if isinstance(weights, list) else w, device=device, inplace=True, fuse=fuse)
#             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\yolov5\models\experimental.py", line 98, in attempt_load
#     ckpt = torch.load(attempt_download(w), map_location="cpu")  # load
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\site-packages\torch\serialization.py", line 1026, in load
#     return _load(opened_zipfile,
#            ^^^^^^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\site-packages\torch\serialization.py", line 1438, in _load
#     result = unpickler.load()
#              ^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\pathlib.py", line 873, in __new__
#     raise NotImplementedError("cannot instantiate %r on your system"
# NotImplementedError: cannot instantiate 'PosixPath' on your system

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\yolov5\hubconf.py", line 65, in _create
#     model = attempt_load(path, device=device, fuse=False)  # arbitrary model
#             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\yolov5\models\experimental.py", line 98, in attempt_load
#     ckpt = torch.load(attempt_download(w), map_location="cpu")  # load
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\site-packages\torch\serialization.py", line 1026, in load
#     return _load(opened_zipfile,
#            ^^^^^^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\site-packages\torch\serialization.py", line 1438, in _load
#     result = unpickler.load()
#              ^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\pathlib.py", line 873, in __new__
#     raise NotImplementedError("cannot instantiate %r on your system"
# NotImplementedError: cannot instantiate 'PosixPath' on your system

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\Scripts\RUN.py", line 14, in <module>
#     Initialize_program()
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\Scripts\Functions.py", line 1359, in Initialize_program
#     Init_fishing()
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\Scripts\Functions.py", line 926, in Init_fishing
#     model = torch.hub.load("yolov5", 'custom', path='yolov5/runs/train/300_hpc/weights/best.pt', source='local',force_reload=True)
#             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\site-packages\torch\hub.py", line 566, in load
#     model = _load_local(repo_or_dir, model, *args, **kwargs)
#             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\ProgramData\miniconda3\Lib\site-packages\torch\hub.py", line 595, in _load_local
#     model = entry(*args, **kwargs)
#             ^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\yolov5\hubconf.py", line 88, in custom
#     return _create(path, autoshape=autoshape, verbose=_verbose, device=device)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\marku\Documents\GitHub\Legeplads\Clicker heroes stuff\yolov5\hubconf.py", line 83, in _create
#     raise Exception(s) from e
# Exception: cannot instantiate 'PosixPath' on your system. Cache may be out of date, try `force_reload=True` or see https://docs.ultralytics.com/yolov5/tutorials/pytorch_hub_model_loading for help.
