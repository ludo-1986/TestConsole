import tools
from rich import print

word = input(f"Enter a name or word --> ").lower().strip()

word_lower_hex = [bytes(i, "utf-8").hex() for i in word.lower()]
word_lower_ascii = [ord(i) for i in word.lower()]
word_upper_hex = [bytes(i, "utf-8").hex() for i in word.upper()]
word_upper_ascii = [ord(i) for i in word.upper()]

rest = len(word) % 3
gear = len(word) // 3
global_gear = gear + 1 if rest else gear

def replace_letter()-> dict:
    
    letter_number = {
        "a" : "a", "b" : "b", "c" : "c", "d" : "d", "e" : "e", "f" : "f",
        "g" : "9", "h" : "4", "i" : "1", "j" : "1", "k" : "4", "l" : "7",
        "m" : "3", "n" : "2", "o" : "0", "p" : "9", "q" : "9", "r" : "4",
        "s" : "5", "t" : "7", "u" : "5", "v" : "5", "w" : "0", "x" : "8",
        "y" : "9", "z" : "0"
    }
    def_word = word.replace(" ", "")
    
    if len(word) < 6:
        multiplier = (6 // len(word)) + 1
        def_word = (word * multiplier)[:6]
        
    word_changed = tools.replace_char(def_word, letter_number)
    def_gear = len(def_word) // 6
    def_rest = len(def_word) % 6
    
    dict_color = {}
    
    for i in range(def_gear):
        pos = i * 6
        
        selected = word_changed[0 + pos:6 + pos]
        
        dict_color.update({
            f"{def_word[0 + pos:6 + pos]} replace letter" : f"{selected}",
            f"{def_word[0 + pos:6 + pos]} invert replace letter" : f"{selected[::-1]}"
        })
    
    if def_rest:
        selected = word_changed[-6:]
        dict_color.update({
            f"{def_word[-6:]} replace letter" : f"{selected}",
            f"{def_word[-6:]} invert replace letter" : f"{selected[::-1]}"
        })
    
    return dict_color

def with_max(order: str="rgb", level: str="light", lower: bool=True)-> str:
    lower_max = word_lower_hex[word_lower_ascii.index(max(word_lower_ascii))]
    upper_max = word_upper_hex[word_upper_ascii.index(max(word_upper_ascii))]
    
    color_dict = {}
    
    used_hex = lower_max if lower else upper_max
    
    if level == "light":
        color_dict.update({
            "rgb" : f"{used_hex}ffff",
            "gbr" : f"ffff{used_hex}",
            "brg" : f"ff{used_hex}ff",
        })
    elif level == "mid0":
        color_dict.update({
            "rgb" : f"{used_hex}00ff",
            "gbr" : f"00ff{used_hex}",
            "brg" : f"00{used_hex}ff",
        })
    elif level == "midf":
        color_dict.update({
            "rgb" : f"{used_hex}ff00",
            "gbr" : f"ff00{used_hex}",
            "brg" : f"ff{used_hex}00",
        })
    else:
        color_dict.update({
            "rgb" : f"{used_hex}0000",
            "gbr" : f"0000{used_hex}",
            "brg" : f"00{used_hex}00",
        })
        
    return color_dict.get(order)

def darkest_color(color: str, light: bool=False)-> str:
    
    """
    color -> mandatory : str = ["12345678" | "123456"]
        only -> return str["rgb"]
        with order : str -> choice from ["gbr" | "brg"] -> return str
    """
    r, g, b = color[:2], color[2:4], color[4:]
    
    sum_r = str(int(r[0], 16) + int(r[1], 16)) 
    sum_g = str(int(g[0], 16) + int(g[1], 16))
    sum_b = str(int(b[0], 16) + int(b[1], 16))
    
    if light:
        sum_r = int(sum_r, 16) * 2
        sum_g = int(sum_g, 16) * 2
        sum_b = int(sum_b, 16) * 2
        return rgb_to_hex(sum_r, sum_g, sum_b)
    
    return f"{sum_r if len(sum_r) == 2 else f"0{sum_r}"}"\
            f"{sum_g if len(sum_g) == 2 else f"0{sum_g}"}"\
            f"{sum_b if len(sum_b) == 2 else f"0{sum_b}"}"

def lightest_color(color: str)-> str:
    
    r, g, b = color[:2], color[2:4], color[4:]
    
    sum_r = int(r, 16) * 2
    sum_g = int(g, 16) * 2
    sum_b = int(b, 16) * 2
    
    return rgb_to_hex(sum_r, sum_g, sum_b)

def rgb_to_hex(r: int, g: int, b: int)-> str:
    return f"{r:02x}{b:02x}{g:02x}"

def hex_to_rgb(color: str)-> tuple[int]:
    
    return int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)

