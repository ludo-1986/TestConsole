import tools
from rich import print

my_date = tools.ask_number(question="choice a date", date=True)
my_date_list_str = [my_date[i:i+2] for i in range(0, len(my_date), 2)]
my_date_list_int = [int(my_date[i:i+2]) for i in range(0, len(my_date), 2)]
total_date = "0"

for i in my_date:
    total_date = str(int(int(total_date) + int(i)))

light = int(total_date) * 4
white = int(total_date) * 6
total_date_dark = str(round(int(total_date) / 2))
total_date_light = str(light) if light <= 99 else f"{light:02x}"
total_date_lighter = str(int(total_date) * 2)
total_date_white = str(white) if white <= 99 else f"{white:02x}"

total_date_list = sum(my_date_list_int)
total_date_list_b16 = int(str(total_date_list), 16)
        
def date_to_color(date: str, order: str=None, full: bool=False)-> str | tuple[str]:
    
    """
    date -> mandatory : str = "12345678"
        only -> return tuple[str]
        with order : str -> choice from ["rgb" | "gbr" | "brg"] -> return str
        with full : bool -> return str
    """
        
    if full:
        r = date[0:2]
        g = date[2:4]
        last = date[4:]
        b = "0"
        
        for i in last:
            b = str(int(int(b) + int(i)))
        return f"{r}{g}{b if len(b) == 2 else f"0{b}"}"
    
    order_dict = {
        "rgb" : f"{date[0:2]}{date[2:4]}{date[-2:]}",
        "gbr" : f"{date[2:4]}{date[-2:]}{date[0:2]}",
        "brg" : f"{date[-2:]}{date[0:2]}{date[2:4]}"
    }
    
    if order:
        return order_dict.get(order)
    
    return date[0:2], date[2:4], date[-2:]

def darkest_color(color: str, order: str="rgb", light: bool=False)-> str:
    
    """
    color -> mandatory : str = ["12345678" | "123456"]
        only -> return str["rgb"]
        with order : str -> choice from ["gbr" | "brg"] -> return str
    """
    
    if len(color) == 6:
        r, g, b = date_to_color(date=color)
        sum_b = str(int(b[0], 16) + int(b[1], 16))
    else:
        r, g, b = date_to_color(date_to_color(date=color, full=True))
        sum_b = b
    
    if light:
        sum_r = str(int(r) * 2) 
        sum_g = str(int(g) * 2)
        sum_b = str(int(b) * 2)
    else:
        sum_r = str(int(r[0], 16) + int(r[1], 16)) 
        sum_g = str(int(g[0], 16) + int(g[1], 16))
    
    order_dict = {
        "rgb" : f"{sum_r if len(sum_r) == 2 else f"0{sum_r}"}"\
            f"{sum_g if len(sum_g) == 2 else f"0{sum_g}"}"\
            f"{sum_b if len(sum_b) == 2 else f"0{sum_b}"}",
        "gbr" : f"{sum_g if len(sum_g) == 2 else f"0{sum_g}"}"\
            f"{sum_b if len(sum_b) == 2 else f"0{sum_b}"}"\
            f"{sum_r if len(sum_r) == 2 else f"0{sum_r}"}",
        "brg" : f"{sum_b if len(sum_b) == 2 else f"0{sum_b}"}"\
            f"{sum_r if len(sum_r) == 2 else f"0{sum_r}"}"\
            f"{sum_g if len(sum_g) == 2 else f"0{sum_g}"}"
    }
    
    return order_dict.get(order)

