import streamlit as st
from scrape import scrape_website, clean_body_content, extract_body_content, split_dom_content
from parse import parse_with_ollama

def main():
    st.title("test")
    url = st.text_input("url")
    if st.button("scrape", disabled=len(url)==0):
        st.write("button clicked")
        data = scrape_website(url)
        body_content = extract_body_content(data)
        clean_content = clean_body_content(body_content)
        print("ddd==", clean_content,"==end")
        st.session_state.dom_content = clean_content

        with st.expander("view DOM content"):
            st.text_area("DOM content", clean_content, height=400)
    if 'dom_content' in st.session_state:
        parse_description = st.text_area("Describe what you want to parse?")
        if st.button("parse", disabled = not parse_description):
            st.write("parsing content....")

            dom_chunks= split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
    print("Hello from scraper!")


if __name__ == "__main__":
    main()
