#! task
import re

text = "abbb"

pattern = r"ab*"

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")


#2 task
import re

text = "abbb"

pattern = r"ab{2,3}"

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")


#3 task
import re

text = "hello_world test_string Python"

pattern = r"[a-z]+_[a-z]+"

print(re.findall(pattern, text))


#4 task
import re

text = "Hello world Python Language"

pattern = r"[A-Z][a-z]+"

print(re.findall(pattern, text))


#5 task
import re

text = "axxxb"

pattern = r"a.*b"

if re.fullmatch(pattern, text):
    print("Match found")


#6 task
import re

text = "Hello, world. Python is cool"

result = re.sub(r"[ ,.]", ":", text)

print(result)


#7 task
import re

text = "hello_world_python"

result = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(result)
 

#8 task
import re

text = "HelloWorldPython"

result = re.split(r"(?=[A-Z])", text)

print(result)


#9 task
import re

text = "HelloWorldPython"

result = re.sub(r"(?<!^)([A-Z])", r" \1", text)

print(result)


#10 task
import re

text = "helloWorldPython"

result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)