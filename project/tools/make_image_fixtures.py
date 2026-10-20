"""Render synthetic, shareable job-advert test fixtures (no real applicant data)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FOLDER = Path(__file__).resolve().parents[1] / "tests/images"
FOLDER.mkdir(parents=True, exist_ok=True)


def font(size):
    return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)


def advert(title, requirements):
    image = Image.new("RGB", (1100, 800), "#f4f4ed")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1100, 120), fill="#214d43")
    draw.text((50, 40), "JOB OPPORTUNITY", font=font(40), fill="white")
    draw.text((50, 170), title, font=font(42), fill="#214d43")
    draw.text((50, 270), "Requirements", font=font(31), fill="#214d43")
    for number, requirement in enumerate(requirements):
        draw.text((65, 330 + number * 70), "- " + requirement, font=font(29), fill="#263c35")
    draw.text((50, 730), "SYNTHETIC COURSE FIXTURE - not a real vacancy", font=font(21), fill="#66735f")
    return image


clean = advert("Junior Frontend Developer", ["HTML and CSS", "JavaScript", "Accessible forms and keyboard navigation"])
clean.save(FOLDER / "clean.jpg", quality=90)
degraded = clean.copy()
ImageDraw.Draw(degraded).rectangle((25, 145, 1075, 245), fill="#b5b5af")
degraded = degraded.filter(ImageFilter.GaussianBlur(2.5))
degraded.save(FOLDER / "degraded.jpg", quality=35)
advert("Junior / Senior Developer", ["Python", "Team collaboration"]).save(FOLDER / "ambiguous.jpg", quality=90)
unrelated = Image.new("RGB", (900, 650), "#fff6df")
draw = ImageDraw.Draw(unrelated)
draw.text((60, 80), "Shopping list", font=font(48), fill="#6b4c2a")
draw.multiline_text((60, 190), "Milk\nBread\nApples", font=font(40), fill="#6b4c2a", spacing=25)
draw.text((50, 580), "SYNTHETIC COURSE FIXTURE", font=font(22), fill="#6b4c2a")
unrelated.save(FOLDER / "not-applicable.jpg", quality=90)
print("Created four synthetic JPEG fixtures.")