color_base: dict[str, str] = {}

for gg in range(global_gear):
    
    for g in range(gear):
        pos = g * 3
        lower_rgb_gear = f"{word_lower_hex[0+pos]}{word_lower_hex[1+pos]}{word_lower_hex[2+pos]}"
        lower_gbr_gear = f"{word_lower_hex[1+pos]}{word_lower_hex[2+pos]}{word_lower_hex[0+pos]}"
        lower_brg_gear = f"{word_lower_hex[2+pos]}{word_lower_hex[0+pos]}{word_lower_hex[1+pos]}"
        
        upper_rgb_gear = f"{word_upper_hex[0+pos]}{word_upper_hex[1+pos]}{word_upper_hex[2+pos]}"
        upper_gbr_gear = f"{word_upper_hex[1+pos]}{word_upper_hex[2+pos]}{word_upper_hex[0+pos]}"
        upper_brg_gear = f"{word_upper_hex[2+pos]}{word_upper_hex[0+pos]}{word_upper_hex[1+pos]}"
        
        color_base.update({
            f"{word[0+pos:3+pos]} lower brg" : lower_brg_gear,
            f"{word[0+pos:3+pos]} lower gbr" : lower_gbr_gear,
            f"{word[0+pos:3+pos]} lower rgb" : lower_rgb_gear,
            f"{word[0+pos:3+pos]} lower invert brg" : lower_brg_gear[::-1],
            f"{word[0+pos:3+pos]} lower invert gbr" : lower_gbr_gear[::-1],
            f"{word[0+pos:3+pos]} lower invert rgb" : lower_rgb_gear[::-1],
            f"{word[0+pos:3+pos]} lower dark brg" : darkest_color(lower_brg_gear),
            f"{word[0+pos:3+pos]} lower dark gbr" : darkest_color(lower_gbr_gear),
            f"{word[0+pos:3+pos]} lower dark rgb" : darkest_color(lower_rgb_gear),
            f"{word[0+pos:3+pos]} lower invert dark brg" : darkest_color(lower_brg_gear)[::-1],
            f"{word[0+pos:3+pos]} lower invert dark gbr" : darkest_color(lower_gbr_gear)[::-1],
            f"{word[0+pos:3+pos]} lower invert dark rgb" : darkest_color(lower_rgb_gear)[::-1],
            f"{word[0+pos:3+pos]} lower light brg" : lightest_color(lower_brg_gear),
            f"{word[0+pos:3+pos]} lower light gbr" : lightest_color(lower_gbr_gear),
            f"{word[0+pos:3+pos]} lower light rgb" : lightest_color(lower_rgb_gear),
            f"{word[0+pos:3+pos]} lower invert light brg" : lightest_color(lower_brg_gear)[::-1],
            f"{word[0+pos:3+pos]} lower invert light gbr" : lightest_color(lower_gbr_gear)[::-1],
            f"{word[0+pos:3+pos]} lower invert light rgb" : lightest_color(lower_rgb_gear)[::-1],
            f"{word[0+pos:3+pos]} lower light from dark brg" : darkest_color(lower_brg_gear, True),
            f"{word[0+pos:3+pos]} lower light from dark gbr" : darkest_color(lower_gbr_gear, True),
            f"{word[0+pos:3+pos]} lower light from dark rgb" : darkest_color(lower_rgb_gear, True),
            f"{word[0+pos:3+pos]} lower invert light from dark brg" : darkest_color(lower_brg_gear, True)[::-1],
            f"{word[0+pos:3+pos]} lower invert light from dark gbr" : darkest_color(lower_gbr_gear, True)[::-1],
            f"{word[0+pos:3+pos]} lower invert light from dark rgb" : darkest_color(lower_rgb_gear, True)[::-1],
        })
        
        color_base.update({
            f"{word[0+pos:3+pos]} upper brg" : upper_brg_gear,
            f"{word[0+pos:3+pos]} upper gbr" : upper_gbr_gear,
            f"{word[0+pos:3+pos]} upper rgb" : upper_rgb_gear,
            f"{word[0+pos:3+pos]} upper invert brg" : upper_brg_gear[::-1],
            f"{word[0+pos:3+pos]} upper invert gbr" : upper_gbr_gear[::-1],
            f"{word[0+pos:3+pos]} upper invert rgb" : upper_rgb_gear[::-1],
            f"{word[0+pos:3+pos]} upper dark brg" : darkest_color(upper_brg_gear),
            f"{word[0+pos:3+pos]} upper dark gbr" : darkest_color(upper_gbr_gear),
            f"{word[0+pos:3+pos]} upper dark rgb" : darkest_color(upper_rgb_gear),
            f"{word[0+pos:3+pos]} upper invert dark brg" : darkest_color(upper_brg_gear)[::-1],
            f"{word[0+pos:3+pos]} upper invert dark gbr" : darkest_color(upper_gbr_gear)[::-1],
            f"{word[0+pos:3+pos]} upper invert dark rgb" : darkest_color(upper_rgb_gear)[::-1],
            f"{word[0+pos:3+pos]} upper light brg" : lightest_color(upper_brg_gear),
            f"{word[0+pos:3+pos]} upper light gbr" : lightest_color(upper_gbr_gear),
            f"{word[0+pos:3+pos]} upper light rgb" : lightest_color(upper_rgb_gear),
            f"{word[0+pos:3+pos]} upper invert light brg" : lightest_color(upper_brg_gear)[::-1],
            f"{word[0+pos:3+pos]} upper invert light gbr" : lightest_color(upper_gbr_gear)[::-1],
            f"{word[0+pos:3+pos]} upper invert light rgb" : lightest_color(upper_rgb_gear)[::-1],
            f"{word[0+pos:3+pos]} upper light from dark brg" : darkest_color(upper_brg_gear, True),
            f"{word[0+pos:3+pos]} upper light from dark gbr" : darkest_color(upper_gbr_gear, True),
            f"{word[0+pos:3+pos]} upper light from dark rgb" : darkest_color(upper_rgb_gear, True),
            f"{word[0+pos:3+pos]} upper invert light from dark brg" : darkest_color(upper_brg_gear, True)[::-1],
            f"{word[0+pos:3+pos]} upper invert light from dark gbr" : darkest_color(upper_gbr_gear, True)[::-1],
            f"{word[0+pos:3+pos]} upper invert light from dark rgb" : darkest_color(upper_rgb_gear, True)[::-1],
        })
    
    if rest:
        lower_bgr_rest = f"{word_lower_hex[-1]}{word_lower_hex[-3]}{word_lower_hex[-2]}"
        lower_gbr_rest = f"{word_lower_hex[-2]}{word_lower_hex[-1]}{word_lower_hex[-3]}"
        lower_rgb_rest = f"{word_lower_hex[-3]}{word_lower_hex[-2]}{word_lower_hex[-1]}"
        upper_bgr_rest = f"{word_upper_hex[-1]}{word_upper_hex[-3]}{word_upper_hex[-2]}"
        upper_gbr_rest = f"{word_upper_hex[-2]}{word_upper_hex[-1]}{word_upper_hex[-3]}"
        upper_rgb_rest = f"{word_upper_hex[-3]}{word_upper_hex[-2]}{word_upper_hex[-1]}"
        
        color_base.update({
            f"{word[-3:]} lower brg" : lower_bgr_rest,
            f"{word[-3:]} lower gbr" : lower_gbr_rest,
            f"{word[-3:]} lower rgb" : lower_rgb_rest,
            f"{word[-3:]} lower invert brg" : lower_bgr_rest[::-1],
            f"{word[-3:]} lower invert gbr" : lower_gbr_rest[::-1],
            f"{word[-3:]} lower invert rgb" : lower_rgb_rest[::-1],
            f"{word[-3:]} lower dark brg" : darkest_color(lower_bgr_rest),
            f"{word[-3:]} lower dark gbr" : darkest_color(lower_gbr_rest),
            f"{word[-3:]} lower dark rgb" : darkest_color(lower_rgb_rest),
            f"{word[-3:]} lower invert dark brg" : darkest_color(lower_bgr_rest)[::-1],
            f"{word[-3:]} lower invert dark gbr" : darkest_color(lower_gbr_rest)[::-1],
            f"{word[-3:]} lower invert dark rgb" : darkest_color(lower_rgb_rest)[::-1],
            f"{word[-3:]} lower light brg" : lightest_color(lower_bgr_rest),
            f"{word[-3:]} lower light gbr" : lightest_color(lower_gbr_rest),
            f"{word[-3:]} lower light rgb" : lightest_color(lower_rgb_rest),
            f"{word[-3:]} lower invert light brg" : lightest_color(lower_bgr_rest)[::-1],
            f"{word[-3:]} lower invert light gbr" : lightest_color(lower_gbr_rest)[::-1],
            f"{word[-3:]} lower invert light rgb" : lightest_color(lower_rgb_rest)[::-1],
            f"{word[-3:]} lower light from dark brg" : darkest_color(lower_bgr_rest, True),
            f"{word[-3:]} lower light from dark gbr" : darkest_color(lower_gbr_rest, True),
            f"{word[-3:]} lower light from dark rgb" : darkest_color(lower_rgb_rest, True),
            f"{word[-3:]} lower invert light from dark brg" : darkest_color(lower_bgr_rest, True)[::-1],
            f"{word[-3:]} lower invert light from dark gbr" : darkest_color(lower_gbr_rest, True)[::-1],
            f"{word[-3:]} lower invert light from dark rgb" : darkest_color(lower_rgb_rest, True)[::-1],
        })
        
        color_base.update({
            f"{word[-3:]} upper brg" : upper_bgr_rest,
            f"{word[-3:]} upper gbr" : upper_gbr_rest,
            f"{word[-3:]} upper rgb" : upper_rgb_rest,
            f"{word[-3:]} upper invert brg" : upper_bgr_rest[::-1],
            f"{word[-3:]} upper invert gbr" : upper_gbr_rest[::-1],
            f"{word[-3:]} upper invert rgb" : upper_rgb_rest[::-1],
            f"{word[-3:]} upper dark brg" : darkest_color(upper_bgr_rest),
            f"{word[-3:]} upper dark gbr" : darkest_color(upper_gbr_rest),
            f"{word[-3:]} upper dark rgb" : darkest_color(upper_rgb_rest),
            f"{word[-3:]} upper invert dark brg" : darkest_color(upper_bgr_rest)[::-1],
            f"{word[-3:]} upper invert dark gbr" : darkest_color(upper_gbr_rest)[::-1],
            f"{word[-3:]} upper invert dark rgb" : darkest_color(upper_rgb_rest)[::-1],
            f"{word[-3:]} upper light brg" : lightest_color(upper_bgr_rest),
            f"{word[-3:]} upper light gbr" : lightest_color(upper_gbr_rest),
            f"{word[-3:]} upper light rgb" : lightest_color(upper_rgb_rest),
            f"{word[-3:]} upper invert light brg" : lightest_color(upper_bgr_rest)[::-1],
            f"{word[-3:]} upper invert light gbr" : lightest_color(upper_gbr_rest)[::-1],
            f"{word[-3:]} upper invert light rgb" : lightest_color(upper_rgb_rest)[::-1],
            f"{word[-3:]} upper light from dark brg" : darkest_color(upper_bgr_rest, True),
            f"{word[-3:]} upper light from dark gbr" : darkest_color(upper_gbr_rest, True),
            f"{word[-3:]} upper light from dark rgb" : darkest_color(upper_rgb_rest, True),
            f"{word[-3:]} upper invert light from dark brg" : darkest_color(upper_bgr_rest, True)[::-1],
            f"{word[-3:]} upper invert light from dark gbr" : darkest_color(upper_gbr_rest, True)[::-1],
            f"{word[-3:]} upper invert light from dark rgb" : darkest_color(upper_rgb_rest, True)[::-1],
        })