def lightest_color(color: str, order: str="rgb")-> str:
    
    r, g, b = date_to_color(color)
    
    sum_r = int(r) * 2
    sum_g = int(g) * 2
    sum_b = int(b) * 2
    
    order_dict = {
        "rgb" : f"{sum_r if sum_r <= 99 else f"{sum_r:02x}"}"\
            f"{sum_g if sum_g <= 99 else f"{sum_g:02x}"}"\
            f"{sum_b if sum_b <= 99 else f"{sum_b:02x}"}",
        "gbr" : f"{sum_g  if sum_g <= 99 else f"{sum_g:02x}"}"\
            f"{sum_b if sum_b <= 99 else f"{sum_b:02x}"}"\
            f"{sum_r if sum_b <= 99 else f"{sum_b:02x}"}",
        "brg" : f"{sum_b if sum_b <= 99 else f"{sum_b:02x}"}"\
            f"{sum_r if sum_r <= 99 else f"{sum_r:02x}"}"\
            f"{sum_g  if sum_g <= 99 else f"{sum_g:02x}"}"
    }
    
    return order_dict.get(order)

def rgb_to_hex(r: int, g: int, b: int)-> str:
    return f"#{r:02x}{b:02x}{g:02x}"

def with_max(order: str="rgb", level: str="light")-> str:
    date_max = max(my_date_list_int)
    
    color_dict = {}
    
    if level == "light":
        color_dict.update({
            "rgb" : f"{date_max}ffff",
            "gbr" : f"ffff{date_max}",
            "brg" : f"ff{date_max}ff",
        })
    elif level == "mid0":
        color_dict.update({
            "rgb" : f"{date_max}00ff",
            "gbr" : f"00ff{date_max}",
            "brg" : f"00{date_max}ff",
        })
    elif level == "midf":
        color_dict.update({
            "rgb" : f"{date_max}ff00",
            "gbr" : f"ff00{date_max}",
            "brg" : f"ff{date_max}00",
        })
    else:
        color_dict.update({
            "rgb" : f"{date_max}0000",
            "gbr" : f"0000{date_max}",
            "brg" : f"00{date_max}00",
        })
        
    return color_dict.get(order)

def full_year(order: str="rgb", level: str="light")-> str:
    year = ("").join(my_date_list_str[-2:]) if len(my_date_list_str) == 4 else f"19{my_date_list_str[-1]}"
    
    color_dict = {}
    
    if level == "light":
        color_dict.update({
            "rgb" : f"{year}ff",
            "gbr" : f"ff{year}",
            "brg" : f"f{year}f",
        })
    elif level == "mid0":
        color_dict.update({
            "rgb" : f"{year}0f",
            "gbr" : f"0f{year}",
            "brg" : f"0{year}f",
        })
    elif level == "midf":
        color_dict.update({
            "rgb" : f"{year}f0",
            "gbr" : f"f0{year}",
            "brg" : f"f{year}0",
        })
    else:
        color_dict.update({
            "rgb" : f"{year}00",
            "gbr" : f"00{year}",
            "brg" : f"0{year}0",
        })
        
    return color_dict.get(order)

def hex_to_rgb(color: str)-> tuple[int]:
    
    r, g, b = date_to_color(date=color)
    
    return int(r, 16), int(g, 16), int(b, 16)

grey = total_date if len(total_date) == 2 else f"0{total_date}"
grey_dark = total_date_dark if len(total_date_dark) == 2 else f"0{total_date_dark}"
grey_light = total_date_light if len(total_date_light) == 2 else f"0{total_date_light}"
grey_lighter = total_date_lighter if len(total_date_lighter) == 2 else f"0{total_date_lighter}"

