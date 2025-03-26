### what is this
kisu is a small cross-platform python app that plays a sound when you press/release a key

![kisu v0 1](https://github.com/user-attachments/assets/b983e972-9549-4a54-856f-143dc5a68fec)

### why?
_"I HAVE TO TURN MY GAME DOWN TO LIKE 10 BECUASE I CANT FUCKING HEAR MY TAPPING I BECOME SHIT WHEN I CANT HEAR MY TAPPING" - Aspect X_

---
### how to use
1. run **kisu** ([download](https://github.com/cpuQ/kisu/releases/latest))
2. open kisu sounds directory (theres a button)
- add audio files to **button1/press** for button 1 **press** sounds
- add audio files to **button1/release** for button 1 **release** sounds
- add audio files to **button2/press** for button 2 **press** sounds
- add audio files to **button2/release** for button 2 **release** sounds
- _you can put as many audio files as you want... or none!_
3. press 'start' button :3

# manual install
> [!note]
> please use python 3.8 to 3.12 as DearPyGui 1.10.1 is not compatible with 3.13 and onwards

> [!warning]
> [there is a MacOS Sequoia bug](https://discussions.apple.com/thread/255761734?sortBy=rank)
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
> [!warning]
> dpg has issues with nuitka lol https://github.com/hoffstadt/DearPyGui/issues/1867 https://github.com/Nuitka/Nuitka/issues/1534#issuecomment-1354679940
```bash
nuitka --onefile --windows-console-mode=disable --windows-icon-from-ico=res/kisu_large.ico main.py
```

> [!note]
> i own all rights to the icon and fonts!
