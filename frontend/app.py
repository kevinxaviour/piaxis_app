import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Piaxis Detail Library",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------
# st.markdown("""
# <style>
# .main {
#     padding-top: 2rem;
# }
# .card {
#     background-color: #f8f9fa;
#     padding: 1.5rem;
#     border-radius: 10px;
#     box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
#     margin-bottom: 1rem;
# }
# .title {
#     font-size: 20px;
#     font-weight: 600;
# }
# .description {
#     color: #444;
# }
# </style>
# """, unsafe_allow_html=True)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("Piaxis Library")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["View Details", "Search Details", "Suggest Detail"]
)

st.sidebar.markdown("---")

# -----------------------------
# SECTION 1: VIEW DETAILS
# -----------------------------
if page == "View Details":

    st.title("Architectural Details")

    if st.button("Load All Details"):
        response = requests.get(f"{BASE_URL}/details")

        if response.status_code == 200:
            details = response.json()

            for d in details:
                st.markdown(f"""
                <div class="card">
                    <div class="title">{d['title']}</div>
                    <div class="description">{d['description']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Failed to fetch details.")

# -----------------------------
# SECTION 2: SEARCH DETAILS
# -----------------------------
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
                    for r in results:
                        st.markdown(f"""
                        <div class="card">
                            <div class="title">{r['title']}</div>
                            <div class="description">{r['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No matching details found.")
            else:
                st.error("Search failed.")

# -----------------------------
# SECTION 3: SUGGEST DETAIL
# -----------------------------
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
                st.success("Best Matching Detail Found")

                st.markdown(f"""
                <div class="card">
                    <div class="title">{data['detail']['title']}</div>
                    <div class="description">{data['detail']['description']}</div>
                </div>
                """, unsafe_allow_html=True)

                st.info(data["explanation"])

            else:
                st.warning(data.get("message", "No match found."))
        else:
            st.error("Suggestion request failed.")