change_color_base: dict[str, str] = {
    "date brg" : date_to_color(my_date, order="brg"),
    "date gbr" : date_to_color(my_date, order="gbr"),
    "date rgb" : date_to_color(my_date, order="rgb"),
    "dark brg": darkest_color(my_date, "brg"),
    "dark gbr": darkest_color(my_date, "gbr"),
    "dark rgb" : darkest_color(my_date),
    "grey" : f"{grey * 3}",
    "grey dark" : f"{grey_dark * 3}",
    "grey light" : f"{grey_light * 3}",
    "grey lighter" : f"{grey_lighter * 3}",
    "invert brg" : date_to_color(my_date, order="brg")[::-1],
    "invert gbr" : date_to_color(my_date, order="gbr")[::-1],
    "invert rgb" : date_to_color(my_date, order="rgb")[::-1],
    "invert dark brg": darkest_color(my_date, "brg")[::-1],
    "invert dark gbr": darkest_color(my_date, "gbr")[::-1],
    "invert dark rgb" : darkest_color(my_date)[::-1],
    "invert light brg" : lightest_color(my_date, order="brg")[::-1],
    "invert light gbr" : lightest_color(my_date, order="gbr")[::-1],
    "invert light rgb" : lightest_color(my_date, order="rgb")[::-1],
    "invert light from dark brg": darkest_color(my_date, "brg", True)[::-1],
    "invert light from dark gbr": darkest_color(my_date, "gbr", True)[::-1],
    "invert light from dark rgb" : darkest_color(my_date, light=True)[::-1],
    "light brg" : lightest_color(my_date, order="brg"),
    "light gbr" : lightest_color(my_date, order="gbr"),
    "light rgb" : lightest_color(my_date, order="rgb"),
    "light from dark brg": darkest_color(my_date, "brg", True),
    "light from dark gbr": darkest_color(my_date, "gbr", True),
    "light from dark rgb" : darkest_color(my_date, light=True),
    "max in date dark brg" : with_max("brg", "dark"),
    "max in date dark gbr" : with_max("gbr", "dark"),
    "max in date dark rgb" : with_max("rgb", "dark"),
    "max in date light brg" : with_max("brg", "light"),
    "max in date light gbr" : with_max("gbr", "light"),
    "max in date light rgb" : with_max("rgb", "light"),
    "max in date mid0 brg" : with_max("brg", "mid0"),
    "max in date mid0 gbr" : with_max("gbr", "mid0"),
    "max in date mid0 rgb" : with_max("rgb", "mid0"),
    "max in date midf brg" : with_max("brg", "midf"),
    "max in date midf gbr" : with_max("gbr", "midf"),
    "max in date midf rgb" : with_max("rgb", "midf"),
    "white" : f"{total_date_white * 3}",
    "year dark brg" : full_year("brg", "dark"),
    "year dark gbr" : full_year("gbr", "dark"),
    "year dark rgb" : full_year("rgb", "dark"),
    "year light brg" : full_year("brg", "light"),
    "year light gbr" : full_year("gbr", "light"),
    "year light rgb" : full_year("rgb", "light"),
    "year mid0 brg" : full_year("brg", "mid0"),
    "year mid0 gbr" : full_year("gbr", "mid0"),
    "year mid0 rgb" : full_year("rgb", "mid0"),
    "year midf brg" : full_year("brg", "midf"),
    "year midf gbr" : full_year("gbr", "midf"),
    "year midf rgb" : full_year("rgb", "midf")
}

data_list = [
    "GIMP Palette",
    "Columns: 3",
    f"# {len(change_color_base)} Colors",
    "# R G B Color name"
    ]

data_dict = {}

key_len = [len(k[0]) for k in change_color_base.items()]
line_dict = [len(k) + len(v) for k, v in change_color_base.items()]
space = max(line_dict) - len(my_date) + 10
before = round(space / 2)
after = space - before

print(f"[bold underline {'#00FF86'}]{" " * before}{my_date}{" " * after}[/]")
    
for k, v in sorted(change_color_base.items(), key=lambda item: item[0]):
    
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
    
print(f"[{'#00FF86'}]{len(change_color_base)} colors[/]")
saving = input(f"save the colors to a file (y/n) --> ").lower().strip()

if saving == "y":

    name_file = input(f"Give the files a name --> ").strip().replace(" ", "_").lower()
    
    data_list.insert(1, f"Name: {name_file.replace("_", " ").capitalize()}")
        
    tools.save_file(data=data_list, file_name=f"{name_file}.gpl", is_json=False)
    tools.save_file(data=data_dict, file_name=f"{name_file}.json")
