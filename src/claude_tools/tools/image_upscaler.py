"""Image upscaler tool using Real-ESRGAN for maximum quality."""

from pathlib import Path
from typing import Any, Dict, Optional

try:
    import cv2
    import numpy as np
    from PIL import Image

    # Real-ESRGAN imports
    try:
        from basicsr.archs.rrdbnet_arch import RRDBNet
        from realesrgan import RealESRGANer

        REALESRGAN_AVAILABLE = True
    except ImportError:
        REALESRGAN_AVAILABLE = False

    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    REALESRGAN_AVAILABLE = False

from claude_tools.core.base_tool import BaseTool


class ImageUpscaler(BaseTool):
    """High-quality image upscaler using AI-based Real-ESRGAN with fallback methods.

    This tool provides maximum quality image upscaling primarily using Real-ESRGAN,
    with classical interpolation methods as fallback when AI models aren't available.
    """

    def __init__(self) -> None:
        """Initialize the image upscaler tool."""
        super().__init__(
            name="image_upscaler",
            description="AI-powered image upscaler for maximum quality results",
            version="1.0.0",
        )
        self._upsampler: Optional[RealESRGANer] = None

    def _initialize_realesrgan(self, model_name: str = "RealESRGAN_x4plus") -> bool:
        """Initialize Real-ESRGAN upsampler.

        Args:
            model_name: Name of the Real-ESRGAN model to use

        Returns:
            True if initialization successful, False otherwise
        """
        if not REALESRGAN_AVAILABLE:
            self.logger.warning("Real-ESRGAN not available, will use fallback methods")
            return False

        try:
            # Define model configurations
            models = {
                "RealESRGAN_x4plus": {
                    "model_path": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
                    "scale": 4,
                    "arch": "RRDBNet",
                    "num_block": 23,
                    "num_grow_ch": 32,
                },
                "RealESRGAN_x2plus": {
                    "model_path": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
                    "scale": 2,
                    "arch": "RRDBNet",
                    "num_block": 23,
                    "num_grow_ch": 32,
                },
            }

            if model_name not in models:
                self.logger.error(f"Unknown model: {model_name}")
                return False

            model_info = models[model_name]

            # Initialize the model architecture
            model = RRDBNet(
                num_in_ch=3,
                num_out_ch=3,
                num_feat=64,
                num_block=model_info["num_block"],
                num_grow_ch=model_info["num_grow_ch"],
                scale=model_info["scale"],
            )

            # Initialize the upsampler
            self._upsampler = RealESRGANer(
                scale=model_info["scale"],
                model_path=model_info["model_path"],
                model=model,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=False,  # Use FP32 for better quality
                gpu_id=None,  # Auto-detect GPU
            )

            self.logger.info(f"Real-ESRGAN {model_name} initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Real-ESRGAN: {e}")
            return False

    def _fallback_upscale(self, image: np.ndarray, scale_factor: float) -> np.ndarray:
        """Fallback upscaling using classical interpolation.

        Args:
            image: Input image as numpy array
            scale_factor: Scale factor for upscaling

        Returns:
            Upscaled image as numpy array
        """
        height, width = image.shape[:2]
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Use Lanczos for best quality among classical methods
        if CV2_AVAILABLE:
            upscaled = cv2.resize(
                image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4
            )
        else:
            # Fallback to PIL
            pil_image = Image.fromarray(image)
            upscaled_pil = pil_image.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )
            upscaled = np.array(upscaled_pil)

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
                - method: Upscaling method 'auto', 'realesrgan', 'fallback' (optional, default: 'auto')

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
            if CV2_AVAILABLE:
                image = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
                if image is None:
                    raise ValueError(f"Could not load image: {input_path}")
            else:
                pil_image = Image.open(input_path).convert("RGB")
                image = np.array(pil_image)

            original_height, original_width = image.shape[:2]

            # Choose upscaling method
            use_realesrgan = False
            if method == "auto":
                use_realesrgan = REALESRGAN_AVAILABLE
            elif method == "realesrgan":
                use_realesrgan = REALESRGAN_AVAILABLE
                if not use_realesrgan:
                    self.logger.warning(
                        "Real-ESRGAN requested but not available, using fallback"
                    )
            elif method == "fallback":
                use_realesrgan = False
            else:
                self.logger.warning(f"Unknown method '{method}', using auto")
                use_realesrgan = REALESRGAN_AVAILABLE

            # Perform upscaling
            if use_realesrgan:
                if self._upsampler is None:
                    model_name = (
                        "RealESRGAN_x4plus"
                        if scale_factor >= 4
                        else "RealESRGAN_x2plus"
                    )
                    if not self._initialize_realesrgan(model_name):
                        use_realesrgan = False

                if use_realesrgan:
                    self.logger.info("Using Real-ESRGAN for upscaling")
                    upscaled_image, _ = self._upsampler.enhance(
                        image, outscale=scale_factor
                    )
                    method_used = "Real-ESRGAN"
                else:
                    self.logger.info("Real-ESRGAN failed, using fallback method")
                    upscaled_image = self._fallback_upscale(image, scale_factor)
                    method_used = "Lanczos (fallback)"
            else:
                self.logger.info("Using fallback interpolation method")
                upscaled_image = self._fallback_upscale(image, scale_factor)
                method_used = "Lanczos"

            # Save upscaled image
            if CV2_AVAILABLE:
                success = cv2.imwrite(str(output_path), upscaled_image)
                if not success:
                    raise ValueError(f"Failed to save image to {output_path}")
            else:
                pil_output = Image.fromarray(upscaled_image)
                pil_output.save(output_path)

            upscaled_height, upscaled_width = upscaled_image.shape[:2]

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
