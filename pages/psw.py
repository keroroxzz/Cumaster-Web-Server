# Psswords generation and length setting 
import numpy as np

psw_length = 16

# psw word table
psw_elements = [chr(i) for i in range(48, 58)]+\
    [chr(i) for i in range(65, 91)]+\
    [chr(i) for i in range(97, 123)]

# generate psw
def generatepsw(length):
    psw_int = np.random.randint(0, len(psw_elements), (length), dtype=int)
    pse_chr = [psw_elements[i] for i in psw_int]
    return ''.join(pse_chr) 