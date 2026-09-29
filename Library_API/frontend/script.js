const API_URL = "http://127.0.0.1:8000/books";


// GET BOOKS
async function getBooks() {
    const response = await fetch(API_URL);
    const books = await response.json();

    const bookList = document.getElementById("bookList");

    bookList.innerHTML = "";

    books.forEach(book => {
        bookList.innerHTML += `
            <div>
                <h3>${book.title}</h3>
                <p>Author: ${book.author}</p>

                <button onclick="editBook(${book.id})">
                    Edit
                </button>

                <button onclick="deleteBook(${book.id})">
                    Delete
                </button>
            </div>

            <hr>
        `;
    });
}


// ADD BOOK
async function addBook() {
    const title = document.getElementById("title").value.trim();
    const author = document.getElementById("author").value.trim();

    if (title === "" || author === "") {
        alert("Please enter title and author");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                author: author
            })
        });

        const data = await response.json();

        console.log(data);

        if (!response.ok) {
            alert(JSON.stringify(data));
            return;
        }

        document.getElementById("title").value = "";
        document.getElementById("author").value = "";

        getBooks();

    } catch (error) {
        console.log(error);
        alert("Book add होत नाही. FastAPI server चालू आहे का ते check कर.");
    }
}

// DELETE BOOK
async function deleteBook(id) {

    const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    const data = await response.json();

    console.log(data);

    getBooks();
}


// EDIT BOOK
async function editBook(id) {

    const newTitle = prompt("Enter new book title:");

    if (!newTitle) {
        return;
    }

    const newAuthor = prompt("Enter new author name:");

    if (!newAuthor) {
        return;
    }

    const response = await fetch(`${API_URL}/${id}`, {
        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: newTitle,
            author: newAuthor
        })
    });

    const data = await response.json();

    console.log(data);

    getBooks();
}


// LOAD BOOKS WHEN PAGE OPENS
getBooks();