# Fast-API-Studying


uvicorn main:app --port 8082 --reload


docker run --name postgres-container -v /home/josearangos/Documentos/Courses/postgresbds:/var/lib/postgresql/data -e POSTGRES_PASSWORD=mysecretpassword -d postgres:latest