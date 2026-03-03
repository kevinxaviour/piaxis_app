import streamlit as st
import requests
from dotenv import load_dotenv
import os

# ---------------------------
# Load Environment Variables
# ---------------------------
load_dotenv()

BASE_URL_1 = os.getenv("URL")     # Task 1 Backend
BASE_URL_2 = os.getenv("URL2")    # Task 2 Backend

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Piaxis Unified Library",
    layout="wide"
)

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Piaxis Unified Portal")
st.sidebar.markdown("---")

main_page = st.sidebar.radio(
    "Select Module",
    ["Task 1 - Detail Library", "Task 2 - Secure Access"]
)

st.sidebar.markdown("---")

# =========================================================
# ======================= TASK 1 ==========================
# =========================================================

if main_page == "Task 1 - Detail Library":

    st.sidebar.subheader("Detail Library Options")

    page = st.sidebar.radio(
        "Navigation",
        ["View Details", "Search Details", "Suggest Detail"]
    )

    # ---------------------------
    # View Details
    # ---------------------------
    if page == "View Details":

        st.title("Architectural Details")

        if st.button("Load All Details"):

            try:
                response = requests.get(f"{BASE_URL_1}/details")

                if response.status_code == 200:
                    details = response.json()
                    st.success(f"Loaded {len(details)} records")
                    st.dataframe(details, use_container_width=True)
                else:
                    st.error("Failed to fetch details.")

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

    # ---------------------------
    # Search Details
    # ---------------------------
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
                try:
                    response = requests.get(
                        f"{BASE_URL_1}/details/search",
                        params={"q": query}
                    )

                    if response.status_code == 200:
                        results = response.json()

                        if results:
                            st.success(f"Found {len(results)} matches")
                            st.dataframe(results, use_container_width=True)
                        else:
                            st.info("No matching details found.")
                    else:
                        st.error("Search failed.")

                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")

    # ---------------------------
    # Suggest Detail
    # ---------------------------
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

            try:
                response = requests.post(
                    f"{BASE_URL_1}/suggest-detail",
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()

                    if "detail" in data:
                        st.success("Match Found")
                        st.json(data)
                    else:
                        st.warning(data.get("message", "No match found."))
                else:
                    st.error("Suggestion request failed.")

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

# =========================================================
# ======================= TASK 2 ==========================
# =========================================================

elif main_page == "Task 2 - Secure Access":

    st.sidebar.subheader("Secure Access Options")

    page = st.sidebar.radio(
        "Navigation",
        ["View Users", "Secure Details"]
    )

    # ---------------------------
    # View Users
    # ---------------------------
    if page == "View Users":

        st.title("Registered Users")

        if st.button("Load All Users"):

            try:
                response = requests.get(f"{BASE_URL_2}/users")

                if response.status_code == 200:
                    users = response.json()

                    if users:
                        st.success(f"Loaded {len(users)} users")
                        st.dataframe(users, use_container_width=True)
                    else:
                        st.info("No users found.")
                else:
                    st.error("Failed to fetch users.")

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

    # ---------------------------
    # Secure Details
    # ---------------------------
    elif page == "Secure Details":

        st.title("Secure Architectural Details")

        st.markdown("Enter your registered email to view accessible details.")

        email = st.text_input("Email Address")

        search_btn = st.button("Search Details")

        if search_btn:

            if email.strip() == "":
                st.warning("Please enter an email.")
                st.stop()

            try:
                response = requests.get(
                    f"{BASE_URL_2}/secure/details",
                    headers={"x-user-email": email}
                )

                if response.status_code == 200:

                    data = response.json()

                    auth_info = data.get("authenticated_as", {})
                    row_count = data.get("row_count", 0)
                    details = data.get("details", [])

                    st.success("Authentication Successful")

                    col1, col2 = st.columns(2)
                    col1.metric("Role", auth_info.get("role", "N/A"))
                    col2.metric("Accessible Rows", row_count)

                    st.divider()

                    st.subheader("Accessible Details")

                    if row_count == 0:
                        st.info("No accessible details found for this user.")
                    else:
                        st.dataframe(details, use_container_width=True)

                else:
                    try:
                        error_message = response.json().get("detail", "Unknown error")
                    except:
                        error_message = "Unknown error"

                    st.error(error_message)

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
