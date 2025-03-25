### what is this
kisu is a small cross-platform python app that plays a sound when you press/release a key

![kisu](https://github.com/user-attachments/assets/590d87f5-0d61-4021-8ee0-9a0cbc78f9b3)

### why?
_"I HAVE TO TURN MY GAME DOWN TO LIKE 10 BECUASE I CANT FUCKING HEAR MY TAPPING I BECOME SHIT WHEN I CANT HEAR MY TAPPING" - Aspect X_

---
### how to use
1. run **kisu**
2. open kisu sounds directory (theres a button)
- add audio files to **button1/press** for button 1 **press** sounds
- add audio files to **button1/release** for button 1 **release** sounds
- add audio files to **button2/press** for button 2 **press** sounds
- add audio files to **button2/release** for button 2 **release** sounds
- _empty folders will default to a silent audio file_
3. press 'start' button :3

# manual install
> [!note]
> please use python 3.8 to 3.12 as DearPyGui 1.10.1 is not compatible with 3.13 and onwards
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

> [!note]
> i own all rights to the icon and fonts!
