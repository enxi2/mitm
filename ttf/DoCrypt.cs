using System;

class DoCrypt {
    public static string gameKey = "?";

    public static string AES_encrypt(string Input, string key)
    {
        RijndaelManaged rijndaelManaged = new RijndaelManaged();
        rijndaelManaged.KeySize = 256;
        rijndaelManaged.BlockSize = 128;
        rijndaelManaged.Mode = CipherMode.CBC;
        rijndaelManaged.Padding = PaddingMode.PKCS7;
        rijndaelManaged.Key = Encoding.UTF8.GetBytes(key);
        rijndaelManaged.IV = new byte[16];
        ICryptoTransform transform = rijndaelManaged.CreateEncryptor(rijndaelManaged.Key, rijndaelManaged.IV);
        byte[] inArray = null;
        using (MemoryStream memoryStream = new MemoryStream()) {
            using (CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Write)) {
                byte[] bytes = Encoding.UTF8.GetBytes(Input);
                cryptoStream.Write(bytes, 0, bytes.Length);
            }
            inArray = memoryStream.ToArray();
        }
        return Convert.ToBase64String(inArray);
    }

    public static string AES_decrypt(string Input, string key)
    {
        ICryptoTransform transform = new RijndaelManaged {
            KeySize = 256,
            BlockSize = 128,
            Mode = CipherMode.CBC,
            Padding = PaddingMode.PKCS7,
            Key = Encoding.UTF8.GetBytes(key),
            IV = new byte[16]
        }.CreateDecryptor();
        byte[] bytes = null;
        using (MemoryStream memoryStream = new MemoryStream()) {
            using (CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Write)) {
                byte[] array = Convert.FromBase64String(Input);
                cryptoStream.Write(array, 0, array.Length);
            }
            bytes = memoryStream.ToArray();
        }
        return Encoding.UTF8.GetString(bytes);
    }

    static void Main(string[] args) {
        Console.WriteLine("[{0}]", string.Join(", ", args));
        if ("decrypt".Equals(args[0])) {
            string encryptedData = System.IO.File.ReadAllText(args[1]);
            string decryptedData = AES_decrypt(encryptedData, gameKey);
            System.IO.File.WriteAllText(args[2], decryptedData);
        }
        else if ("encrypt".Equals(args[0])) {
            string decryptedData = System.IO.File.ReadAllText(args[1]);
            string encryptedData = AES_encrypt(decryptedData, gameKey);
            System.IO.File.WriteAllText(args[2], encryptedData);
        }
    }
}
