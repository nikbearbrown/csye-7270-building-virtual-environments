extends Node

func add_padding(texture: Texture2D, pad: int) -> ImageTexture:
	var source := texture.get_image()
	if source.is_compressed():
		source.decompress()
	source.convert(Image.FORMAT_RGBA8)
	var size := source.get_size() + Vector2i(pad, pad) * 2
	var padded := Image.create_empty(size.x, size.y, false, Image.FORMAT_RGBA8)
	padded.fill(Color(0, 0, 0, 0))
	padded.blit_rect(source, Rect2i(Vector2i.ZERO, source.get_size()), Vector2i(pad, pad))
	return ImageTexture.create_from_image(padded)
