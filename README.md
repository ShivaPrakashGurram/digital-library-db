# digital-library-db

## 🚀 Features

- 🔍 AI-Powered Book Search – Search books by category using Gemini AI (Google Generative AI).
- 🧾 Upload & Download Books – Securely upload and download PDFs to/from AWS S3.
- 👨‍💼 Role-Based Access – Admin, Clerk, and User functionalities.
- 🧠 FastAPI Backend – High-performance asynchronous API.
- 🧬 MongoDB Integration – Flexible document storage for users, books, and metadata.
- ☁️ AWS S3 – Store and retrieve book files with presigned URLs.

- ## 🛠 Tech Stack

- Backend: FastAPI (Python)
- Database: MongoDB
- AI Integration: Gemini AI 
- Storage: AWS S3 (Presigned URLs for file access)
- Environment: Python 3.11+, Uvicorn, Pydantic

-## EndPoints
ADMIN:-
- POST: /admin/create-book  ->Creates Book details in Database
- POST: /admin/upload-book/{title} ->Uploads Book to Aws_s3 storge
- DELETE: /admin/delete-book/{title} ->Deletes Book in Database
- POST: /clerk/issue-book/{username}/{book_title} ->Issues Book to user
- POST: /clerk/return-book/{username}/{book_title} ->Return Book by cleark
- GET: /clerk/check-availability/{book_title} ->Checks Availability of book
- POST: /user/request-book/{username}/{book_title} ->Request Book by user
- POST: /user/return-book/{username}/{book_title} ->Return book by user
- POST: /user/search-book-online/{category} ->Search books by category in online through Gemini Ai integration 
- GET: /user/download-book/{book_filename} ->Download Book by url


