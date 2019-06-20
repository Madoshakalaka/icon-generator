# Icon Generator

Note: It's a basically a general purpose icon generator but
It's originally a tool I wrote for google chrome extension in a specific project.
So the default naming scheme of the generated icons may be weird. 

With that said. It is easy to change. Just change some literals at the end of iconGen.py file.

## Functionality
Generate a series of icons in different resolutions with a image provided.

![usecase.png](https://github.com/Madoshakalaka/icon-generator/blob/master/icon_generator/readme_assets/usecase.png)

The user is able to either interactively select a region from the image with GUI, OR just use some square picture without GUI.

The GUI features polite and completely interactive prompts and is straightforward to use.

![easy2use.png](icon_generator/readme_assets/easy2use.png)

## How to Use

support python 3.5 +

`pip install iconGen`

It should have command line executable entry point by default

- `iconGen thonk.png` for an interactive session with GUI

- `iconGen --full square.png` for icon generation without GUI

- `iconGen -h` for more help such as customizable output directory