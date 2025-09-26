from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
# ---------------------------
# 配置参数
# ---------------------------
KEY_SIZE = 16  # AES-128: 16字节, AES-192: 24字节, AES-256: 32字节
BLOCK_SIZE = 16  # AES 块大小固定为 16 字节

# ---------------------------
# 示例密钥（实际应用中应安全生成和存储）
# ---------------------------
# 方式1：使用 16 字节随机密钥（推荐）


# 方式2：从字符串或 hex 生成密钥（仅用于测试）
# key = b'mykey12345678901'  # 必须是 16/24/32 字节
# key = bytes.fromhex('e45a1f418d2e4f56531f2aef...')  # 你的 JS 转换后的 key

# print(f"Key (hex): {key.hex()}")

# ---------------------------
# 加密函数
# ---------------------------
def aes_cbc_encrypt(plaintext):

    key = bytes.fromhex("8f235bc1cac17a46530c616ff234be78")
    # 确保明文是 bytes
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    # 生成随机 IV（初始化向量）
    
    iv =bytes.fromhex("69783956775867344e5853626b645431")

    # 创建 AES-CBC 加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 填充并加密
    padded_data = pad(plaintext, BLOCK_SIZE)  # PKCS#7 填充
    ciphertext = cipher.encrypt(padded_data)

    # 返回 base64 编码的 IV + 密文（便于传输）
    encrypted_data = ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

# ---------------------------
# 解密函数
# ---------------------------
def aes_cbc_decrypt(encrypted_b64):
    key = bytes.fromhex("8f235bc1cac17a46530c616ff234be78")
    # 从 base64 解码
    encrypted_data = base64.b64decode(encrypted_b64)
    iv =bytes.fromhex("69783956775867344e5853626b645431")

    # 提取 IV 和密文
    # iv = encrypted_data[:BLOCK_SIZE]
    ciphertext = encrypted_data

    # 创建 AES-CBC 解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密并去填充
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, BLOCK_SIZE)  # 去除 PKCS#7 填充

    return plaintext.decode('utf-8')


def str_to_md5(text):
    """
    将字符串转换为 MD5 哈希值（十六进制字符串）
    """
    # 将字符串编码为字节，再计算 MD5
    md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    return md5_hash

# # 示例
# text = "appid=100008370&business_site=search_airticketscivil_online_pic&version=2.0.30&dimensions=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&extend_param=ak7Oj2doYMHGkXZ9ST5pJogOCCG///HWQ/Kl32rGeNM002Mgcr3MiJwWHR9bljN00C+H3pGS0QkTS+cybU5kHGoF2BK4PqNKEZeBioYzoyA="
# md5_value = str_to_md5(text)
# print(f"MD5: {md5_value}")
# # 输出: MD5: 6c23dbab02d3d83486380554237d28fe
# # ---------------------------
# # 使用示例
# # ---------------------------
# message = r'{"resolution_width":1920,"resolution_height":1080,"language":""}'

# # 加密
# encrypted = aes_cbc_encrypt(message)
# print(f"Encrypted (base64): {encrypted}")
# encrypted = 'ak7Oj2doYMHGkXZ9ST5pJogOCCG///HWQ/Kl32rGeNM002Mgcr3MiJwWHR9bljN00C+H3pGS0QkTS+cybU5kHGoF2BK4PqNKEZeBioYzoyA='
# # 解密
# decrypted = aes_cbc_decrypt(encrypted)
# print(f"Decrypted: {decrypted}")