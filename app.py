import streamlit as st

from svg2mod import svg
from svg2mod.exporter import Svg2ModExportPretty
from svg2mod.importer import Svg2ModImport

st.set_page_config(page_title='KiCad tool: svg2mod', page_icon='🖼️', layout='centered')

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("KiCad tool: svg2mod")
st.text("Convert Inkscape SVG image to KiCad footprint")
st.image("example.png", use_column_width=True)

st.markdown("""
## How to use the tool?
- Upload SVG image
- Change conversion options as per requirement
- Press the <kbd>Convert</kbd> button
-----
""", unsafe_allow_html=True)

image = st.file_uploader("Upload SVG image file", type=['svg'])

if image is not None:
    with open("footprint.svg", 'wb') as image_file:
        image_file.write(image.read())

    module_name = st.text_input(label="Base name of the module", value="svg2mod")
    module_value = st.text_input(label="Value of the module", value="G***")
    scale_factor = st.number_input(label="Scale paths by this factor", value=1.0)
    precision = st.number_input(label="Smoothness for approximating curves with line segments", value=5.0)
    dpi = st.number_input(label="DPI of the SVG file", value=96)
    force_layer = st.text_input(label="Force everything into the single provided layer", value="")
    
    ignore_hidden = st.checkbox(label="Do not export hidden objects", value=True)
    center = st.checkbox(label="Center the module to the center of the bounding box", value=False)
    pads = st.checkbox(label="Convert any artwork on Cu layers to pads", value=False)

    try:
        imported = Svg2ModImport(
            "footprint.svg",
            module_name = module_name,
            module_value = module_value,
            ignore_hidden = ignore_hidden,
            force_layer = force_layer
        )

        exported = Svg2ModExportPretty(
            imported,
            None,
            center = center,
            scale_factor = scale_factor,
            precision = precision,
            dpi = dpi,
            pads = pads,
        )

        exported.write()
    except Exception:
        st.error("Something went wrong!")
        st.stop()

    if st.button("Convert"):
        st.markdown("-----")
        st.success("Footprint generated successfully!") 

        st.download_button(
            label="Download footprint", 
            data=exported.raw_file_data, 
            file_name="footprint.kicad_mod", 
            mime="plain/text")

st.markdown("""
-----
##### Made with lots of ⏱️, 📚 and ☕ by InputBlackBoxOutput
""")
