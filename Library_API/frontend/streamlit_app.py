import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Library Management System")


# ---------------- SIDEBAR MENU ----------------

# ---------------- SIDEBAR MENU ----------------

st.sidebar.title("📚 Library Menu")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Book",
        "📚 View Books",
        "🔍 Search Books",
        "✏️ Update Book",
        "🗑️ Delete Book"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if menu == "🏠 Dashboard":

    st.header("📊 Library Dashboard")

    try:
        response = requests.get(f"{BASE_URL}/books")

        if response.status_code == 200:

            books = response.json()

            if books:

                # ---------- FIRST ROW ----------

                col1, col2 = st.columns(2)

                col1.metric(
                    "📚 Total Books",
                    len(books)
                )

                total_authors = len(
                    set(book["author"] for book in books)
                )

                col2.metric(
                    "✍️ Total Authors",
                    total_authors
                )


                # ---------- SECOND ROW ----------

                col3, col4 = st.columns(2)

                latest_book = books[-1]["title"]

                col3.metric(
                    "📖 Latest Book",
                    latest_book
                )

                highest_id = max(
                    book["id"] for book in books
                )

                col4.metric(
                    "🆔 Highest Book ID",
                    highest_id
                )


                # ---------- RECENT BOOKS ----------

                st.divider()

                st.subheader("📚 Recent Books")

                st.dataframe(
                    pd.DataFrame(books[-5:]),
                    use_container_width=True
                )

            else:
                st.info("📚 No books available.")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI server is not running!")


# ==================================================
# ADD BOOK
# ==================================================

elif menu == "➕ Add Book":

    st.header("➕ Add New Book")

    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author Name")

    if st.button("➕ Add Book", use_container_width=True):

        if title and author:

            data = {
                "title": title,
                "author": author
            }

            response = requests.post(
                f"{BASE_URL}/books",
                json=data
            )

            if response.status_code == 201:
                st.success("🎉 Book Added Successfully!")

            elif response.status_code == 409:
                st.warning("⚠️ This book already exists!")

            else:
                st.error("❌ Error adding book.")

        else:
            st.warning("⚠️ Please enter Book Title and Author.")


# ==================================================
# VIEW BOOKS
# ==================================================

elif menu == "📚 View Books":

    st.header("📚 All Books")

    response = requests.get(f"{BASE_URL}/books")

    if response.status_code == 200:

        books = response.json()

        if books:

            df = pd.DataFrame(books)

            st.success(f"Total Books: {len(books)}")

            st.dataframe(
                df,
                use_container_width=True
            )

        else:
            st.warning("No books available!")


# ==================================================
# SEARCH BOOKS
# ==================================================

elif menu == "🔍 Search Books":

    st.header("🔍 Search Books")

    search_type = st.radio(
        "Search By:",
        ["Title", "Author"]
    )

    search_value = st.text_input("Enter search value")

    if st.button("🔍 Search"):

        if search_value:

            if search_type == "Title":

                response = requests.get(
                    f"{BASE_URL}/books",
                    params={"title": search_value}
                )

            else:

                response = requests.get(
                    f"{BASE_URL}/books",
                    params={"author": search_value}
                )

            if response.status_code == 200:

                books = response.json()

                if books:

                    st.success(f"{len(books)} book(s) found!")

                    st.dataframe(
                        pd.DataFrame(books),
                        use_container_width=True
                    )

                else:
                    st.warning("No books found.")

        else:
            st.warning("⚠️ Please enter something to search.")


# ==================================================
# UPDATE BOOK
# ==================================================

elif menu == "✏️ Update Book":

    st.header("✏️ Update Book")

    book_id = st.number_input(
        "Enter Book ID",
        min_value=1,
        step=1
    )

    new_title = st.text_input("New Book Title")
    new_author = st.text_input("New Author Name")

    if st.button("💾 Update Book", use_container_width=True):

        if new_title and new_author:

            data = {
                "title": new_title,
                "author": new_author
            }

            response = requests.put(
                f"{BASE_URL}/books/{book_id}",
                json=data
            )

            if response.status_code == 200:
                st.success("🎉 Book Updated Successfully!")

            else:
                st.error("❌ Book not found!")

        else:
            st.warning("⚠️ Please enter Title and Author.")


# ==================================================
# DELETE BOOK
# ==================================================

elif menu == "🗑️ Delete Book":

    st.header("🗑️ Delete Book")

    st.warning("⚠️ This action cannot be undone!")

    book_id = st.number_input(
        "Enter Book ID to Delete",
        min_value=1,
        step=1
    )

    confirm = st.checkbox(
        "I confirm that I want to delete this book"
    )

    if st.button("🗑️ Delete Book", use_container_width=True):

        if confirm:

            response = requests.delete(
                f"{BASE_URL}/books/{book_id}"
            )

            if response.status_code == 200:
                st.success("🗑️ Book Deleted Successfully!")

            else:
                st.error("❌ Book not found!")

        else:
            st.warning("⚠️ Please confirm before deleting.")