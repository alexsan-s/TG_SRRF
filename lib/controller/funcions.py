import re

# Validade CPF
def validadeCPF(value):
    return re.search("\d{3}.?\d{3}.?\d{3}-?\d{2}", value)


# Validade CPF
def validadeEmail(value):
    return re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', value)
