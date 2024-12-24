from quicktex import dds
from PIL import Image
import matplotlib.pyplot as plt

dds_fn = "s88750_em.dds"

dds_obj = dds.read(dds_fn)
image = dds_obj.decode()

plt.imshow(image)
plt.axis('off')
plt.show()
