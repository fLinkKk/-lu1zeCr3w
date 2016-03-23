# php Code to decrypt data using aes 256bit in cbc mode
# Enter data in base64!!!!
# dataIN is the encrypted input data encoded in base64

<?php

function decrypt_data($data, $iv, $key) {
	$cypher = mcrypt_module_open(MCRYPT_RIJNDAEL_256, '', MCRYPT_MODE_CBC, '');

	if (mcrypt_generic_init($cypher, $key, $iv) != -1) {
		$decrypted = mdecrypt_generic($cypher, base64_decode($data));

		mcrypt_generic_deinit($cypher);
		mcrypt_module_close($cypher);

		return $decrypted;
	}

	return false;
}

$dataIN = $argv[1];

$iv = "";
$key = "";

$decr = decrypt_data($dataIN, $iv, $key);

echo $decr
?>
