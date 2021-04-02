import re
import datetime

# Validade CPF
def validadeCPF(value):
    return re.search("\d{3}.?\d{3}.?\d{3}-?\d{2}", value)


# Validade CPF
def validadeEmail(value):
    return re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', value)

# capitalize the word
def capitalizeWord(value):
    return value.upper()

def validadeRg(value):
    return re.search('(^\d{1,2}).?(\d{3}).?(\d{3})-?(\d{1}|X|x$)',value)

def validadeTelefone(value):
    return re.search('(^[0-9]{2})?(\s|-)?(9?[0-9]{4})-?([0-9]{4}$)',value)

def validadeCep(value):
    return re.search('(^[0-9]{5})-?([0-9]{3}$)', value)

# * Password of at least 6 characters, at least one uppercase letter, at least one lowercase letter, at least one number, at least one special character
def validadePassword(value):
    return re.search('(?=^.{6,}$)((?=.*\w)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[|!"$%&\/\(\)\?\^\'\\\+\-\*]))^.*', value)

def validadeDate(value):
    format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(value, format)
        return True
    except ValueError:
        return False
    
def validadeNumber(value):
    return re.search('^[0-9]+$', value)
#Debug
# x = validadeDate('2021-04-02')
# print(x)
# if x:
#     print('ihul')
# else:
#     print('aff')