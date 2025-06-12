import streamlit as st
from PIL import Image
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from io import BytesIO
import streamlit_image_comparison as sic

# --- Streamlit Page Config ---
st.set_page_config(page_title="UWH Image Quality Analyzer", layout="wide")
st.title("🌊 Underwater Image Enhancement Quality Analyzer")

# --- Sidebar: Image upload ---
uploaded = st.sidebar.file_uploader("Upload underwater image", type=["jpg", "png", "jpeg"])
if uploaded:
    original = Image.open(uploaded).convert("RGB")
    buf = BytesIO()
    original.save(buf, format="JPEG")
    img_data = buf.getvalue()

    # --- Enhancement stub ---
    enhanced = original  # Replace this line with your actual enhancement function

    # --- Layout display ---
    st.subheader("Original vs Enhanced")
    sic.compare_images(
        original=original,
        transformed=enhanced,
        label="Original",
        label2="Enhanced",
        width=700,
    )

    # --- Compute metrics ---
    orig_arr = np.array(original)
    enh_arr = np.array(enhanced)
    psnr_val = peak_signal_noise_ratio(orig_arr, enh_arr, data_range=255)
    ssim_val = structural_similarity(orig_arr, enh_arr, multichannel=True, data_range=255)

    st.markdown("### 📊 Quality Metrics")
    st.write(f"- **PSNR**: {psnr_val:.2f} dB  ")
    st.write(f"- **SSIM**: {ssim_val:.3f}")

    st.info("Higher PSNR & SSIM indicate better similarity to the original 📈")
else:
    st.sidebar.info("Upload an image to see quality analysis.")
