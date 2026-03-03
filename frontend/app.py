import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()

BASE_URL = os.getenv("URL")


# Page config
st.set_page_config(
    page_title="Piaxis Detail Library",
    layout="wide"
)


# SideBar Navigation
st.sidebar.title("Piaxis Library")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["View Details", "Search Details", "Suggest Detail"]
)

st.sidebar.markdown("---")


# View Details

if page == "View Details":

    st.title("Architectural Details")

    if st.button("Load All Details"):
        response = requests.get(f"{BASE_URL}/details")

        if response.status_code == 200:
            details = response.json()
            st.table(details)
        else:
            st.error("Failed to fetch details.")


# Search Details
elif page == "Search Details":

    st.title("Search Detail Library")

    query = st.text_input("Enter search keyword")

    col1, col2 = st.columns([1, 5])
    with col1:
        search_btn = st.button("Search")

    if search_btn:
        if query.strip() == "":
            st.warning("Please enter a search term.")
        else:
            response = requests.get(
                f"{BASE_URL}/details/search",
                params={"q": query}
            )

            if response.status_code == 200:
                results = response.json()

                if results:
                    st.table(results)
                else:
                    st.info("No matching details found.")
            else:
                st.error("Search failed.")


# Suggest Details

elif page == "Suggest Detail":

    st.title("Smart Detail Suggestion")

    col1, col2, col3 = st.columns(3)

    with col1:
        host = st.selectbox(
            "Host Element",
            ["External Wall", "Window", "Internal Wall"]
        )

    with col2:
        adjacent = st.selectbox(
            "Adjacent Element",
            ["Slab", "External Wall", "Floor"]
        )

    with col3:
        exposure = st.selectbox(
            "Exposure",
            ["External", "Internal"]
        )

    st.markdown("")

    if st.button("Get Suggestion", use_container_width=True):

        payload = {
            "host_element": host,
            "adjacent_element": adjacent,
            "exposure": exposure
        }

        response = requests.post(
            f"{BASE_URL}/suggest-detail",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()

            if "detail" in data:
                st.write(data)

            else:
                st.warning(data.get("message", "No match found."))
        else:

            st.error("Suggestion request failed.")

