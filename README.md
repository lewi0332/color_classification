# color_classification
Script to return top three dominant colors from an image. 

Code revised from Adam Spannbauer's icon color sorting: https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/

Input: 
 - image filepath
 - image URL
 
Output: 
 - json string with RGB and Hex for the most prominant colors: 
 
 ```
 >>> python hsv_classify.py -i ./fohrtest/fohrimage2.jpg
 
{"first_color": {"red": 151, "green": 133, "blue": 123, "hex": "#97857b"}, "second_color": {"red": 138, "green": 133, "blue: ": 111, "hex": "#8a796f"}, "third_color": {"red": 166, "green": 133, "blue": 135, "hex": "#a69287"}}
```
