# Optimized images

Images were resized to 2x target size in px using Lanczos3:

- `circle*`: 256x256px
- `default_avatar`: 500x500px
- images used in content (not background) can't be wider than 880px: width 1760px (or original smaller), height to keep aspect ratio
- background: (assume 4k) original size

## Compression

I've used [Squoosh](https://squoosh.app) with the following encoders at maximum effort:

- AVIF (manually tuned quality in range 30-~~40~~45)
- JPEG XL (lossless with slight loss enabled for small images, manually tuned loss in range 75-80 and progressive rendering for other)
- OxiPNG (unless the original is JPEG)
- WebP (manually tuned quality in range 75-90)

## Results

The perceived quality should be PNG, JPEG XL, WebP/AVIF, but without significant differences. AVIF sometimes has colours slightly different from original.\
Ordered from smallest to largest (small images):

1. AVIF
2. WebP (~2x AVIF)
3. JPEG XL (~3x-17x AVIF)
4. PNG (~4x-23x AVIF)

In large images the size differences are smaller and JPEG XL sometimes can beat WebP.

### Load order

For small images it makes sense to load them in order by size, but for bigger JPEG XL is preferred because of progressive rendering, unless AVIF is much smaller (~2x).
