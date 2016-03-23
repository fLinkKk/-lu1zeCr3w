# Encrypts data using aes 256 bit CBC
# Enter data to crypt in base64!!
# returns data encoded in base64

<?php
function encrypt_data($data, $iv, $key) {
	$cypher = mcrypt_module_open(MCRYPT_RIJNDAEL_256, '', MCRYPT_MODE_CBC, '');

	if (mcrypt_generic_init($cypher, $key, $iv) != -1) {
		$decrypted = mcrypt_generic($cypher, base64_decode($data));

		mcrypt_generic_deinit($cypher);
		mcrypt_module_close($cypher);

		return $decrypted;
	}

	return false;
}

$iv = "";
$key = "";

$data = $argv[1];
$encr = base64_encode(encrypt_data($data, $iv, $key));

echo $encr;
?>
