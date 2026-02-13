# Google Earth 地图动画生成器(线路版)

本程序写给：自驾旅行、地理爱好者、历史地图爱好者。生成器的代码是 Fork 来的，原作者已经弃坑。本代码是在其基础上精简而来，只保留了【线路浏览】部分，需要其他功能，请移步 **[kml_generater](https://github.com/likoosong/kml_generater)

**[我的B站](https://space.bilibili.com/386433605)** 

~~**原作者已停更**~~，这是 [大佬的B站](https://space.bilibili.com/153276950)

![](img\model.png)

## 运行环境

建议在virtualenv环境下食用......

```
安装python环境后，请运行
pip install -r requestments.txt
python main.py
```

## 打包

```
pyinstaller --windowed --onefile --key '123456789' --icon=image/logo.ico --clean --noconfirm main.py
```



