from pathlib import Path
from django.core.files import File
from shop.models import Product

media_dir = Path("media/products")

for product in Product.objects.all():
    if not product.image:
        print(f"NO IMAGE: {product.name}")
        continue

    filename = Path(product.image.name).name
    local_file = media_dir / filename

    if local_file.exists():
        print(f"Uploading: {filename}")

        with open(local_file, "rb") as f:
            product.image.save(
                filename,
                File(f),
                save=True
            )

        print(f"SUCCESS: {product.name}")
    else:
        print(f"LOCAL FILE NOT FOUND: {filename}")