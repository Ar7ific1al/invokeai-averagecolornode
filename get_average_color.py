from invokeai.app.invocations.primitives import (
    ImageField,
    ColorField,
    ColorOutput
)
from invokeai.app.invocations.baseinvocation import(
    BaseInvocation,
    InputField,
    InvocationContext,
    invocation
)


@invocation("average_color", title = "Average Color", tags = ["primitives", "color"], category = "primitives", version = "1.0.0")
class AverageColorInvocation(BaseInvocation):
    """ Get the average color of the input image """

    #   Inputs
    image:          ImageField  = InputField(description = "Input image to average")

    def invoke(self, context: InvocationContext) -> ColorOutput:
        image = context.services.images.get_pil_image(self.image.image_name)
        
        # Convert the image to RGB mode if not already
        image = image.convert("RGB") if image.mode != "RGB" else image

        # Calculate the average color
        pixel_data = list(image.getdata())
        total_pixels = len(pixel_data)
        average_color = tuple(map(lambda x: sum(x) // total_pixels, zip(*pixel_data)))
        
        average_color = ColorField(r = average_color[0], g = average_color[1], b = average_color[2], a = 255)

        return ColorOutput(
            color = average_color
        )