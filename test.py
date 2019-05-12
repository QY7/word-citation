from colorama import init
from colorama import Fore, Back, Style


init()

print(Fore.WHITE + 'some red text')
print(Back.BLUE + 'and with a green background')
print(Style.RESET_ALL)
print('back to normal now')