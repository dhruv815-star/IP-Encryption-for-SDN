import csv
import struct
import sys

# declaring key here
KEY = '\xff'*16
# CSV delimiter character
DELIMITER = ','  


def rotl(b, r):
    return ((b << r) & 0xff) | (b >> (8 - r))


def permute_fwd(state):
    (b0, b1, b2, b3) = state
    b0 += b1
    b2 += b3
    b0 &= 0xff
    b2 &= 0xff
    b1 = rotl(b1, 2)
    b3 = rotl(b3, 5)
    b1 ^= b0
    b3 ^= b2
    b0 = rotl(b0, 4)
    b0 += b3
    b2 += b1
    b0 &= 0xff
    b2 &= 0xff
    b1 = rotl(b1, 3)
    b3 = rotl(b3, 7)
    b1 ^= b2
    b3 ^= b0
    b2 = rotl(b2, 4)
    return (b0, b1, b2, b3)


def permute_bwd(state):
    (b0, b1, b2, b3) = state
    b2 = rotl(b2, 4)
    b1 ^= b2
    b3 ^= b0
    b1 = rotl(b1, 5)
    b3 = rotl(b3, 1)
    b0 -= b3
    b2 -= b1
    b0 &= 0xff
    b2 &= 0xff
    b0 = rotl(b0, 4)
    b1 ^= b0
    b3 ^= b2
    b1 = rotl(b1, 6)
    b3 = rotl(b3, 3)
    b0 -= b1
    b2 -= b3
    b0 &= 0xff
    b2 &= 0xff
    return (b0, b1, b2, b3)


def xor4(x, y):
    return [(x[i] ^ y[i]) & 0xff for i in (0, 1, 2, 3)]


#encrypting the input ip address
def encrypt(key, ip):
    """16-byte key, ip string like '192.168.1.2'"""
    try:
        state = [int(x) for x in ip.split('.')] #splitting accross .
    except ValueError:
        raise
    try:
        state = xor4(state, [ord(x) for x in key[:4]])
        state = permute_fwd(state)
        state = xor4(state, [ord(x) for x in key[4:8]])
        state = permute_fwd(state)
        state = xor4(state, [ord(x) for x in key[8:12]])
        state = permute_fwd(state)
        state = xor4(state, [ord(x) for x in key[12:16]])
    except IndexError:
        raise
    return '.'.join(str(x) for x in state)

#decrypting the encrypted ip address
def decrypt(key, ip):
    """16-byte key, encrypted ip string like '215.51.199.127'"""
    try:
        state = [int(x) for x in ip.split('.')] #splitting accross .
    except ValueError:
        raise
    try:
        state = xor4(state, [ord(x) for x in key[12:16]])
        state = permute_bwd(state)
        state = xor4(state, [ord(x) for x in key[8:12]])
        state = permute_bwd(state)
        state = xor4(state, [ord(x) for x in key[4:8]])
        state = permute_bwd(state)
        state = xor4(state, [ord(x) for x in key[:4]])
    except IndexError:
        raise
    return '.'.join(str(x) for x in state)


def usage():
    print('usage:  %s csvfile index e|d'  % sys.argv[0])
    print('\tindex = csv index in 0, 1, ...')
    print('\te = encrypt, d = decrypt')
    sys.exit(1)


def test():
    """basic encryption sanity check"""
    ip = init = '1.2.3.4'
    key = '\xff'*16 
    iterations = 10
    for i in range(iterations):
        ip = encrypt(key, ip)
    if ip != '191.207.11.210':
        raise ValueError
    for i in range(iterations):
        ip = decrypt(key, ip)
    if ip != init:
        raise ValueError

def clean_csv(input_file, output_file):

    with open(input_file, "rb") as f:
        content = f.read()

    # Remove NULL characters
    cleaned_content = content.replace(b'\x00', b'')

    with open(output_file, "wb") as f:
        f.write(cleaned_content)


def main():
    assert len(KEY) == 16
    try:
        test()
    except ValueError:
        print('test failed')
        sys.exit(1)

    try:
        filein = sys.argv[1]
        fileout = sys.argv[2]
        index = int(sys.argv[3])
        index2 = int(sys.argv[4])
        mode = sys.argv[5]
    except:
        usage()

    if mode == 'e':
        process = encrypt
    elif mode == 'd':
        process = decrypt
    else:
        usage()

    with open(filein, 'r') as csvfile:
        with open(fileout, 'w', newline='') as cfile:
            reader = csv.reader(csvfile, delimiter=DELIMITER)
            writer = csv.writer(cfile, delimiter=DELIMITER)

            for row in reader:
                ip = row[index].strip()
                ip2 = row[index2].strip()
                newrow = row
                try:
                    newrow[index] = process(KEY, ip)
                    newrow[index2] = process(KEY, ip2)
                except:
                    continue
                writer.writerow(newrow)


if __name__ == '__main__':
    sys.exit(main())
