def disc_to_cont(i,j):
    x = round(2*(i - 13.5))
    z = round(2*(j - 23))
    return x,z

def cont_to_disc(x,z):
    i = round(x/2 + 13.5)
    j = round(z/2 + 23)
    return i,j