average_lower = sum(word_lower_ascii) // len(word)
average_upper = sum(word_upper_ascii) // len(word)
max_lower = max(word_lower_ascii)
max_upper = max(word_upper_ascii)
min_lower = min(word_lower_ascii)
min_upper = min(word_upper_ascii)

color_base.update({
    "average lower" : rgb_to_hex(average_lower, average_lower, average_lower),
    "average upper" : rgb_to_hex(average_upper, average_upper, average_upper),
    "ave max min lower" : rgb_to_hex(average_lower, max_lower, min_lower),
    "ave max min upper" : rgb_to_hex(average_upper, max_upper, min_upper),
    "max lower" : rgb_to_hex(max_lower, max_lower, max_lower),
    "max upper" : rgb_to_hex(max_upper, max_upper, max_upper),
    "min lower" : rgb_to_hex(min_lower, min_lower, min_lower),
    "min upper" : rgb_to_hex(min_upper, min_upper, min_upper),
    "average invert lower" : rgb_to_hex(average_lower, average_lower, average_lower)[::-1],
    "average invert upper" : rgb_to_hex(average_upper, average_upper, average_upper)[::-1],
    "ave max min invert lower" : rgb_to_hex(average_lower, max_lower, min_lower)[::-1],
    "ave max min invert upper" : rgb_to_hex(average_upper, max_upper, min_upper)[::-1],
    "max invert lower" : rgb_to_hex(max_lower, max_lower, max_lower)[::-1],
    "max invert upper" : rgb_to_hex(max_upper, max_upper, max_upper)[::-1],
    "min invert lower" : rgb_to_hex(min_lower, min_lower, min_lower)[::-1],
    "min invert upper" : rgb_to_hex(min_upper, min_upper, min_upper)[::-1],
    "with max mid0 brg upper" : with_max(order="brg", level="mid0", lower=False),
    "with max mid0 gbr upper" : with_max(order="gbr", level="mid0", lower=False),
    "with max mid0 rgb upper" : with_max(order="rgb", level="mid0", lower=False),
    "with max light brg upper" : with_max(order="brg", lower=False),
    "with max light gbr upper" : with_max(order="gbr", lower=False),
    "with max light rgb upper" : with_max(order="rgb", lower=False),
    "with max midf brg lower" : with_max(order="brg", level="midf"),
    "with max midf gbr lower" : with_max(order="gbr", level="midf"),
    "with max midf rgb lower" : with_max(order="rgb", level="midf"),
    "with max dark brg lower" : with_max(order="brg", level="dark"),
    "with max dark gbr lower" : with_max(order="gbr", level="dark"),
    "with max dark rgb lower" : with_max(order="rgb", level="dark"),
    "with max invert mid0 brg upper" : with_max(order="brg", level="mid0", lower=False)[::-1],
    "with max invert mid0 gbr upper" : with_max(order="gbr", level="mid0", lower=False)[::-1],
    "with max invert mid0 rgb upper" : with_max(order="rgb", level="mid0", lower=False)[::-1],
    "with max invert light brg upper" : with_max(order="brg", lower=False)[::-1],
    "with max invert light gbr upper" : with_max(order="gbr", lower=False)[::-1],
    "with max invert light rgb upper" : with_max(order="rgb", lower=False)[::-1],
    "with max invert midf brg lower" : with_max(order="brg", level="midf")[::-1],
    "with max invert midf gbr lower" : with_max(order="gbr", level="midf")[::-1],
    "with max invert midf rgb lower" : with_max(order="rgb", level="midf")[::-1],
    "with max invert dark brg lower" : with_max(order="brg", level="dark")[::-1],
    "with max invert dark gbr lower" : with_max(order="gbr", level="dark")[::-1],
    "with max invert dark rgb lower" : with_max(order="rgb", level="dark")[::-1],
})

