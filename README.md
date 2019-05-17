# color_classification
Script to return top three dominant colors from an image. 

Input: 
 - image filepath
 
Output: 
 - json string with RGB and Hex for the most prominant colors: 
 
 >>> python hsv_classify.py -i ./fohrtest/fohrimage2.jpg
 
 ```
{"first_color": {"red": 151, "green": 133, "blue": 123, "hex": "#97857b"}, "second_color": {"red": 138, "green": 133, "blue: ": 111, "hex": "#8a796f"}, "third_color": {"red": 166, "green": 133, "blue": 135, "hex": "#a69287"}}
```
