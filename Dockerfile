# 1. Use a lightweight Python base image to keep the container small and secure
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first to leverage Docker layer caching
# (This means if you change your Python code later, Docker doesn't have to reinstall Pandas every time)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project files into the container
COPY . .

# 6. Expose the port FastAPI runs on
EXPOSE 8000

# 7. Command to run the application when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]