import streamlit as st

from svg2mod import svg
from svg2mod.exporter import Svg2ModExportPretty
from svg2mod.importer import Svg2ModImport

st.set_page_config(page_title='KiCad tool: svg2mod', page_icon='🖼️', layout='centered')

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("KiCad tool: svg2mod")
st.text("Convert Inkscape SVG image to KiCad footprint")

st.markdown("-----")
image = st.file_uploader("Upload SVG image file", type=['svg'])

if image is not None:
    with open("footprint.svg", 'wb') as image_file:
        image_file.write(image.read())

    imported = Svg2ModImport(
        "footprint.svg",
        module_name = "svg2mod",
        module_value = "G***",
        ignore_hidden = True,
        force_layer = None
    )

    exported = Svg2ModExportPretty(
        imported,
        None,
        center = True,
        scale_factor = 1.0,
        precision = 5.0,
        dpi = 96,
        pads = False,
    )

    exported.write()

    if st.button("Convert"):
        st.success("Conversion successful!") 

        st.download_button(label="Download footprint", data=exported.raw_file_data, file_name="footprint.KiCad_mod", mime="plain/text")

st.markdown("""
-----
##### Made with lots of ⏱️, 📚 and ☕ by InputBlackBoxOutput
""")
