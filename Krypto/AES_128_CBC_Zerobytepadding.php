<?php
# Resulting cipher text has no integrity or authenticity added
# and is not protected against padding oracle attacks.

# --- DECRYPTION ---
$path="c2.txt";
//$key="9c467317a06b113d1e47f6ba9fa2ad234613613d2f90ea481586ffe21e68c5046ec55f51bff52b58659e97416421502ab503955c788980eca22dfec";
$key="366c476f3547544e475071356149557a";
//$key="5a2edea42cf17380bd395b4065f51b806c86daf1c9cfffb07c7701f505a3f5305de6af3c2b1503908b59ba7bd6d7c50095ef7cafd20156005dd1ecd62586d630";
$iv_size=8;
$ciphertext_base64=file_get_contents($path);
//echo($ciphertext_base64);
$ciphertext_dec = base64_decode($ciphertext_base64);
//echo($ciphertext_dec);
# retrieves the IV, iv_size should be created using mcrypt_get_iv_size()
$iv_dec = substr($ciphertext_dec, 0, $iv_size);
$iv_dec = "0123456789abcdef";
# retrieves the cipher text (everything except the $iv_size in the front)
//$ciphertext_dec = substr($ciphertext_dec, $iv_size);

# may remove 00h valued characters from end of plain text
$plaintext_dec = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key,
$ciphertext_dec, MCRYPT_MODE_CBC, $iv_dec);

echo  $plaintext_dec . "\n";

?>