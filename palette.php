#!/usr/bin/php
<?php
$levels = [0, 128, 255];
$channels = 3;
$indexes = array_fill(0, $channels, 0);
$n = pow(count($levels), $channels);

$size = 10;
$img = imagecreatetruecolor($n * $size, $size);
for ($i = 0; $i < $n; $i ++)
{
	$color = 0;
	for ($k = 0; $k < $channels; $k ++)
	{
		$color <<= 8;
		$color |= $levels[$indexes[$k]];
	}
	imagefilledrectangle($img, $i * $size, 0, ($i + 1) * $size, $size, $color);

	for ($j = $channels - 1; $j >= 0; $j --)
	{
		$indexes[$j] ++;
		if ($indexes[$j] == count($levels))
		{
			$indexes[$j] = 0;
		}
		else
		{
			break;
		}
	}
}

if (!isset($argv[1]))
{
	die('Output file not specified!' . PHP_EOL);
}
$path = $argv[1];
if (file_exists($path))
{
	die('File "' . $path . '" already exists!' . PHP_EOL);
}
imagepng($img, $path);
