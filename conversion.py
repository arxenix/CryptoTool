import xml.etree.cElementTree as ET
import base64
from Crypto.Util.asn1 import *

def toBinary(num):
    return "{0:b}".format(num)

def toHex(num):
    return "{0:x}".format(num)

def toPaddedHex(num):
    hex = toHex(num)
    if len(hex)%2==1:
        hex = "0"+hex
    return hex

def toBase64(num):
    hex = toHex(num)
    if len(hex)%2==1:
        hex = "0"+hex
    return base64.b64encode(hex.decode('hex'))

def fromBase64(x):
    return int(base64.b64decode(x).encode('hex'),16)

def privateToXMLDSigFile(privateKey, file):
    root = ET.Element("RSAKeyPair")
    ET.SubElement(root, "Modulus").text = toBase64(privateKey.n)
    ET.SubElement(root, "Exponent").text = toBase64(privateKey.e)
    ET.SubElement(root, "P").text = toBase64(privateKey.p)
    ET.SubElement(root, "Q").text = toBase64(privateKey.q)
    ET.SubElement(root, "DP").text = toBase64(privateKey.dp)
    ET.SubElement(root, "DQ").text = toBase64(privateKey.dq)
    ET.SubElement(root, "InverseQ").text = toBase64(privateKey.invq)
    ET.SubElement(root, "D").text = toBase64(privateKey.d)
    tree = ET.ElementTree(root)
    tree.write(file)

def publicToXMLDSigFile(publicKey, file):
    root = ET.Element("RSAKeyValue")
    ET.SubElement(root, "Modulus").text = toBase64(publicKey.n)
    ET.SubElement(root, "Exponent").text = toBase64(publicKey.e)
    tree = ET.ElementTree(root)
    tree.write(file)

def privateToXMLDSigHexFile(privateKey, file):
    root = ET.Element("RSAKeyPair")
    ET.SubElement(root, "Modulus", EncodingType="hexBinary").text = toHex(privateKey.n).upper()
    ET.SubElement(root, "Exponent", EncodingType="hexBinary").text = toHex(privateKey.e).upper()
    ET.SubElement(root, "P", EncodingType="hexBinary").text = toHex(privateKey.p).upper()
    ET.SubElement(root, "Q", EncodingType="hexBinary").text = toHex(privateKey.q).upper()
    ET.SubElement(root, "DP", EncodingType="hexBinary").text = toHex(privateKey.dp).upper()
    ET.SubElement(root, "DQ", EncodingType="hexBinary").text = toHex(privateKey.dq).upper()
    ET.SubElement(root, "InverseQ", EncodingType="hexBinary").text = toHex(privateKey.invq).upper()
    ET.SubElement(root, "D", EncodingType="hexBinary").text = toHex(privateKey.d).upper()
    tree = ET.ElementTree(root)
    tree.write(file)
    file.close()

def toASN1(num):
    hex = toPaddedHex(num)
    length = toPaddedHex(len(hex)/2)
    return "02"+length+hex

def privateToPEM(privateKey):
    seq = DerSequence()
    seq.append(0)
    seq.append(privateKey.n)
    seq.append(privateKey.e)
    seq.append(privateKey.d)
    seq.append(privateKey.p)
    seq.append(privateKey.q)
    seq.append(privateKey.dp)
    seq.append(privateKey.dq)
    seq.append(privateKey.invq)
    return base64.b64encode(seq.encode())

def privateToPEMFile(privateKey, file):
    pem = privateToPEM(privateKey)
    pemlines = [pem[i:i+64] for i in range(0, len(pem), 64)]
    print pemlines
    file.write("-----BEGIN RSA PRIVATE KEY-----\n")
    for line in pemlines:
        file.write(line+"\n")
    file.write("-----END RSA PRIVATE KEY-----\n")
    file.close()