color_base.update(replace_letter())

data_list = [
    "GIMP Palette",
    "Columns: 3",
    f"# {len(color_base)} Colors",
    "# R G B Color name"
    ]

data_dict = {}

key_len = [len(k[0]) for k in color_base.items()]
line_dict = [len(k) + len(v) for k, v in color_base.items()]
space = max(line_dict) - len(word) + 10
before = round(space / 2)
after = space - before

print(f"[bold underline {'#00FF86'}]{" " * before}{word.capitalize()}{" " * after}[/]")
    
for k, v in sorted(color_base.items(), key=lambda item: item[0]):
    
    hex_color = f"#{v}" if not v.startswith("#") else v
    
    r, g, b = hex_to_rgb(v)
    data_list.append(f"{r}\t{g}\t{b}\t{k.capitalize()}")
    
    data_dict.update({k.replace(" ", "_") : f"#{v.upper()}"})
    
    lumen = r * 0.2126 + g * 0.7152 + b * 0.0722
    
    text_color = "#f1986f" if lumen < 100 else "#080324"
    space = max(key_len) - len(k) + 4
    first = round(space / 2)
    last = space - first
    
    print(f"[{text_color} on {hex_color}]{" " * first}{k}{" " * last}|  #{v.upper()}  [/]")
    
print(f"[{'#00FF86'}]{len(color_base)} colors[/]")

saving = input(f"save the colors to a file (y/n) --> ").lower().strip()

if saving == "y":

    name_file = input(f"Give the files a name --> ").strip().replace(" ", "_").lower()
    
    data_list.insert(1, f"Name: {name_file.replace("_", " ").capitalize()}")
        
    tools.save_file(data=data_list, file_name=f"{name_file}.gpl", is_json=False)
    tools.save_file(data=data_dict, file_name=f"{name_file}.json")
