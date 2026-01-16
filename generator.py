from styles import Big, Cursive, CursiveBold, Hollow

normal = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:'",.<>/?`~\\"""

def generate(string, style):
    fancy = globals()[style].get()
    result = ''
    for symbol in string:
        i = normal.find(symbol)
        if i == -1:
            result += symbol
            continue
        result += fancy[i]
    return result