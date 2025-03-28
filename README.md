### what is this
kisu is a small cross-platform python app that plays a sound when you press/release a key

![kisu v0 2](https://github.com/user-attachments/assets/8af72c2a-c438-48f7-9ed9-802808b7975d)

### why?
*I HAVE TO TURN MY GAME DOWN TO LIKE 10 BECUASE I CANT FUCKING HEAR MY TAPPING I BECOME SHIT WHEN I CANT HEAR MY TAPPING" - Aspect X*

---
### how to use
0. [download](https://github.com/cpuQ/kisu/releases/latest) and extract **kisu**
1. run it
2. open kisu sounds directory (theres also a button)
- add audio files to **button1/press** for button 1 **press** sounds
- add audio files to **button1/release** for button 1 **release** sounds
- add audio files to **button2/press** for button 2 **press** sounds
- add audio files to **button2/release** for button 2 **release** sounds
- *you can put as many audio files as you want... or none!*
3. select audio output
4. press start button :3

### todo
- [ ] have a separate settings gui for more configuration options
- [ ] proper audio device dropdown selection
- [ ] bpm prediction based on taps
- [ ] play release key if pressed for longer than X ms or X beats
- [ ] play sounds every 4 taps (useful in streams maybe)
- [ ] normalize audio volume

*suggest any other feature requests in issues*

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
