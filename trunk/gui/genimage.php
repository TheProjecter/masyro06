<?php
$img = imagecreatetruecolor($_GET['wz'],$_GET['hz']);
$org_img = imagecreatefromjpeg($_GET['img']);
$ims = getimagesize($_GET['img']);

$pX = ($_GET['x']*$ims[0])/$_GET['wo'];
$pY = ($_GET['y']*$ims[1])/$_GET['ho'];
$w = ($_GET['w']*$ims[0])/$_GET['wo'];
$h = ($_GET['h']*$ims[1])/$_GET['ho'];
// resource dst_im, resource src_im, int dstX, int dstY, int srcX, int srcY, int dstW, int dstH, int srcW, int srcH )
imagecopyresized($img,$org_img, 0, 0, $pX, $pY, $_GET['wz'], $_GET['hz'], $w, $h);
imagerectangle ($img, 0, 0, $_GET['wz']-1, $_GET['hz']-1, 0);
header('Content-type: image/png');
imagejpeg($img,"", 85);
imagedestroy($img);
?>
