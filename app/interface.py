"""Simple interface for the Colour Space Converter project."""

from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

from math_engine.converter import (
    RGB_TO_YIQ,
    channel_preview,
    convert_image_to_grayscale,
    convert_image_to_yiq,
    convert_yiq_array_to_rgb,
    image_difference,
    mathematical_summary,
    change_of_basis_demo,
)
from db.database import (
    initialize_database,
    save_image_record,
    save_colour_space_record,
    save_conversion_record,
    get_recent_history,
)
from ds.batch_queue import BatchQueue
from app.batch_processor import process_batch_file


def image_bytes(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def render_app():
    initialize_database()

    # Keep the interface plain: remove decorative motion and use neutral focus styles.
    st.markdown(
        """
        <style>
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
            scroll-behavior: auto !important;
        }
        button:focus, button:focus-visible,
        [role="tab"]:focus, [role="tab"]:focus-visible {
            outline: 1px solid #888888 !important;
            box-shadow: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Colour Space Converter")
    st.write("Linear Algebra Project 16 — RGB to YIQ conversion")

    converter_tab, grayscale_tab, batch_tab, maths_tab, history_tab = st.tabs(
        ["Image Converter", "Grayscale Tool", "Batch Queue", "Mathematics", "Database"]
    )

    with converter_tab:
        uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
        if uploaded is not None:
            try:
                image = Image.open(uploaded).convert("RGB")
                image.thumbnail((400, 400))
                st.image(image, caption="Original RGB image", use_container_width=True)

                if st.button("Convert image"):
                    yiq, original = convert_image_to_yiq(image)
                    restored = convert_yiq_array_to_rgb(yiq)
                    grayscale = convert_image_to_grayscale(image)
                    mae, rmse, _ = image_difference(original, restored)

                    image_id = save_image_record(
                        uploaded.name, original.width, original.height, uploaded.type
                    )
                    save_colour_space_record(image_id)
                    save_conversion_record(image_id, "RGB to YIQ to RGB", mae, rmse)

                    st.session_state["result"] = {
                        "filename": uploaded.name,
                        "yiq": yiq,
                        "original": original,
                        "restored": restored,
                        "grayscale": grayscale,
                        "mae": mae,
                        "rmse": rmse,
                    }
                    st.success("Conversion completed.")

                result = st.session_state.get("result")
                if result and result["filename"] == uploaded.name:
                    st.subheader("Y, I and Q channels")
                    cols = st.columns(3)
                    for col, index, channel in zip(cols, range(3), ["Y", "I", "Q"]):
                        col.image(
                            channel_preview(result["yiq"][:, :, index], channel),
                            caption=f"{channel} channel",
                            use_container_width=True,
                        )

                    st.subheader("Restored RGB image")
                    cols = st.columns(2)
                    cols[0].image(result["original"], caption="Original", use_container_width=True)
                    cols[1].image(result["restored"], caption="Restored", use_container_width=True)

                    st.write(f"Mean Absolute Error (MAE): {result['mae']:.6f}")
                    st.write(f"Root Mean Square Error (RMSE): {result['rmse']:.6f}")

                    st.subheader("Grayscale image")
                    st.image(result["grayscale"], use_container_width=True)
                    st.write(
                        "Grayscale keeps brightness only. Different RGB colours can have "
                        "the same brightness, so the original colours cannot be recovered uniquely."
                    )
                    st.download_button(
                        "Download restored image",
                        image_bytes(result["restored"]),
                        file_name="restored_rgb.png",
                        mime="image/png",
                    )
            except (UnidentifiedImageError, OSError, ValueError) as error:
                st.error(f"Could not open the image: {error}")

    with grayscale_tab:
        st.subheader("RGB to Grayscale")
        st.write(
            "This separate tool converts each RGB pixel into one brightness value. "
            "Because three colour values become one value, the original colour cannot "
            "be recovered uniquely."
        )
        gray_upload = st.file_uploader(
            "Choose an image for grayscale conversion",
            type=["png", "jpg", "jpeg"],
            key="grayscale_upload",
        )
        if gray_upload is not None:
            try:
                gray_image = Image.open(gray_upload).convert("RGB")
                gray_image.thumbnail((400, 400))
                st.image(gray_image, caption="Original RGB image", use_container_width=True)
                if st.button("Convert to grayscale", key="convert_grayscale"):
                    gray_result = convert_image_to_grayscale(gray_image)
                    st.session_state["grayscale_result"] = {
                        "filename": gray_upload.name,
                        "image": gray_result,
                    }
                gray_result = st.session_state.get("grayscale_result")
                if gray_result and gray_result["filename"] == gray_upload.name:
                    st.image(gray_result["image"], caption="Grayscale output", use_container_width=True)
                    st.info(
                        "Linear algebra: grayscale is a rank-1 transformation from R³ to R¹. "
                        "It keeps brightness but loses two dimensions of colour information. "
                        "Many different RGB colours can produce the same gray value."
                    )
            except (UnidentifiedImageError, OSError, ValueError) as error:
                st.error(f"Could not open this image: {error}")

    with batch_tab:
        files = st.file_uploader(
            "Choose multiple images",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="batch_files",
        )
        if st.button("Process queue", disabled=not files):
            queue = BatchQueue()
            for file in files:
                queue.enqueue(file)

            st.write(f"Images in queue: {queue.size()}")
            while not queue.is_empty():
                file = queue.dequeue()
                result = process_batch_file(file)
                if result["status"] == "success":
                    st.write(
                        f"{file.name}: completed "
                        f"(MAE {result['mae']:.6f}, RMSE {result['rmse']:.6f})"
                    )
                else:
                    st.error(f"{file.name}: failed — {result['error']}")
            st.success("Queue processing completed.")

    with maths_tab:
        st.subheader("RGB to YIQ matrix")
        st.latex(
            r"\begin{bmatrix}Y\\I\\Q\end{bmatrix}="
            r"\begin{bmatrix}0.299&0.587&0.114\\0.596&-0.274&-0.322\\0.211&-0.523&0.312\end{bmatrix}"
            r"\begin{bmatrix}R\\G\\B\end{bmatrix}"
        )
        st.write("Matrix used in the conversion:")
        st.dataframe(RGB_TO_YIQ, use_container_width=True)

        summary = mathematical_summary()
        st.write(f"Determinant: {summary['determinant']:.6f}")
        st.write(f"Rank of RGB to YIQ matrix: {summary['rank_rgb_to_yiq']}")
        st.write(f"Rank of grayscale matrix: {summary['rank_grayscale']}")
        st.write("Inverse matrix:")
        st.dataframe(summary["inverse"], use_container_width=True)

        st.subheader("Change of basis: RGB coordinates to YIQ coordinates")
        st.write(
            "RGB is the original coordinate system. Y, I and Q are coordinates "
            "of the same colour in a new basis. The columns of the inverse matrix "
            "are the YIQ basis vectors expressed in RGB coordinates."
        )
        st.latex(r"[RGB]_{RGB} = B_{YIQ\ in\ RGB}[YIQ]_{YIQ}")
        st.latex(r"[YIQ]_{YIQ} = B_{YIQ\ in\ RGB}^{-1}[RGB]_{RGB}")
        st.write("YIQ basis vectors expressed in RGB coordinates (columns form the basis matrix):")
        st.dataframe(summary["yiq_basis_in_rgb"], use_container_width=True)
        demo = change_of_basis_demo()
        st.write(f"Example RGB colour: {demo['rgb']}")
        st.write(f"Its YIQ coordinates: {tuple(round(v, 6) for v in demo['yiq'])}")
        st.write(
            "Converting those YIQ coordinates back through the YIQ basis gives: "
            f"{tuple(round(v, 6) for v in demo['reconstructed_rgb'])}"
        )
        st.write(
            "The RGB to YIQ matrix has rank 3 and is invertible. "
            "The grayscale matrix has rank 1 and loses colour information."
        )

    with history_tab:
        st.subheader("Saved conversions")
        history = get_recent_history()
        if history:
            st.dataframe(
                [
                    {
                        "ID": row[0],
                        "Image": row[1],
                        "Operation": row[2],
                        "MAE": row[3],
                        "RMSE": row[4],
                        "Status": row[5],
                        "Date": row[6],
                    }
                    for row in history
                ],
                use_container_width=True,
            )
        else:
            st.write("No conversions saved yet.")
