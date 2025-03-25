if you are on windows you download the compiled release from [releases tab](https://github.com/cpuQ/kisu/releases)

---
### how to use
1. run **kisu**
2. open kisu directory
3. add audio files to **sounds/button1/press** for button 1 **press** sounds
4. add audio files to **sounds/button1/release** for button 1 **release** sounds
5. add audio files to **sounds/button2/press** for button 2 **press** sounds
6. add audio files to **sounds/button2/release** for button 2 **release** sounds

# manual install
> [!note]
> please use any python version between 3.8 and 3.12 as DearPyGui 1.10.1 is not compatible with 3.13 and onwards
```bash
git clone https://github.com/cpuQ/kisu
```
```bash
cd kisu
```
```Pip Requirements
python -m pip install -r requirements.txt
```
```bash
python main.py
```

## compiled with nuitka
```bash
nuitka --onefile --windows-console-mode=disable --windows-icon-from-ico=res/kisu_large.ico main.py
```
