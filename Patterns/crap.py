import os, resource, hashlib
from Crypto.Cipher import AES
from Crypto import Random


def swap(fname,destroy):
    data = []
    for line in open(fname,'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


def aes_encrypt(password, message):
    key = hashlib.sha256(password).hexdigest()[0:16]
    iv = Random.new().read(AES.block_size)
    ciph = AES.new(key, AES.MODE_CFB, iv)
    return ciph.encrypt(bytes(message)), iv


def aes_decrypt(ciphertext, password, iv):
    key = hashlib.sha256(password).hexdigest()[0:16]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(bytes(ciphertext))


def check_mem_usage():
    """
    Check the current memory usage of program
    :return: Current RAM usage in bytes
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def encrypt_txt_file(fnamein, fnameout, destroy, password):
    data = swap(fnamein, destroy)
    contents = ''
    for line in data:
        contents += line

    encrypted_data, ivP = aes_encrypt(password, contents)
    dat = ''
    for character in encrypted_data:
        dat += character
    open(fnameout,'w').write(encrypted_data)
    return ivP


def decrypt_text_file(fnamein, fnameout, password, iV, destroy):
    encdata = swap(fnamein,destroy)
    contents = ''
    for element in encdata:
        contents += element
    # Now write the clear text into output file
    clear_text = aes_decrypt(contents, password, iV)
    open(fnameout,'w').write(clear_text)


def example():
    # Example of encrypting the contents of a text file (without deleting original)
    IV = encrypt_txt_file('example.txt', 'encrypted_example.txt', False, '5up3Rwe1Rd5417d00d')
    # Example of Decrypting previously created file
    decrypt_text_file('encrypted_example.txt', 'decrypted_example.txt', '5up3Rwe1Rd5417d00d', IV, False)
    print "_______________________________________________________________________________________"
    os.system('cat encrypted_example.txt')
    print "\n_______________________________________________________________________________________"
    os.system('cat decrypted_example.txt')
    print "\n_______________________________________________________________________________________"
    os.system('cmp example.txt decrypted_example.txt')


def main():
    mem_overhead = check_mem_usage()
    print str(float(mem_overhead) / 1000) + " kilobytes in RAM overhead"

    example()


if __name__ == '__main__':
    main()
