"""Image upscaler tool using AI models for maximum quality."""

from pathlib import Path
from typing import Any, Dict, Optional

from claude_tools.core.base_tool import BaseTool

try:
    import cv2
    import numpy as np
    from PIL import Image

    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# AI upscaling imports - currently disabled due to model access issues
AI_UPSCALING_AVAILABLE = False


class ImageUpscaler(BaseTool):
    """High-quality image upscaler using advanced classical methods.

    This tool provides maximum quality image upscaling using enhanced classical algorithms
    including progressive upscaling, edge preservation, and sharpening techniques.
    """

    def __init__(self) -> None:
        """Initialize the image upscaler tool."""
        super().__init__(
            name="image_upscaler",
            description="High-quality image upscaler using advanced algorithms",
            version="1.0.0",
        )
        self._ai_model: Optional[Any] = None

    # AI model methods disabled due to model access issues
    # These can be re-enabled when proper AI models are available

    def _high_quality_upscale(
        self, image: np.ndarray, scale_factor: float
    ) -> np.ndarray:
        """High-quality upscaling using advanced classical methods.

        Args:
            image: Input image as numpy array
            scale_factor: Scale factor for upscaling

        Returns:
            Upscaled image as numpy array
        """
        height, width = image.shape[:2]

        if CV2_AVAILABLE:
            # Multi-step upscaling for better quality
            current_image = image.copy()
            current_scale = 1.0

            # Apply progressive upscaling for large scale factors
            while current_scale < scale_factor:
                step_scale = min(2.0, scale_factor / current_scale)
                current_height, current_width = current_image.shape[:2]
                step_width = int(current_width * step_scale)
                step_height = int(current_height * step_scale)

                # Use Lanczos4 for best quality
                current_image = cv2.resize(
                    current_image,
                    (step_width, step_height),
                    interpolation=cv2.INTER_LANCZOS4,
                )
                current_scale *= step_scale

            # Apply bilateral filtering for edge-preserving noise reduction
            upscaled = cv2.bilateralFilter(current_image, 9, 80, 80)

            # Gentle sharpening to enhance details
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpened = cv2.filter2D(upscaled, -1, kernel * 0.15)

            # Blend original and sharpened for natural look
            upscaled = cv2.addWeighted(upscaled, 0.7, sharpened, 0.3, 0)
            upscaled = np.clip(upscaled, 0, 255).astype(np.uint8)

        else:
            # Fallback to PIL with multiple steps
            pil_image = Image.fromarray(image)
            current_scale = 1.0

            while current_scale < scale_factor:
                step_scale = min(2.0, scale_factor / current_scale)
                current_size = pil_image.size
                new_size = (
                    int(current_size[0] * step_scale),
                    int(current_size[1] * step_scale),
                )

                # Use Lanczos resampling
                pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
                current_scale *= step_scale

            # Apply gentle smoothing then sharpening
            from PIL import ImageEnhance, ImageFilter

            # Light Gaussian blur to reduce upscaling artifacts
            pil_image = pil_image.filter(ImageFilter.GaussianBlur(radius=0.5))
            # Unsharp mask for detail enhancement
            pil_image = pil_image.filter(
                ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3)
            )

            # Mild contrast and sharpness enhancement
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.05)
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(1.1)

            upscaled = np.array(pil_image)

        return upscaled

    def validate_inputs(self, **kwargs) -> bool:
        """Validate input parameters.

        Args:
            **kwargs: Should contain 'input_path' and optionally 'output_path', 'scale_factor'

        Returns:
            True if inputs are valid, False otherwise
        """
        # Check required parameters
        if "input_path" not in kwargs:
            self.logger.error("Missing required parameter: 'input_path'")
            return False

        input_path = Path(kwargs["input_path"])
        if not input_path.exists():
            self.logger.error(f"Input file does not exist: {input_path}")
            return False

        if not input_path.is_file():
            self.logger.error(f"Input path is not a file: {input_path}")
            return False

        # Validate file extension
        valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
        if input_path.suffix.lower() not in valid_extensions:
            self.logger.error(f"Unsupported file format: {input_path.suffix}")
            return False

        # Validate scale factor if provided
        scale_factor = kwargs.get("scale_factor", 4.0)
        if not isinstance(scale_factor, (int, float)) or scale_factor <= 1.0:
            self.logger.error("Scale factor must be a number greater than 1.0")
            return False

        return True

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """Execute image upscaling.

        Args:
            **kwargs: Should contain:
                - input_path: Path to input image
                - output_path: Path for output image (optional)
                - scale_factor: Upscaling factor (optional, default: 4.0)
                - method: Upscaling method 'auto', 'ai', 'fallback' (optional, default: 'auto')

        Returns:
            Dictionary containing results and metadata
        """
        if not self.validate_inputs(**kwargs):
            raise ValueError("Invalid inputs provided")

        input_path = Path(kwargs["input_path"])
        scale_factor = kwargs.get("scale_factor", 4.0)
        method = kwargs.get("method", "auto")

        # Generate output path if not provided
        output_path = kwargs.get("output_path")
        if output_path is None:
            stem = input_path.stem
            suffix = input_path.suffix
            output_path = (
                input_path.parent / f"{stem}_upscaled_{int(scale_factor)}x{suffix}"
            )
        else:
            output_path = Path(output_path)

        self.logger.info(f"Upscaling {input_path} by {scale_factor}x to {output_path}")

        try:
            # Load image
            pil_image = Image.open(input_path).convert("RGB")
            original_width, original_height = pil_image.size

            # Choose upscaling method
            use_ai = False
            if method == "auto":
                use_ai = AI_UPSCALING_AVAILABLE
            elif method == "ai":
                use_ai = AI_UPSCALING_AVAILABLE
                if not use_ai:
                    self.logger.warning(
                        "AI upscaling requested but not available, using fallback"
                    )
            elif method == "fallback":
                use_ai = False
            else:
                self.logger.warning(f"Unknown method '{method}', using auto")
                use_ai = AI_UPSCALING_AVAILABLE

            # Perform upscaling - AI is currently disabled, so always use high-quality classical
            self.logger.info("Using high-quality classical upscaling method")
            image_np = np.array(pil_image)
            upscaled_np = self._high_quality_upscale(image_np, scale_factor)
            upscaled_image_pil = Image.fromarray(upscaled_np)
            method_used = "High-Quality Classical (Enhanced Lanczos)"

            # Save upscaled image
            upscaled_image_pil.save(output_path, optimize=True, quality=95)

            upscaled_width, upscaled_height = upscaled_image_pil.size

            result = {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "method_used": method_used,
                "scale_factor": scale_factor,
                "original_dimensions": (original_width, original_height),
                "upscaled_dimensions": (upscaled_width, upscaled_height),
                "actual_scale": (
                    upscaled_width / original_width,
                    upscaled_height / original_height,
                ),
                "file_size_before": input_path.stat().st_size,
                "file_size_after": output_path.stat().st_size,
                "success": True,
            }

            self.logger.info(
                f"Successfully upscaled image: {original_width}x{original_height} -> {upscaled_width}x{upscaled_height}"
            )
            return result

        except Exception as e:
            self.logger.error(f"Upscaling failed: {e}")
            return {
                "input_path": str(input_path),
                "output_path": str(output_path) if output_path else None,
                "error": str(e),
                "success": False,
            }
